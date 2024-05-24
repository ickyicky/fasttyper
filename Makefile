build: fasttyper dist
	python3 setup.py sdist bdist_wheel

push:
	twine upload dist/*

clean:
	rm dist/*
