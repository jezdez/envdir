import ast
import codecs
import os

from setuptools import setup


here = os.path.abspath(os.path.dirname(__file__))


class VersionFinder(ast.NodeVisitor):
    def __init__(self):
        self.version = None

    def visit_Assign(self, node):
        if node.targets[0].id == '__version__':
            self.version = node.value.s


def read(*parts):
    return codecs.open(os.path.join(here, *parts), 'r').read()


def find_version(*parts):
    finder = VersionFinder()
    finder.visit(ast.parse(read(*parts)))
    return finder.version


setup(name="envdir",
      version=find_version('envdir', 'version.py'),
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
      long_description=(read('README.rst') +
                        '\n\n' +
                        read(os.path.join('docs', 'changelog.rst'))),
      author='Jannis Leidel',
      author_email='jannis@leidel.info',
      url='http://envdir.readthedocs.org/',
      license='MIT',
      packages=['envdir'],
      entry_points=dict(console_scripts=['envdir=envdir:run',
                                         'envshell=envdir:shell']),
      zip_safe=False)
