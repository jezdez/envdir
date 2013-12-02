Python API
==========

.. function:: envdir.open([path])

To use an envdir in a Python file (e.g. Django's ``manage.py``) simply call
the ``open`` function of the envdir module:

.. code-block:: python

    import envdir
    envdir.open()

envdir will try to find an :file:`envdir` directory next to the file you modified.

It's also possible to explicitly pass the path to the envdir:

.. code-block:: python

    import envdir

    envdir.open('/home/jezdez/mysite/envs/prod')

Calling ``open`` will automatically apply all environment variables to the
current instance of ``os.environ``.

If you want to implement more advanced access to envdirs there is also an
own dict-like :class:`~envdir.Env` object to work with. The above example
could also be written like this:

.. code-block:: python

    import envdir

    env = envdir.open('/home/jezdez/mysite/envs/prod')

The returned :class:`~envdir.Env` instance has a dict-like interface but also
features a :meth:`~envdir.Env.clear` method to reset the current instance of
:data:`os.environ` to the value it had before the envdir was opened:

.. code-block:: python

    import envdir

    env = envdir.open('/home/jezdez/mysite/envs/prod')

    # do something

    env.clear()

Since calling the clear method should be done in a transparent manner
you can also use it as a context manager:

.. code-block:: python

    import envdir

    with envdir.open('/home/jezdez/mysite/envs/prod') as env:
        # do something

Outside the context manager block the environ is reset back automatically.

To access and write values you can also use the dict-like interface:

.. code-block:: python

    import envdir

    with envdir.open() as env:
        env['DATABASE_URL'] = 'sqlite://:memory:'
        assert 'DATABASE_URL' in env
        assert env.items() == [('DATABASE_URL', 'sqlite://:memory:')]

.. note::

    Additions to the envdir done inside the context manager block are
    persisted to disk and will be available the next time your open the
    envdir again.

Of course you can also directly interact with :class:`~envdir.Env` instances,
e.g.:

.. code-block:: python

    import envdir

    with envdir.Env('/home/jezdez/mysite/envs/prod') as env:
        # do something here

The difference between instantiating an :class:`~envdir.Env` yourself to
using :func:`envdir.open` is that you'll lose the automatic discovery of
the ``envdir`` directory.

See the API docs below for a full list of methods available in the
:class:`~envdir.Env` object.

.. autoclass:: envdir.Env
   :members:
   :undoc-members:
   :special-members:
   :inherited-members:
