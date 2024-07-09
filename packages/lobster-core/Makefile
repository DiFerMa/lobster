package:
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf lobster
	mkdir -p lobster/tools
	cp ../../lobster/*.py lobster
	cp -Rv ../../lobster/config lobster
	cp -Rv ../../lobster/html lobster
	cp ../../lobster/tools/*.py lobster/tools
	cp -Rv ../../lobster/tools/core lobster/tools
	python setup.py sdist bdist_wheel
