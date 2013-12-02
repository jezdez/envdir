import optparse
import os
import subprocess
import sys

from .env import Env
from .version import __version__

# must have shell = True on Windows
shellout = sys.platform == 'win32'


class Response(Exception):
    def __init__(self, message='', status=0):
        self.message = message
        self.status = status


class Runner(object):
    envdir_usage = "usage: %prog [--help] [--version] dir child"
    envshell_usage = "usage: %prog [--help] [--version] dir"

    def __init__(self):
        self.parser = optparse.OptionParser(version=__version__)
        self.parser.disable_interspersed_args()
        self.parser.prog = 'envdir'

    def path(self, path):
        real_path = os.path.realpath(os.path.expanduser(path))
        if not os.path.exists(real_path):
            # use 111 error code to adher to envdir's standard
            raise Response("envdir %r does not exist" % path, 111)
        if not os.path.isdir(real_path):
            # use 111 error code to adher to envdir's standard
            raise Response("envdir %r not a directory" % path, 111)
        return real_path

    def open(self, path=None, stacklevel=1):
        if path is None:
            frame = sys._getframe()
            get_parent = lambda frame: frame.f_back
            for _ in range(stacklevel):
                frame = get_parent(frame)
            if frame is not None:
                callerdir = os.path.dirname(frame.f_code.co_filename)
                path = os.path.join(callerdir, 'envdir')
            else:
                # last holdout, assume cwd
                path = 'envdir'
        return Env(self.path(path))

    def shell(self, name, *args):
        self.parser.set_usage(self.envshell_usage)
        self.parser.prog = 'envshell'
        options, args = self.parser.parse_args(list(args))

        if len(args) == 0:
            raise Response("%s\nError: incorrect number of arguments" %
                           (self.parser.get_usage()), 2)

        sys.stdout.write("Launching envshell for %s. "
                         "Type 'exit' or 'Ctrl+D' to return.\n" %
                         self.path(args[0]))
        sys.stdout.flush()
        self.open(args[0], 2)

        shell = os.environ['SHELL']
        try:
            subprocess.check_call([shell],
                                  universal_newlines=True,
                                  shell=shellout,
                                  bufsize=0,
                                  close_fds=True)
        except OSError as err:
            if err.errno == 2:
                raise Response("Unable to find shell %s" % shell, err.errno)
            else:
                raise Response("An error occurred: %s" % err,
                               status=err.errno)

        raise Response()

    def run(self, name, *args):
        self.parser.set_usage(self.envdir_usage)
        self.parser.prog = 'envdir'
        options, args = self.parser.parse_args(list(args))

        if len(args) < 2:
            raise Response("%s\nError: incorrect number of arguments\n" %
                           (self.parser.get_usage()), 2)

        self.open(args[0], 2)

        # the args to call later
        args = args[1:]

        # in case someone passes in -- for any reason to separate the commands
        if args[0] == '--':
            args = args[1:]

        try:
            process = subprocess.Popen(args,
                                       universal_newlines=True,
                                       shell=shellout,
                                       bufsize=0,
                                       close_fds=True)
            process.wait()
        except OSError as err:
            if err.errno == 2:
                raise Response("Unable to find command %s" %
                               args[0], err.errno)
            else:
                raise Response(status=err.errno)
        except KeyboardInterrupt:
            # first send mellow signal
            process.terminate()
            process.poll()
            if process.returncode is None:
                # still running, kill it
                process.kill()

        raise Response(status=process.returncode)
