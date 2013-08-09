import codecs
import os
import re
import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand

here = os.path.abspath(os.path.dirname(__file__))


class CramTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import cram
        sys.exit(cram.main(['tests.t']))


def read(*parts):
    return codecs.open(os.path.join(here, *parts), 'r').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(name="envdir",
      version=find_version('envdir', '__main__.py'),
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Topic :: Software Development :: Build Tools',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.1',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
      ],
      description="A Python port of daemontools' envdir.",
      long_description=read('README.rst') + '\n\n' + read('CHANGES.rst'),
      author='Jannis Leidel',
      author_email='jannis@leidel.info',
      url='http://github.com/jezdez/envdir',
      license='MIT',
      packages=['envdir'],
      entry_points=dict(console_scripts=['envdir=envdir:main',
                                         'envshell=envdir:main']),
      zip_safe=False,
      tests_require=['cram'],
      cmdclass={'test': CramTest})
