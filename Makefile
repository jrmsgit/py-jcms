PYTHON ?= python3
PIP ?= pip3

.PHONY: default
default: build

.PHONY: clean
clean:
	@rm -rf htmlcov build
	@rm -f jcmstest.profile .coverage
	@rm -f *.c *.html *.so

.PHONY: distclean
distclean: clean
	@rm -rf dist jcms.egg-info
	@find . -type d -name __pycache__ | xargs rm -rf
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

.PHONY: build
build:
	@$(PYTHON) setup.py build

.PHONY: dist
dist:
	@$(PYTHON) setup.py sdist
	@$(PYTHON) setup.py bdist_egg --exclude-source-files

.PHONY: test
test:
	@$(PYTHON) jcmstest.py

.PHONY: install
install:
	@$(PYTHON) setup.py install --force

.PHONY: uninstall
uninstall:
	@$(PIP) uninstall -y jcms
