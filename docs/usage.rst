Usage
=====

Command line
------------

From the original envdir_ documentation:

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

Isolated shell
--------------

envdir also includes an optional CLI tool called ``envshell`` which launches
a subshell using the given directory. It basically allows you to make a set
of environment variable stick to your current shell session if you happen to
use envdir a lot outside of simple script use.

For example:

.. code-block:: console

    $ envshell ~/mysite/envs/prod/
    Launching envshell for /home/jezdez/mysite/envs/prod. Type 'exit' or 'Ctrl+D' to return.
    $ python manage.py runserver
    ..

To leave the subshell, simply use the ``exit`` command or press ``Ctrl+D``.

.. _envdir: http://cr.yp.to/daemontools/envdir.html


Setup an empty environment variable
-----------------------------------

Use an empty line to setup an empty environment variable (in contrast to an
empty file, which would unset the environment variable):

.. code-block:: console

   $ echo > envdir/EMPTY_ENV
   $ envdir envdir env | grep EMPTY_ENV
   EMPTY_ENV=
