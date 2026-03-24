.. include:: global.rst.inc
.. highlight:: bash
.. _quickstart:

Quickstart
==========

This guide will get you started with borg-import.

Getting started quickly
-----------------------

If you just want to try borg-import with minimal setup:

::

    git clone https://github.com/borgbackup/borg-import.git
    cd borg-import
    python -m venv env
    source env/bin/activate
    pip install -e .
    borg-import --help