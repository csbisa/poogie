SOURCES=$(shell find . -type f -name '*.ksy' | sed 's/^.\///')
KSY_OBJS=$(patsubst %.ksy, generated/%.py, $(SOURCES))

generated/%.py: %.ksy
	@echo "GEN	$@"
	@mkdir -p generated/$(dir $<)
	@touch generated/$(dir $<)/__init__.py
	@ksc -t python --outdir generated/$(dir $<) $<

types: $(KSY_OBJS)

all: types
