.. include:: global.rst.inc
.. highlight:: bash
.. _installation:

Installation
============

To install Borg-Import, you need `Python 3`_ and `pip`_ installed. You can then either `download borg-import directly
<https://github.com/borgbackup/borg-import/archive/master.zip>`_
or clone it from the `repo`_.
Extract the downloaded .zip if necessary.
Open a terminal in the borg-import directory and execute the following to install the program via pip:
:code:`pip install --user -e .`

If you have */home/user/.local/bin/* in your ``PATH`` variable, you can then start using Borg-Import.
Otherwise, you will need to add *.local/bin/* to your ``PATH`` via adding ``export PATH=$PATH:/home/user/.local/bin/``
to your .profile file if you are using a POSIX-based shell. Don't forget to :code:`source ~/.profile` when you're done.
