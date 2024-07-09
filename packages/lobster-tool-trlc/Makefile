package:
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf lobster
	mkdir -p lobster/tools
	cp ../../lobster/version.py lobster
	cp -Rv ../../lobster/tools/trlc lobster/tools
	python setup.py sdist bdist_wheel
