.. include:: global.rst.inc
.. highlight:: none
.. _faq:

Frequently asked questions
==========================

My old backup program isn't officially supported. Can I still use borg-import?
------------------------------------------------------------------------------

Chances are good that your old backup program is using some
kind of rsync+hardlinks mechanisms that will work with
|project_name|'s ``rsynchl`` mode. If you're unsure, try to find
out or ask how the program is organizing its backups.
Support for the software *Back In Time*_ was discovered by
simply trying it out.
