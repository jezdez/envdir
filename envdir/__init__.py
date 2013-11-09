from .__main__ import runner, go
from .env import Env  # noqa
from .version import __version__  # noqa

read = runner.read
open = runner.open


def run(*args):
    go(runner.run, *args)


def shell(*args):
    go(runner.shell, *args)
