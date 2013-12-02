from .__main__ import runner, go
from .env import Env  # noqa
from .version import __version__  # noqa

open = runner.open


# for backward compatibility
def read(path=None):
    return open(path, stacklevel=2)


def run(*args):
    go(runner.run, *args)


def shell(*args):
    go(runner.shell, *args)
