.PHONY: test lint types bench

all: lint types test

test:
	@python -m unittest tests/*_test.py -v

lint:
	@python -m flake8 nate tests

types:
	@python -m mypy nate tests

bench:
	@python -m tests.tags_bench