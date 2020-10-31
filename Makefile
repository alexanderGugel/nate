.PHONY: test bench

test:
	@python -m unittest tests/*_test.py -v

bench:
	@python -m tests.tags_bench