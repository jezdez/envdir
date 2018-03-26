Changelog
---------


1.0.0 (26/03/2018)
^^^^^^^^^^^^^^^^^^

* Drop python 2.6, 3.2 and 3.3

* Add explicit support for python 3.6

* Add support for symlinks

* Improved support for windows

0.7 (08/10/2014)
^^^^^^^^^^^^^^^^

* Use `exec` (`os.execvpe`) to replace the envdir process with the child
  process (fixes #20).

* Change `isenvvar()` to only check for `=` in var names.

0.6.1 (12/23/2013)
^^^^^^^^^^^^^^^^^^

* Fixed handling SIGTERM signals to make sure all children of the forked
  process are killed, too. Thanks to Horst Gutmann for the report and
  help fixing it.

0.6 (12/03/2013)
^^^^^^^^^^^^^^^^

* Rewrote tests with pytest.

* Vastly extended Python API.

* Added Sphinx based docs: https://envdir.readthedocs.io/

* Fixed killing child process when capturing keyboard interrupt.

* Added standalone script based on PEPs 441 and 397, compatible with
  Python Launcher for Windows. See the installation instructions for more
  info.

0.5 (09/22/2013)
^^^^^^^^^^^^^^^^

* Added check if the the provided path is a directory and throw an error if
  not. This adds compatibility to the daemontools' envdir.

* Make sure to convert Nulls (``\0``) to newlines as done so in daemontools'
  envdir.

0.4.1 (08/21/2013)
^^^^^^^^^^^^^^^^^^

* Fixed ``envdir.read()`` to actually work with already existing environment
  variables. Extended docs to test Python use.

0.4 (08/09/2013)
^^^^^^^^^^^^^^^^

* Added ``envshell`` command which launches a subshell using the environment
  as defined in the given envdir. Example::

    $ envshell ~/mysite/envs/prod/
    Launching envshell for /home/jezdez/mysite/envs/prod. Type 'exit' or 'Ctrl+D' to return.
    $ python manage.py runserver
    ..

0.3 (07/30/2013)
^^^^^^^^^^^^^^^^

* Catch ``KeyboardInterrupt`` exceptions to not show a traceback from envdir
  but the repsonse from the called command.

* Allow multiline environment variables. Thanks to Horst Gutmann for the
  suggestion. This is a departure from daemontools' standard which only
  allows the first line of the environment variable file.

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
