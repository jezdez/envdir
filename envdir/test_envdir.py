import os
import subprocess
import py
import pytest

import envdir
from envdir.runner import Response
from envdir.__main__ import go


@pytest.fixture(scope="module")
def run():
    from envdir.runner import Runner
    runner = Runner()
    return runner.run


@pytest.fixture(scope="module")
def shell():
    from envdir.runner import Runner
    runner = Runner()
    return runner.shell


@pytest.fixture
def tmpenvdir(tmpdir):
    return tmpdir.mkdir('testenvdir')


def test_usage(run):
    "Testing the usage"
    with py.test.raises(Response) as response:
        run('envdir')
    assert "incorrect number of arguments" in response.value.message
    assert response.value.status == 2


def test_default(run, tmpenvdir):
    "Default cases."
    tmpenvdir.join('DEFAULT').write('test')
    with py.test.raises(Response) as response:
        run('envdir', str(tmpenvdir), 'ls')
    assert "DEFAULT" in os.environ
    assert response.value.status == 0
    assert response.value.message == ''

    tmpenvdir.join('DEFAULT_DASHDASH').write('test')
    with py.test.raises(Response) as response:
        run('envdir', str(tmpenvdir), '--', 'ls')
    assert "DEFAULT_DASHDASH" in os.environ

    # Overriding an env var inline
    os.environ['DEFAULT_OVERRIDE'] = 'test2'
    with py.test.raises(Response) as response:
        run('envdir', str(tmpenvdir), 'ls')
    assert "DEFAULT" in os.environ
    assert "DEFAULT_OVERRIDE" in os.environ
    assert response.value.status == 0
    assert response.value.message == ''


def test_reset(run, tmpenvdir):
    "Resetting an env var with an empty file"
    tmpenvdir.join('RESET').write('')
    os.environ['RESET'] = 'test3'
    with py.test.raises(Response):
        run('envdir', str(tmpenvdir), 'ls')
    assert os.environ['DEFAULT'] == 'test'
    with py.test.raises(KeyError):
        assert os.environ['RESET'] == 'test3'


def test_multiline(run, tmpenvdir):
    "Multiline envdir file"
    tmpenvdir.join('MULTI_LINE').write("""multi
line
""")
    with py.test.raises(Response):
        run('envdir', str(tmpenvdir), 'ls')
    assert os.environ['MULTI_LINE'] == 'multi\nline'


def test_translate_nulls(run, tmpenvdir):
    "NULLs are translated into newline"
    tmpenvdir.join('NULL_CHARS').write("""null\x00character""")
    with py.test.raises(Response):
        run('envdir', str(tmpenvdir), 'ls')
    assert os.environ['NULL_CHARS'] == 'null\ncharacter'


def test_incorrect_no_args(run, tmpenvdir):
    "Incorrect number of arguments"
    with py.test.raises(Response) as response:
        run('envdir', str(tmpenvdir))
    assert 'incorrect number of arguments' in response.value.message
    assert 2 == response.value.status


def test_doesnt_exist(run, tmpdir):
    with py.test.raises(Response) as response:
        run('envdir', str(tmpdir.join('missing')), 'ls')
    assert 'does not exist' in response.value.message
    assert 111 == response.value.status

    with py.test.raises(Response) as response:
        run('envdir', str(tmpdir), 'doesnt-exist')
    assert 'Unable to find command' in response.value.message
    assert 2 == response.value.status


def test_must_be_directory(run, tmpdir):
    "The envdir must be a directory"
    tmpdir.join('not-a-directory').write('')
    with py.test.raises(Response) as response:
        run('envdir', str(tmpdir.join('not-a-directory')), 'ls')
    assert 'not a directory' in response.value.message
    assert 111 == response.value.status


def test_error_code(run, tmpenvdir):
    with py.test.raises(Response) as response:
        run('envdir', str(tmpenvdir),
            'python', '-c', 'import sys; sys.exit(19)')
    assert response.value.status == 19


def test_equal_sign(run, tmpenvdir):
    tmpenvdir.join('EQUAL_SIGN=').write('test')
    with py.test.raises(Response):
        run('envdir', str(tmpenvdir), 'printenv')
    assert 'EQUAL_SIGN' not in os.environ


timeout = py.path.local.sysfind('timeout') or py.path.local.sysfind('gtimeout')


@py.test.mark.skipif(timeout is None,
                     reason="(g)timeout command not found")
def test_keyboard_interrupt(run, tmpenvdir):
    with py.test.raises(SystemExit) as exit:
        go(run, (str(timeout), '--signal=SIGTERM', '--', '1', 'envdir',
                 str(tmpenvdir), 'ls'))
    if py.std.sys.version_info[:2] == (2, 6):
        assert exit.value == 2
    else:
        assert exit.value.code == 2


def test_shell(shell, tmpenvdir, capfd):
    tmpenvdir.join('TEST_SHELL').write('test')
    with py.test.raises(Response) as response:
        shell('envshell', str(tmpenvdir))
    out, err = capfd.readouterr()
    assert response.value.status == 0
    assert "Launching envshell for " in out

    with py.test.raises(Response) as response:
        shell('envshell')
    assert "incorrect number of arguments" in response.value.message


def test_shell_doesnt_exist(shell, tmpenvdir):
    tmpenvdir.join('NO_TEST_SHELL').write('test')
    os.environ['SHELL'] = '/does/not/exist'
    with py.test.raises(Response) as response:
        shell('envshell', str(tmpenvdir))
    assert "Unable to find shell" in response.value.message


