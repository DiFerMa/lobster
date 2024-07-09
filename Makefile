SYSTEM_PYTHONPATH:=$(PYTHONPATH)
export LOBSTER_ROOT=$(PWD)
export PYTHONPATH=$(LOBSTER_ROOT)

ASSETS=$(wildcard assets/*.svg)

lobster/html/assets.py: $(ASSETS) util/mkassets.py
	util/mkassets.py lobster/html/assets.py $(ASSETS)

lint: style
	@PYTHONPATH=$(SYSTEM_PYTHONPATH) \
	python -m pylint --rcfile=pylint3.cfg \
		--reports=no \
		--ignore=assets.py \
		lobster

style:
	python -m pycodestyle lobster \
		--exclude=assets.py

.PHONY: packages
packages:
	# git clean -xdf
	# export LOBSTER_ROOT="C:/Projects/Github/lobster"
	# $(LOBSTER_ROOT)
	# export PYTHONPATH="C:/Projects/Github/lobster"
	# $(PYTHONPATH)
	rm -rf test_install
	rm -rf test_install_monolithic
	make lobster/html/assets.py
	make -C packages/lobster-core
	make -C packages/lobster-tool-trlc
	make -C packages/lobster-tool-codebeamer
	make -C packages/lobster-tool-cpp
	make -C packages/lobster-tool-gtest
	make -C packages/lobster-tool-json
	make -C packages/lobster-tool-python
	make -C packages/lobster-metapackage
	make -C packages/lobster-monolithic
	PYTHONPATH= \
		pip3 install --prefix test_install \
		packages/*/dist/*.whl
	PYTHONPATH= \
		pip3 install --prefix test_install_monolithic \
		packages/lobster-monolithic/meta_dist/*.whl
	diff -Naur test_install/lib/site-packages/lobster test_install_monolithic/lib/site-packages/lobster -x "*.pyc"
	# diff -Naur test_install/scripts test_install_monolithic/scripts

integration-tests: packages
	(cd integration-tests/projects/basic; make)
	(cd integration-tests/projects/filter; make)

system-tests:
	make -B -C test-system/lobster-json
	make -B -C test-system/lobster-python

unit-tests:
	python -m unittest discover -s test-unit -v

test: integration-tests system-tests unit-tests

upload-main: packages
	python -m twine upload --repository pypi packages/*/dist/*
	python -m twine upload --repository pypi packages/*/meta_dist/*

remove-dev:
	python -m util.release

github-release:
	git push
	python -m util.github_release

bump:
	python -m util.bump_version_post_release

full-release:
	make remove-dev
	git push
	make upload-main
	make github-release
	make bump
	git push
