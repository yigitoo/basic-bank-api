all: default

default: run

run:
	./scripts/run.sh

install: setup

setup:
	./scripts/setup.sh

.PHONY: all default run install setup
