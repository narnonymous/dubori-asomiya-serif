.PHONY: all build test clean

SOURCES := $(wildcard sources/*.designspace sources/*.ufo sources/*.py)
CONFIG := sources/config.yaml

all: build

build:
	python3 src/build_font_family.py

test:
	fontbakery check-googlefonts fonts/ttf/*.ttf fonts/variable/*.ttf

clean:
	rm -rf build/
