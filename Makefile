.PHONY: clean clean-test clean-pyc clean-build docs help
.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr '*.so'
	rm -fr .pytype
	rm -fr .ruff_cache
	rm -fr build/
	rm -fr setup.py
	rm -fr dist/
	rm -fr .eggs/
	rm -fr cmake-build-debug
	rm -fr inst/_filet/cmake-build-debug
	find . -path './docker' -prune -o -name '*.egg-info' -exec rm -fr {} +
	find . -path './docker' -prune -o -name '*.egg' -exec rm -fr {} +

clean-pyc: ## remove Python file artifacts
	find . -path './docker' -prune -o -name '*.pyc' -exec rm -fr {} +
	find . -path './docker' -prune -o -name '*.pyo' -exec rm -fr {} +
	find . -path './docker' -prune -o -name '*'*~'' -exec rm -fr {} +
	find . -path './docker' -prune -o -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

lint: ## check style with flake8
	flake8 filet tests

test: ## run tests quickly with the default Python
	pytest

test-dev:
	TEST_PROFILE=dev; pytest

test-mypy:
	mypy filet tests docs/conf.py

test-xdoctest:
	python -m xdoctest filet all

test-pytype:
	pytype --disable=import-error filet tests docs/conf.py

test-typeguard:
	 pytest --typeguard-packages=filet

test-types: test-mypy test-xdoctest test-typeguard test-pytype

test-cpp:
	$(MAKE) -C lib all
	rm -rf cmake-build-debug
	cmake -DCMAKE_BUILD_TYPE=Debug -DCMAKE_MAKE_PROGRAM=ninja -G Ninja -S . -B cmake-build-debug
	cmake --build cmake-build-debug --target tests -j 10
	cmake-build-debug/tests

test-all: ## run tests on every Python version with tox
	nox

coverage: ## check code coverage quickly with the default Python
	coverage run --source filet -m pytest
	coverage report -m
	coverage html -d docs/coverage
	coverage-badge -o docs/coverage/coverage.svg

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/filet.rst
	rm -f docs/modules.rst
	rm -rf docs/_generated
	rm -rf docs/_build
	rm -rf docs/coverage
	rm -f docs/filet*.rst
	$(MAKE) -C docs clean
	sphinx-apidoc -o docs/ filet
	$(MAKE) coverage
	mv docs/coverage/index.html docs/coverage/_coverage.html
	$(MAKE) -C docs SPHINXOPTS=-v html
	mv docs/_build/html/_coverage.html docs/_build/html/coverage.html
	$(BROWSER) docs/_build/html/index.html

servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

bump-patch:
	git pull
	python docs/scripts/bump_module.py "patch"

bump-minor:
	git pull
	python docs/scripts/bump_module.py "minor"

bump-major:
	git pull
	python docs/scripts/bump_module.py "major"

bump: bump-patch # default

pr: bump
	@if [ -n "$$(git status --porcelain --ignore-submodules)" ]; then \
		echo "You have unstaged/committed changes. Please commit or stash them first."; \
		exit 1; \
	fi && \
	if [ -n "$$(git log @{u}..)" ]; then \
		echo "There are commits that haven't been pushed yet. Please push your changes first."; \
		exit 1; \
	fi && \
	BRANCH_NAME=$(shell git branch --show-current) && \
	glab mr create --source-branch $$BRANCH_NAME --target-branch main --title "PR $$BRANCH_NAME - $$(poetry version -s)" --description "$(filter-out $@,$(MAKECMDGOALS))"


pr-merge-if-ready: bump
	@if [ -n "$$(git status --porcelain --ignore-submodules)" ]; then \
		echo "You have unstaged/committed changes. Please commit or stash them first."; \
		exit 1; \
	fi
	@if [ -n "$$(git log @{u}..)" ]; then \
		echo "There are commits that haven't been pushed yet. Please push your changes first."; \
		exit 1; \
	fi
	@BRANCH_NAME=$(shell git branch --show-current); \
	MR_LISTING=$$(glab mr list --source-branch $$BRANCH_NAME); \
	PR_ID=$$(echo "$$MR_LISTING" | grep -Eo '!([0-9]+)' | head -n 1 | tr -d '!'); \
	if [ -n "$$PR_ID" ]; then \
		if $(MAKE) pr-status; then \
			glab mr merge $$PR_ID; \
		else \
			echo "PR is not ready to be merged due to pending or failing checks."; \
		fi \
	else \
		echo "No MR found for source branch $$BRANCH_NAME"; \
	fi

release: pr-merge-if-ready
	@# Fetch the latest status of the main branch from the remote
	git fetch origin main:main && \
	OPEN_PRS_COUNT=$$(glab mr list --target-branch main | wc -l) && \
   	if [ "$$OPEN_PRS_COUNT" -ne 0 ]; then \
   		echo "There are open merge requests targeting the main branch. Resolve them before creating a tag."; \
   		exit 1; \
   	fi && \
	VERSION=$$(poetry version -s) && \
	echo "Detected version: $$VERSION" && \
	if git rev-parse "$$VERSION" >/dev/null 2>&1; then \
		echo "Tag $$VERSION already exists."; \
	else \
		echo "Creating new tag $$VERSION on the remote main branch." && \
		git tag "$$VERSION" origin/main && \
		git push origin "$$VERSION" && \
		echo "Tag $$VERSION has been created on the remote main branch and pushed. Create the release manually in GitLab."; \
	fi

clean-docker:
	rm docker/conf/core-site.xml -rf
	rm docker/conf/hive-site.xml -rf
	rm docker/conf/iceberg-site.xml -rf
	rm docker/etc/catalog/hive.properties -rf
	rm docker/etc/catalog/iceberg.properties -rf

stop-docker:
	cd docker && docker compose down

start-local: clean-docker  # run docker environment
	export TEST_PROFILE=default
	cd docker && docker compose up -d

start-dev: clean-docker  # run docker environment
	export TEST_PROFILE=dev
	cd docker && docker compose -f docker-compose-dev.yml up -d

publish: dist ## package and upload a release
	poetry publish

dist: clean-build clean-pyc ## builds source and wheel package
	poetry build

install-debug:
	export DEBUG_MODE=true
	poetry install --verbose

install: clean-build clean-pyc ## install the package to the active Python's site-packages
	poetry install --verbose

all: install dist
	c++ --version  # default compile method (not needed but here for the IDE)
