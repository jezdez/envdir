envdir
======

.. image:: https://api.travis-ci.org/jezdez/envdir.png
   :alt: Build Status
   :target: https://travis-ci.org/jezdez/envdir

This is a Python port of daemontools_' envdir_.

What?
-----

envdir runs another program with a modified environment according to files
in a specified directory.

So for example, imagine a software you want to run on a server but don't
want to leave certain configuration variables embedded in the program's source
code. A common pattern to solve this problem is to use environment variables
to separate configuration from code.

envdir allows you to set a series of environment variables at once to simplify
maintaing complicated environments, for example in wich you have multiple sets
of those configuration variables depending on the infrastructure you run your
program on (e.g. Windows vs. Linux, Staging vs. Production, Old system vs.
New system etc).

Let's have a look at a typical envdir::

    $ tree mysite_env/
    mysite_env/
    ├── DJANGO_SETTINGS_MODULE
    ├── MYSITE_DEBUG
    ├── MYSITE_DEPLOY_DIR
    ├── MYSITE_SECRET_KEY
    └── PYTHONSTARTUP

    0 directories, 3 files
    $ cat mysite_env/DJANGO_SETTINGS_MODULE
    mysite.settings
    $

As you can see each file has a capitalized name and contains the value of the
environment variable to set when running your program. To use it, simply
prefix the call to your program with envdir::

    $ envdir mysite_env python manage.py runserver

That's it, nothing more and nothing less. The way you structure your envdir
is left to you but can easily match your configuration requirements and
integrate with other configuration systems. envdirs contain just files after
all.

An interesting summary about why it's good to store configuration values in
environment variables can be found on the 12factor_ site.

.. _12factor: http://12factor.net/config

Why?
----

Because envdir small enough that it shouldn't be tied to a bigger
software distribution like daemontools that requires a compiler.

Also, this Python port can easily be used on Windows, not only UNIX systems.

Installation
------------

::

    pip install envdir

or::

    easy_install envdir

Usage
-----

Command line
^^^^^^^^^^^^

Quoting the envdir documentation:

    envdir runs another program with environment modified according to files
    in a specified directory.

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

Python
^^^^^^

To use envdir in a Python file (e.g. Django's ``manage.py``) you can use::

    import envdir
    envdir.read()

envdir will try to find an ``envdir`` directory next to the file you modified.

It's also possible to explicitly pass the path to the envdir::

    import os
    import envdir

    envdir.read('/etc/mysite/envdir')

Feedback
--------

Feel free to open tickets at https://github.com/jezdez/envdir/issues.
Say thanks at https://www.gittip.com/jezdez/.

.. _daemontools: http://cr.yp.to/daemontools.html
.. _envdir: http://cr.yp.to/daemontools/envdir.html

Changelog
---------

0.2.1 (07/11/2013)
^^^^^^^^^^^^^^^^^^

* Fixed ``python -m envdir``
* Extended README to better describe the purpose

0.2 (07/10/2013)
^^^^^^^^^^^^^^^^

* Added ability to use envdir from Python.

0.1 (07/10/2013)
^^^^^^^^^^^^^^^^

* Initial release.
