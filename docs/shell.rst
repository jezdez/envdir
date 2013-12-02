envshell
========

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
