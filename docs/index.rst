.. include:: ../README.rst

How?
----

Installation
^^^^^^^^^^^^

.. code-block:: console


    $ pip install envdir

or:

.. code-block:: console

    $ easy_install envdir

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

.. note::

    This Python port behaves different for multi line environment variables.
    It will not only read the first line of the file but the whole file. Take
    care with big files!

Alternatively you can also use the ``python -m envdir`` form to call envdir.

Feedback
--------

Feel free to open tickets at https://github.com/jezdez/envdir/issues.
Say thanks at https://www.gittip.com/jezdez/.

More documentation
------------------

.. toctree::
   :maxdepth: 3

   Python API -- Using envdir from Python scripts <api>
   envshell -- subshell with sticky envdir <shell>
   changelog
