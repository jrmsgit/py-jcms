PIP ?= pip3
PYTHON ?= python3
VENVDIR ?= /var/opt/jcms.venv
VENVPIP = $(VENVDIR)/bin/$(PIP)
VENVPYTHON = $(VENVDIR)/bin/$(PYTHON)

.PHONY: default
default: build

.PHONY: clean
clean:
	@find . -type d -name __pycache__ | xargs rm -vrf
	@rm -vrf htmlcov build
	@rm -vf jcmstest.profile .coverage
	@rm -vf */*.html */*.c */*.so

.PHONY: distclean
distclean: clean
	@rm -vrf dist jcms.egg-info
	@rm -vf db.sqlite3

.PHONY: coverage
coverage:
	@$(PYTHON) -m coverage run jcmstest.py
	@$(PYTHON) -m coverage report

.PHONY: htmlcov
htmlcov:
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
	@$(PYTHON) setup.py build_ext --inplace

.PHONY: build
build: buildext
	@$(PYTHON) setup.py build

.PHONY: dist
dist:
	$(PYTHON) setup.py sdist
	$(PYTHON) setup.py bdist_wheel

.PHONY: check
check:
	@$(PYTHON) setup.py check
	@$(PYTHON) manage.py check

.PHONY: test
test:
	@$(PYTHON) jcmstest.py

.PHONY: install
install:
	@$(PYTHON) setup.py install --force

.PHONY: uninstall
uninstall:
	@$(PIP) uninstall -y jcms

.PHONY: venv
venv:
	@$(PYTHON) -m venv --symlinks $(VENVDIR)
	@$(VENVPIP) install -U --upgrade-strategy only-if-needed -r requirements.txt
	@echo "$(VENVDIR) venv created"

.PHONY: venv-remove
venv-remove:
	rm -rf $(VENVDIR)

.PHONY: venv-info
venv-info:
	@echo $(VENVDIR)
	@$(VENVPYTHON) --version
	@$(VENVPIP) --version
	@$(VENVPIP) freeze | sort -u