def test_read(tmpenvdir):
    tmpenvdir.join('READ').write('test')
    applied = envdir.read(str(tmpenvdir))
    assert 'READ' in os.environ
    assert 'READ' in applied


def test_read_magic_dir(capfd, tmpdir):
    "Python usage with magic envdir"
    tmp = tmpdir.mkdir('envdir')
    tmp.join('READ_MAGIC').write('test')
    magic_scripts = tmpdir.join('test_magic.py')
    magic_scripts.write("""
import envdir, os, sys
envdir.read()
if 'READ_MAGIC' in os.environ:
    sys.exit(42)
""")
    status = subprocess.call(['python', str(magic_scripts)])
    assert status == 42

    # this should raise a Response with an error because envdir.run()
    # can't have all arguments
    with py.test.raises(SystemExit) as response:
        envdir.run('envdir', str(tmp))
    out, err = capfd.readouterr()

    if py.std.sys.version_info[:2] == (2, 6):
        assert response.value == 2
    else:
        assert response.value.code == 2
    assert "incorrect number of arguments" in err

    with py.test.raises(SystemExit) as response:
        envdir.run()
    out, err = capfd.readouterr()
    if py.std.sys.version_info[:2] == (2, 6):
        assert response.value == 2
    else:
        assert response.value.code == 2


def test_read_existing_var(tmpenvdir):
    tmpenvdir.join('READ_EXISTING').write('override')
    os.environ['READ_EXISTING'] = 'test'
    envdir.read(str(tmpenvdir))
    assert os.environ['READ_EXISTING'] == 'override'


def test_write(tmpenvdir):
    env = envdir.open(str(tmpenvdir))
    env['WRITE'] = 'test'
    assert tmpenvdir.ensure('WRITE')
    assert tmpenvdir.join('WRITE').read() == 'test'
    envdir.read(str(tmpenvdir))
    assert os.environ['WRITE'] == 'test'


def test_write_magic(tmpdir):
    tmp = tmpdir.mkdir('envdir')
    magic_scripts = tmpdir.join('test_magic_write.py')
    magic_scripts.write("""
import envdir, os, sys
env = envdir.open()
env['WRITE_MAGIC'] = 'test'
""")
    subprocess.call(['python', str(magic_scripts)])
    assert tmp.join('WRITE_MAGIC').read() == 'test'
    envdir.read(str(tmp))
    assert os.environ['WRITE_MAGIC'] == 'test'


def test_context_manager(tmpenvdir):
    tmpenvdir.join('CONTEXT_MANAGER').write('test')

    with envdir.open(str(tmpenvdir)) as env:
        assert 'CONTEXT_MANAGER' in os.environ
    assert 'CONTEXT_MANAGER' not in os.environ
    assert repr(env) == "<envdir.Env '%s'>" % tmpenvdir


def test_dict_like(tmpenvdir):
    tmpenvdir.join('ITER').write('test')
    env = envdir.open(str(tmpenvdir))
    assert list(env) == ['ITER']
    assert hasattr(env, '__iter__')

    assert [k for k in env] == ['ITER']
    assert list(env.values()) == ['test']
    assert list(env.items()) == [('ITER', 'test')]
    assert 'ITER' in os.environ
    env.clear()
    assert list(env.items()) == []
    assert 'ITER' not in os.environ

    with envdir.open(str(tmpenvdir)) as env:
        assert list(env.items()) == [('ITER', 'test')]


def test_context_manager_reset(tmpenvdir):
    tmpenvdir.join('CONTEXT_MANAGER_RESET').write('test')
    # make the var exist in the enviroment
    os.environ['CONTEXT_MANAGER_RESET'] = 'moot'
    with envdir.open(str(tmpenvdir)) as env:
        assert os.environ['CONTEXT_MANAGER_RESET'] == 'test'
        env.clear()
        # because we reset the original value
        assert os.environ['CONTEXT_MANAGER_RESET'] == 'moot'
        assert 'CONTEXT_MANAGER_RESET' in os.environ


def test_context_manager_write(tmpenvdir):
    with envdir.open(str(tmpenvdir)) as env:
        assert 'CONTEXT_MANAGER_WRITE' not in os.environ
        env['CONTEXT_MANAGER_WRITE'] = 'test'
        assert 'CONTEXT_MANAGER_WRITE' in os.environ
    assert 'CONTEXT_MANAGER_WRITE' not in os.environ


def test_context_manager_item(tmpenvdir):
    tmpenvdir.join('CONTEXT_MANAGER_ITEM').write('test')

    with envdir.open(str(tmpenvdir)) as env:
        assert 'CONTEXT_MANAGER_ITEM' in os.environ
        # the variable is in the env, but not in the env
        assert env['CONTEXT_MANAGER_ITEM'] == 'test'
        del env['CONTEXT_MANAGER_ITEM']
        assert 'CONTEXT_MANAGER_ITEM' not in os.environ
        assert 'CONTEXT_MANAGER_ITEM' not in env

        env['CONTEXT_MANAGER_ITEM_SET'] = 'test'
        assert 'CONTEXT_MANAGER_ITEM_SET' in os.environ
        assert tmpenvdir.join('CONTEXT_MANAGER_ITEM_SET').check()
        del env['CONTEXT_MANAGER_ITEM_SET']
        assert 'CONTEXT_MANAGER_ITEM_SET' not in os.environ
        assert not tmpenvdir.join('CONTEXT_MANAGER_ITEM_SET').check()
    assert tmpenvdir.ensure('CONTEXT_MANAGER_ITEM_SET')
    assert 'CONTEXT_MANAGER_ITEM_SET' not in os.environ
