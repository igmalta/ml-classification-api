# Makefile
.PHONY: help
help:
	@echo "Commands:"
	@echo "venv   : creates development environment."
	@echo "vconda : creates conda development environment."
	@echo "style  : runs style formatting."
	@echo "clean  : cleans all unecessary files."
	@echo "test   : run all tests."

# Environment
.ONESHELL:
venv:
	python3 -m venv venv
	source venv/bin/activate && \
	python -m pip install --upgrade pip setuptools wheel && \
	python -m pip install poetry && \
	poetry install

# Conda environment
SHELL := /bin/bash

greeting:
	@echo ${PYTHON}

.PHONY:
vconda:
	conda create -p venv --copy -y python=$(PYTHON)
	source activate ./venv && \
	python -m pip install --upgrade pip setuptools wheel && \
	python -m pip install poetry && \
	poetry install

# Styling
.PHONY: style
style:
	black .
	flake8
	isort .

# Cleaning
.PHONY: clean
clean: style
	find . -type f -name "*.DS_Store" -ls -delete
	find . | grep -E "(__pycache__|\.pyc|\.pyo)" | xargs rm -rf
	find . | grep -E ".pytest_cache" | xargs rm -rf
	find . | grep -E ".ipynb_checkpoints" | xargs rm -rf
	rm -f .coverage

# Test
.PHONY: test
test:
	python -m pytest