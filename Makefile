clean:
	rm -rf .ipynb_checkpoints
	rm -rf **/.ipynb_checkpoints
	rm -rf .pytest_cache
	rm -rf build
	rm -rf dist

pypi: clean
	python setup.py sdist
	python setup.py bdist_wheel --universal
	twine upload dist/*

install:
	python -m pip install --upgrade pip
	python -m pip install -e .
