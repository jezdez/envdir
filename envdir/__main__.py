import glob
import optparse
import os
import subprocess
import sys

__version__ = '0.2.1'


class EnvOptionParser(optparse.OptionParser):

    def error(self, msg, no=2):
        """error(msg : string, [no : int])

        Print a usage message incorporating 'msg' to stderr and exit.
        Takes an optional error number.
        """
        self.print_usage(sys.stderr)
        self.exit(no, "%s: error: %s\n" % (self.get_prog_name(), msg))


class Envdir(object):
    usage = "usage: %prog [--help] [--version] dir child"

    def __init__(self):
        self.parser = EnvOptionParser(self.usage,
                                      version=__version__,
                                      prog='envdir')
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
                value = env_file.readline().strip()
                yield name, value

    def read(self, path=None):
        if path is None:
            frame = sys._getframe()
            callerdir = os.path.dirname(frame.f_back.f_code.co_filename)
            path = os.path.join(callerdir, 'envdir')

        real_path = os.path.realpath(os.path.expanduser(path))
        if not os.path.exists(real_path):
            # use 111 error code to adher to envdir's standard
            self.parser.error("envdir %r does not exist" % path, no=111)

        for name, value in self.environ(real_path):
            if value:
                os.environ.setdefault(name, value)
            elif name in os.environ:
                del os.environ[name]

    def main(self, args):
        options, args = self.parser.parse_args(args)

        if len(args) < 2:
            self.parser.error("incorrect number of arguments")
            self.parser.print_usage()

        self.read(args[0])

        # the args to call later
        child_args = args[1:]

        # in case someone passes in -- for any reason to separate the commands
        if child_args[0] == '--':
            child_args = child_args[1:]

        process = subprocess.Popen(child_args,
                                   universal_newlines=True,
                                   shell=False,
                                   bufsize=0,
                                   close_fds=True)

        if process.wait() != 0:
            self.parser.exit(process.returncode, '')

envdir = Envdir()


def main():
    envdir.main(sys.argv[1:])

if __name__ == '__main__':
    main()
