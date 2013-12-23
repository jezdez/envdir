Installation
============

As Python package
-----------------

.. highlight:: console

::

    $ pip install envdir

or:

::

    $ easy_install envdir

As standalone script
--------------------

Alternatively you can also download a standalone executable that follows
Python's `PEP 441`_ and works with the Python Launcher for Windows (`PEP 397`_).
Simply install the launcher from its site_ (downloads_) and you're ready to
follow the rest of the instructions below.

Windows
^^^^^^^

.. note::

    The Python Launcher for Windows also provides other useful features like
    being able to correctly launch Python when double clicking a file with
    the .py file extension, a ``py`` command line tool to easily launch the
    interactive Python shell when you're working on the command line. See
    the `Python Launcher for Windows documentation`_ for more infos.

Next step is downloading the actual standalone script. On Windows this entails
using your web browser to download the following URL:

.. parsed-literal::

    \https://github.com/jezdez/envdir/releases/download/|release|/envdir-|release|.pyz

Or simply run this on the command line to trigger the download with your
default web browser:

.. parsed-literal::

    C:\\Windows\Explorer.exe \https://github.com/jezdez/envdir/releases/download/|release|/envdir-|release|.pyz

Then -- from the location you downloaded the file to -- run the envdir script
like you would any other script:

.. parsed-literal::

    C:\\Users\\jezdez\\Desktop>.\\envdir-|release|.pyz ..

Linux, Mac OS, others
^^^^^^^^^^^^^^^^^^^^^

On Linux, Mac OS and other platforms with a shell like bash simply download
the standalone file from Github:

.. parsed-literal::

    $ curl -LO \https://github.com/jezdez/envdir/releases/download/|release|/envdir-|release|.pyz

and then run the file like you would do when running the script installed by
the envdir package (see above):

.. parsed-literal::

    $ ./envdir-|release|.pyz ..

.. _`PEP 441`: http://www.python.org/dev/peps/pep-0441/
.. _`PEP 397`: http://www.python.org/dev/peps/pep-0397/
.. _site: https://bitbucket.org/pypa/pylauncher/
.. _downloads: https://bitbucket.org/pypa/pylauncher/downloads
.. _`Python Launcher for Windows documentation`: https://bitbucket.org/pypa/pylauncher/src/tip/Doc/launcher.rst
