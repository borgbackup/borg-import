.. include:: global.rst.inc
.. highlight:: none
.. _faq:

Frequently Asked Questions
==========================

My old backup program isn't officially supported. Can I still use borg-import?
------------------------------------------------------------------------------

It is likely that your old backup program uses an
rsync-with-hard-links mechanism that works with
borg-import's ``rsynchl`` mode. If you're unsure, try to find
out or ask how the program organizes its backups.
Support for `Back In Time`_ was discovered simply by
trying it.
