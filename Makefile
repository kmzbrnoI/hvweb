GENERATORS=$(wildcard scr/*.py)

ALL_FILES=hvs.html users.html
ALL=$(patsubst %,build/%,$(ALL_FILES))

SHELL := /bin/bash

all: $(ALL)

build/hvs.html: templates/hv.html templates/hvs.html scr/hvlist_gen.py hvs
	source hvwww-venv/bin/activate && ./scr/hvlist_gen.py hvs -o $@

build/users.html: templates/users.html scr/users_gen.py data
	source hvwww-venv/bin/activate && ./scr/users_gen.py data/users.ini -o $@

clean:
	rm -r $(ALL)

check:
	flake8 $(GENERATORS)
	mypy --strict $(GENERATORS)

.PHONY: all clean check
