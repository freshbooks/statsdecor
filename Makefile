.PHONY: clean-pyc clean-build docs clean install lint test test-all
.PHONY: coverage release dist

help:
	@echo "install - Install development dependencies."
	@echo "clean - Remove all build, test, coverage and Python artifacts."
	@echo "clean-build - Remove build artifacts."
	@echo "clean-pyc - Remove Python bytecode."
	@echo "clean-test - Remove test and coverage artifacts."
	@echo "lint - Check style with flake8."
	@echo "test - Run tests quickly with the default Python."
	@echo "test-all - Run tests on every Python version with tox."
	@echo "coverage - Check code coverage with the default Python."
	@echo "release - Package and upload a release."
	@echo "dist - Create tar and whl files."

install: requirements-dev.txt requirements.txt
	pip install -r requirements-dev.txt

clean: clean-build clean-pyc clean-test

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

lint:
	flake8 statsdecor tests

test:
	py.test tests/

test-all:
	tox

coverage:
	coverage run --source statsdecor `which py.test` tests/
	coverage report -m
	coverage html

release: clean
	python setup.py sdist upload
	python setup.py bdist_wheel upload

dist: clean
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

tag:
	git tag $(shell cat VERSION)
	git push --tags
