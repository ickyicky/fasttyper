build:
	python setup.py sdist bdist_wheel

push:
	twine upload dist/*