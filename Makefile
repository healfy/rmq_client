.PHONY: lint clean test

lint:
	flake8
clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	isort .

test:
	pytest
