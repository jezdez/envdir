import glob
import optparse
import os
import subprocess
import sys

__version__ = '0.4.1'

# must have shell = True on Windows
shellout = sys.platform == 'win32'


class EnvOptionParser(optparse.OptionParser):

    def error(self, msg, no=2):
        """error(msg : string, [no : int])

        Print a usage message incorporating 'msg' to stderr and exit.
        Takes an optional error number.
        """
        self.print_usage(sys.stderr)
        self.exit(no, "%s: error: %s\n" % (self.get_prog_name(), msg))


class Runner(object):
    envdir_usage = "usage: %prog [--help] [--version] dir child"
    envshell_usage = "usage: %prog [--help] [--version] dir"

    def __init__(self):
        self.parser = EnvOptionParser(version=__version__)
        self.parser.disable_interspersed_args()

    @staticmethod
    def is_envvar(name):
        root, name = os.path.split(name)
        return (name == name.upper() and
                not name.startswith('_') and
                not '=' in name)

    def environ(self, path):
        env_paths = filter(self.is_envvar, glob.glob(os.path.join(path, '*')))
        for env_path in env_paths:
            with open(env_path, 'r') as env_file:
                root, name = os.path.split(env_path)
                value = env_file.read().strip()
                yield name, value

    def path(self, path):
        real_path = os.path.realpath(os.path.expanduser(path))
        if not os.path.exists(real_path):
            # use 111 error code to adher to envdir's standard
            self.parser.error("envdir %r does not exist" % path, no=111)
        return real_path

    def read(self, path=None):
        if path is None:
            frame = sys._getframe()
            callerdir = os.path.dirname(frame.f_back.f_code.co_filename)
            path = os.path.join(callerdir, 'envdir')

        for name, value in self.environ(self.path(path)):
            if value:
                os.environ[name] = value
            elif name in os.environ:
                del os.environ[name]

    def shell(self, args):
        self.parser.set_usage(self.envshell_usage)
        self.parser.prog = 'envshell'

        if len(args) == 0:
            self.parser.error("incorrect number of arguments")
            self.parser.print_usage()

        sys.stdout.write("Launching envshell for %s. "
                         "Type 'exit' or 'Ctrl+D' to return.\n" %
                         self.path(args[0]))
        sys.stdout.flush()
        self.read(args[0])

        try:
            subprocess.check_call([os.environ['SHELL']],
                                  universal_newlines=True,
                                  shell=shellout,
                                  bufsize=0,
                                  close_fds=True)
        except OSError as err:
            if err.errno == 2:
                self.parser.error(err.errno,
                                  "Unable to find shell %s" %
                                  os.environ['SHELL'])
            else:
                self.parser.exit(err.errno, '')

    def call(self, args):
        self.parser.set_usage(self.envdir_usage)
        self.parser.prog = 'envdir'

        if len(args) < 2:
            self.parser.error("incorrect number of arguments")
            self.parser.print_usage()

        self.read(args[0])

        # the args to call later
        child_args = args[1:]

        # in case someone passes in -- for any reason to separate the commands
        if child_args[0] == '--':
            child_args = child_args[1:]

        try:
            subprocess.check_call(child_args,
                                  universal_newlines=True,
                                  shell=shellout,
                                  bufsize=0,
                                  close_fds=True)
        except OSError as err:
            if err.errno == 2:
                self.parser.error(err.errno,
                                  "Unable to find command %s" %
                                  child_args[0])
            else:
                self.parser.exit(err.errno, '')
        except subprocess.CalledProcessError as err:
            self.parser.exit(err.returncode, '')
        except KeyboardInterrupt:
            self.parser.exit()

    def main(self, name, args):
        options, args = self.parser.parse_args(args)
        if name.endswith('envdir') or name.endswith('__main__.py'):
            self.call(args)
        elif name.endswith('envshell'):
            self.shell(args)
        else:
            self.parser.print_usage(sys.stderr)

envdir = Runner()


def main():
    envdir.main(sys.argv[0], sys.argv[1:])

if __name__ == '__main__':
    main()
