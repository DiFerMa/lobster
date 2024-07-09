package:
	rm -rf build
	rm -rf dist
	rm -rf meta_dist
	rm -rf *.egg-info
	rm -rf lobster
	cp -Rv ../../lobster lobster
	python setup.py sdist bdist_wheel
	mv dist meta_dist
