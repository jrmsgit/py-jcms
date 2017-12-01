PYTHON ?= python3
PIP ?= pip3

.PHONY: default
default: build

.PHONY: clean
clean:
	@rm -rf htmlcov build
	@rm -f jcmstest.profile .coverage
	@find . -type d -name __pycache__ | xargs rm -rf
	@find . -type f -name '*.c' | xargs rm -f
	@find . -type f -name '*.so' | xargs rm -f

.PHONY: distclean
distclean: clean
	@rm -rf dist jcms.egg-info
	@rm -f db.sqlite3

.PHONY: coverage
coverage:
	@$(PYTHON) -m coverage run jcmstest.py
	@$(PYTHON) -m coverage report

.PHONY: htmlcov
htmlcov: coverage
	@$(PYTHON) -m coverage html

.PHONY: profile
profile:
	@$(PYTHON) jcmsprof.py

.PHONY: lang-extract
lang-extract:
	@$(PYTHON) manage.py makemessages --settings=jcms.settings

.PHONY: lang-compile
lang-compile:
	@$(PYTHON) manage.py compilemessages --settings=jcms.settings

.PHONY: lang
lang: lang-extract lang-compile

.PHONY: buildext
buildext:
	@$(PYTHON) setup.py build_ext

.PHONY: build
build:
	@$(PYTHON) setup.py build

.PHONY: dist
dist:
	$(PYTHON) setup.py -q bdist_wheel

.PHONY: test
test:
	@$(PYTHON) jcmstest.py

.PHONY: install
install:
	@$(PYTHON) setup.py install --force

.PHONY: uninstall
uninstall:
	@$(PIP) uninstall -y jcms
