GENERATORS=$(wildcard scr/*.py)

ALL_FILES= \
	dukelska-h0/hvs.html dukelska-h0/users.html \
	mendelu-tt/hvs.html mendelu-tt/users.html

ALL=$(patsubst %,build/%,$(ALL_FILES))

SHELL := /bin/bash

all: $(ALL)

build/dukelska-h0/hvs.html: templates/hv.html templates/dukelska_h0_hvs.html scr/hvlist_gen.py serverRepos/dukelska-h0/lok
	source hvwww-venv/bin/activate && ./scr/hvlist_gen.py templates/dukelska_h0_hvs.html serverRepos/dukelska-h0/lok -o $@

build/mendelu-tt/hvs.html: templates/hv.html templates/mendelu_tt_hvs.html scr/hvlist_gen.py serverRepos/mendelu-tt/lok
	source hvwww-venv/bin/activate && ./scr/hvlist_gen.py templates/mendelu_tt_hvs.html serverRepos/mendelu-tt/lok -o $@

build/dukelska-h0/users.html: templates/dukelska_h0_users.html scr/users_gen.py serverRepos/dukelska-h0/data/users.ini
	source hvwww-venv/bin/activate && ./scr/users_gen.py templates/dukelska_h0_users.html serverRepos/dukelska-h0/data/users.ini -o $@

build/mendelu-tt/users.html: templates/mendelu_tt_users.html scr/users_gen.py serverRepos/mendelu-tt/data/users.ini
	source hvwww-venv/bin/activate && ./scr/users_gen.py templates/mendelu_tt_users.html serverRepos/mendelu-tt/data/users.ini -o $@

clean:
	rm -r $(ALL)

check:
	flake8 $(GENERATORS)
	mypy --strict $(GENERATORS)

init:  # Initialize serverRepos in clean repository
	mkdir serverRepos
	git clone git@github.com:kmzbrnoI/hJOPserverConfig serverRepos/dukelska-h0
	cd serverRepos/dukelska-h0 && git checkout mosilana-h0
	git clone git@github.com:kmzbrnoI/hJOPserverConfig serverRepos/mendelu-tt
	cd serverRepos/mendelu-tt && git checkout mendelu-tt

.PHONY: all clean check init
