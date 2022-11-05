#!/usr/bin/env bash

ACTIVE_ENV := . .venv/bin/activate

.PHONY: setup
setup:
	[ -d .venv ] || python3 -m venv .venv 
	${ACTIVE_ENV} && pip install -Ur requirements.txt

.PHONY: run
run:
	${ACTIVE_ENV} && python3 pyxor/main.py

.PHONY: test
test:
	${ACTIVE_ENV} && PYTHONPATH=${PWD}/pyxor pytest -v

.PHONY: clean-up
clean-up:
	rm -rf .venv; find . -name '.pytest_cache' -o -name '__pycache__' |xargs -I '{}' rm -rf {} 

