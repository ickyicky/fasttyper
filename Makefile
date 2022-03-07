build: fasttyper
	python setup.py sdist bdist_wheel

push:
	twine upload dist/*

clean:
	rm dist/*
