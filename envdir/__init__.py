import sys
from .__main__ import envdir, __version__  # noop

read = envdir.read


def main():
    envdir.main(sys.argv[1:])
