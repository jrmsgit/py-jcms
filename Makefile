PYTHON ?= python3

.PHONY: default
default:
	@echo 'nothing to do...'

.PHONY: clean
clean:
	@rm -rf htmlcov
	@rm -f jcmstest.profile .coverage

.PHONY: distclean
distclean:
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
