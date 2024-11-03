==================
Avro Schema Generator - Tool for generating Avro schema from JSON
==================

.. warning::

   This tool is no longer maintained and is published solely for reference and logic reuse purposes.
Installation
============

.. code:: bash

   pip install filet

Prerequisites
~~~~~~~~~~~~~

-  Python 3.9+
-  poetry
-  glab (optional) For release management (commands)
- cmake (optional) For cpp development
- make (optional) For makefiles
- ninja (optional) For cpp development
- pre-commit (optional) For pre-commit hooks

Commands
~~~~~~~~~~~~

Install the package using makefiles:

.. code::

   make install

Build dist using makefiles:

.. code::

   make dist

Run tests (pytest) using makefiles:

.. code::

   make test


Run cpp tests (catch2) using makefiles:

.. code::

   make test-cpp


Run all tests using makefiles:

.. code::

   make test-all

Run lint using makefiles:

.. code::

   make lint

Create dev venv:

.. code::

   python -m venv .venv
   source .venv/bin/activate
   pip install poetry

Bump Version:

.. code::

   make bump-<major|minor|patch>

Install pre-commit:

.. code::

   pre-commit install

Update pre-commit:

.. code::

   pre-commit update -a

Run pre-commit:

.. code::

   pre-commit run -a


Manage Dependencies:
~~~~~~~~~~~~~~~~~~~~~

Add new dependency:

.. code::

   poetry add <dependency>

Update dependencies in the pyproject.toml file:

Prod-dependencies: dependencies in -> `[tool.poetry.dependencies]` Section
Dev-dependencies: dependencies in -> `[tool.poetry.dev-dependencies]` Section

Update lock file:

.. code::

   poetry update
