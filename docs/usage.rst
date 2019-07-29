.. include:: global.rst.inc
.. highlight:: none
.. _detailed_usage:

Usage
=====

``borg-import`` consists of a number of commands, one for each
backup system supported. Each accepts a number of arguments and
options. The following sections will describe each in detail.

General
-------

Note that |project_name| will ask you for your repo's passphrase
which blocks the import until you enter it. To let |project_name|
continue automatically, you can pass the environment variable
*BORG_PASSPHRASE*:
:code:`BORG_PASSPHRASE=xxxxxx borg-import ....`

.. _rsnapshot:

borg-import rsnapshot
---------------------

.. generate-usage:: rsnapshot
