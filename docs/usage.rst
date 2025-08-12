.. include:: global.rst.inc
.. highlight:: none
.. _detailed_usage:

Usage
=====

``borg-import`` consists of a number of commands, one for each
backup system supported. Each accepts a number of arguments and
options. The following sections describe each in detail.

General
-------

Note that borg-import will prompt for your repository passphrase,
which pauses the import until you enter it. To let borg-import
continue automatically, set the environment variable
BORG_PASSPHRASE:

``BORG_PASSPHRASE=xxxxxx borg-import ...``

.. _rsnapshot:

borg-import rsnapshot
---------------------

.. generate-usage:: rsnapshot

.. _borg:

borg-import borg
----------------

.. generate-usage:: borg
