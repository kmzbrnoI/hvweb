TEMPLATES_DIR=templates
TEMPLATES=$(wildcard $(TEMPLATES_DIR)/*.html)
GENERATORS=$(wildcard scr/*.py)
HVS_DIR=hvs
HVS=$(wildcard $(LOKS_DIR)/*.2lok)

ALL_FILES=index.html
ALL=$(patsubst %,build/%,$(ALL_FILES))

all: $(ALL)

build/index.html: $(TEMPLATES) $(GENERATORS) $(HVS)
	./scr/hvlist_gen.py -o $@ -l $(HVS_DIR)

clean:
	rm -r $(ALL)

check:
	flake8 $(GENERATORS)
	mypy --strict $(GENERATORS)

.PHONY: all clean check
