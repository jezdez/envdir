import sys

from .runner import Runner, Response

runner = Runner()


def go(caller, *args):
    if not args:
        args = sys.argv
    try:
        caller(args[0], *args[1:])
    except Response as response:
        if response.message:
            sys.stderr.write(response.message)
        sys.exit(response.status or 0)
    else:
        sys.exit(0)


if __name__ == '__main__':
    go(runner.run)  # pragma: no cover
