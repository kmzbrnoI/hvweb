TEMPLATES_DIR=templates
TEMPLATES=$(wildcard $(TEMPLATES_DIR)/*.html)
GENERATORS=$(wildcard scr/*.py)
HVS_DIR=hvs
HVS=$(wildcard $(LOKS_DIR)/*.2lok)

ALL_FILES=hvs.html
ALL=$(patsubst %,build/%,$(ALL_FILES))

SHELL := /bin/bash

all: $(ALL)

build/hvs.html: $(TEMPLATES) $(GENERATORS) $(HVS_DIR)
	source hvwww-venv/bin/activate && ./scr/hvlist_gen.py $(HVS_DIR) -o $@

clean:
	rm -r $(ALL)

check:
	flake8 $(GENERATORS)
	mypy --strict $(GENERATORS)

.PHONY: all clean check
