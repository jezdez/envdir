Changelog
---------

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
