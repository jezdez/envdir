envdir
======

.. image:: https://api.travis-ci.org/jezdez/envdir.png
   :alt: Build Status
   :target: https://travis-ci.org/jezdez/envdir

This is a Python port of daemontools_' envdir_.

Why?
----

Because it's small enough that it shouldn't be tied to a bigger
software distribution like daemontools. Also, this Python port
can easily be used on Windows, not only UNIX systems.

Installation
------------

::

    pip install envdir

or::

    easy_install envdir

Usage
-----

Quoting the envdir documentation:

    envdir runs another program with environment modified according to files in a specified directory.
    Interface::

        envdir d child

    ``d`` is a single argument. ``child`` consists of one or more arguments.

    envdir sets various environment variables as specified by files in the
    directory named ``d``. It then runs ``child``.

    If ``d`` contains a file named ``s`` whose first line is ``t``, envdir
    removes an environment variable named ``s`` if one exists, and then adds
    an environment variable named ``s`` with value ``t``. The name ``s`` must
    not contain ``=``. Spaces and tabs at the end of ``t`` are removed.
    Nulls in ``t`` are changed to newlines in the environment variable.

    If the file ``s`` is completely empty (0 bytes long), envdir removes an
    environment variable named ``s`` if one exists, without adding a new
    variable.

    envdir exits ``111`` if it has trouble reading ``d``, if it runs out of
    memory for environment variables, or if it cannot run child. Otherwise
    its exit code is the same as that of child.

Alternatively you can also use the ``python -m envdir`` form to call envdir.

Feedback
--------

Feel free to open tickets at https://github.com/jezdez/envdir/issues.
Say thanks at https://www.gittip.com/jezdez/.

.. _daemontools: http://cr.yp.to/daemontools.html
.. _envdir: http://cr.yp.to/daemontools/envdir.html

Changelog
---------

0.1 (07/10/2013)
^^^^^^^^^^^^^^^^

* Initial release.
