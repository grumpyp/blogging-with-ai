lint:
	mypy src --strict
	flake8 src --max-line-length 120

test:
	pytest src/tests