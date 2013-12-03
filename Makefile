.PHONY: pyz dist upload

pyz:
	pyzzer.pyz -o build/envdir-$(shell python setup.py --version).pyz -m envdir:run -r envdir

dist:
	python setup.py sdist bdist_wheel

upload:
	twine upload -s dist/*
