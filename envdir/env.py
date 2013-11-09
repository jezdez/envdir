import glob
import os


def isenvvar(name):
    root, name = os.path.split(name)
    return (name == name.upper() and
            not name.startswith('_') and
            not '=' in name)


class Env(object):
    """
    An object to represent an envdir environment with extensive
    dict-like API, can be used as context manager.
    """
    def __init__(self, root):
        self.root = root
        self.applied = {}
        self.originals = {}
        self.created = {}

    def __repr__(self):
        return "<envdir.Env '%s'>" % self.root

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.clear()

    def __getitem__(self, name):
        return self.get(name)

    def __setitem__(self, name, value):
        self.write(**{name: value})
        self.set(name, value)
        self.created[name] = value

    def __delitem__(self, name):
        os.remove(os.path.join(self.root, name))
        self.delete(name)

    def __contains__(self, name):
        return (name in self.applied or
                os.path.exists(os.path.join(self.root, name)))

    def clear(self):
        for name in list(self.applied.keys()):
            self.delete(name)
            if name in self.created:
                os.remove(os.path.join(self.root, name))

    def open(self, name, mode='r'):
        return open(os.path.join(self.root, name), mode)

    def get(self, name):
        with self.open(name) as var:
            return var.read().strip().replace('\x00', '\n')

    def set(self, name, value):
        if name in os.environ:
            self.originals[name] = os.environ[name]
        self.applied[name] = value
        if value:
            os.environ[name] = value
        elif name in os.environ:
            del os.environ[name]

    def delete(self, name):
        if name in self.originals:
            os.environ[name] = self.originals[name]
        elif name in os.environ:
            del os.environ[name]
        if name in self.applied:
            del self.applied[name]

    def read(self):
        for path in filter(isenvvar, glob.glob(os.path.join(self.root, '*'))):
            root, name = os.path.split(path)
            value = self.get(name)
            self.set(name, value)
        return self.applied

    def write(self, **values):
        for name, value in values.items():
            with self.open(name, 'w') as env:
                env.write('%s' % value)
