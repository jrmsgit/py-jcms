PYTHON ?= python3
PIP ?= pip3

.PHONY: default
default: build

.PHONY: clean
clean:
	@rm -rf htmlcov
	@rm -f jcmstest.profile .coverage

.PHONY: distclean
distclean: clean
	@rm -rf dist jcms.egg-info build
	@find . -type d -name __pycache__ | xargs rm -rf
	@rm -f db.sqlite3

.PHONY: coverage
coverage:
	@$(PYTHON) -m coverage run jcmstest.py
	@$(PYTHON) -m coverage report

.PHONY: htmlcov
htmlcov: coverage
	@$(PYTHON) -m coverage html

.PHONY: test
test:
	@$(PYTHON) jcmstest.py

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

.PHONY: build
build:
	@$(PYTHON) setup.py build

.PHONY: dist
dist: build
	@$(PYTHON) setup.py sdist --formats=xztar

.PHONY: install
install: dist
	@$(PYTHON) setup.py install --force --skip-build

.PHONY: uninstall
uninstall:
	@$(PIP) uninstall -y jcms