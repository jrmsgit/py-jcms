PYTHON ?= python3
PIP ?= pip3

.PHONY: default
default: build

.PHONY: clean
clean:
	@rm -rf htmlcov build
	@rm -f jcmstest.profile .coverage

.PHONY: distclean
distclean: clean
	@rm -rf dist jcms.egg-info
	@find . -type d -name __pycache__ | xargs rm -rf
	@rm -f db.sqlite3

.PHONY: coverage
coverage: clean
	@$(PYTHON) -m coverage run jcmstest.py
	@$(PYTHON) -m coverage report

.PHONY: htmlcov
htmlcov: coverage
	@$(PYTHON) -m coverage html

.PHONY: profile
profile: clean
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

.PHONY: test
test: clean
	@$(PYTHON) jcmstest.py

.PHONY: install
install: build
	@$(PYTHON) setup.py install --force --skip-build

.PHONY: uninstall
uninstall:
	@$(PIP) uninstall -y jcms
