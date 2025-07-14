.. include:: global.rst.inc
.. highlight:: bash
.. _installation:

Installation
============

To install Borg-Import, you need `Python 3`_ and `pip`_ installed. You can then either `download borg-import directly
<https://github.com/borgbackup/borg-import/archive/master.zip>`_
or clone it from the `githubrepo`_.
Extract the downloaded .zip if necessary.
Open a terminal in the borg-import directory and execute the following to install the program via pip:
:code:`pip install --user -e .`

If you have */home/user/.local/bin/* in your ``PATH`` variable, you can then start using Borg-Import.
Otherwise, you will need to add *.local/bin/* to your ``PATH``.

For Developers
--------------

If you're planning to contribute to Borg-Import, you should set up the development environment:

1. Install development dependencies:

   :code:`pip install -r requirements.d/development.txt`

2. Set up pre-commit hooks:

   :code:`pre-commit install`

This will automatically run code formatting (black) and linting (flake8) checks before each commit.
The pre-commit hooks will ensure your code follows the project's style guidelines.
