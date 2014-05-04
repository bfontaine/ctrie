SRC=ctrie

COVERFILE:=.coverage
COVERAGE_REPORT:=report -m

PY_VERSION:=$(subst ., ,$(shell python --version 2>&1 | cut -d' ' -f2))
PY_VERSION_MAJOR:=$(word 1,$(PY_VERSION))
PY_VERSION_MINOR:=$(word 2,$(PY_VERSION))
PY_VERSION_SHORT:=$(PY_VERSION_MAJOR).$(PY_VERSION_MINOR)

ifdef TRAVIS_PYTHON_VERSION
PY_VERSION_SHORT:=$(TRAVIS_PYTHON_VERSION)
endif

.PHONY: check check-versions stylecheck covercheck docs

default: deps check-versions

deps:
	pip install -qr requirements.txt
ifeq ($(PY_VERSION_SHORT),2.6)
	pip install -q unittest2
endif
ifneq ($(PY_VERSION_SHORT),3.3)
ifneq ($(PY_VERSION_SHORT),3.4)
	pip install -q wsgiref==0.1.2
endif
endif

check:
	python tests/test.py

check-versions:
	tox

stylecheck:
	pep8 $(SRC)

covercheck:
	coverage run --source=$(SRC) tests/test.py
	coverage $(COVERAGE_REPORT)

clean:
	find . -name '*~' -delete
	rm -f $(COVERFILE)
	make -C docs clean

publish: stylecheck check-versions
	cp README.rst README
	python setup.py sdist upload
	rm -f README

docs:
	make -C docs html
