import os
import subprocess
import py

import envdir
from envdir.runner import Runner, Response
from envdir.__main__ import go

runner = Runner()

api = py.test.mark.api
run = py.test.mark.run
shell = py.test.mark.shell


@run
def test_usage():
    "Testing the usage"
    with py.test.raises(Response) as response:
        runner.run('envdir')
    assert "incorrect number of arguments" in response.value.message
    assert response.value.status == 2


@run
def test_default(tmpdir):
    "Default cases."
    tmp = tmpdir.mkdir('testenvdir')
    tmp.join('DEFAULT').write('test')
    with py.test.raises(Response) as response:
        runner.run('envdir', str(tmp), 'ls')
    assert "DEFAULT" in os.environ
    assert response.value.status == 0
    assert response.value.message == ''

    tmp.join('DEFAULT_DASHDASH').write('test')
    with py.test.raises(Response) as response:
        runner.run('envdir', str(tmp), '--', 'ls')
    assert "DEFAULT_DASHDASH" in os.environ

    # Overriding an env var inline
    os.environ['DEFAULT_OVERRIDE'] = 'test2'
    with py.test.raises(Response) as response:
        runner.run('envdir', str(tmp), 'ls')
    assert "DEFAULT" in os.environ
    assert "DEFAULT_OVERRIDE" in os.environ
    assert response.value.status == 0
    assert response.value.message == ''


@run
def test_reset(tmpdir):
    "Resetting an env var with an empty file"
    tmp = tmpdir.mkdir('testenvdir')
    tmp.join('RESET').write('')
    os.environ['RESET'] = 'test3'
    with py.test.raises(Response):
        runner.run('envdir', str(tmp), 'ls')
    assert os.environ['DEFAULT'] == 'test'
    with py.test.raises(KeyError):
        assert os.environ['RESET'] == 'test3'


@run
def test_multiline(tmpdir):
    "Multiline envdir file"
    tmp = tmpdir.mkdir('testenvdir')
    tmp.join('MULTI_LINE').write("""multi
line
""")
    with py.test.raises(Response):
        runner.run('envdir', str(tmp), 'ls')
    assert os.environ['MULTI_LINE'] == 'multi\nline'


@run
def test_translate_nulls(tmpdir):
    "NULLs are translated into newline"
    tmp = tmpdir.mkdir('testenvdir')
    tmp.join('NULL_CHARS').write("""null\x00character""")
    with py.test.raises(Response):
        runner.run('envdir', str(tmp), 'ls')
    assert os.environ['NULL_CHARS'] == 'null\ncharacter'


@run
def test_incorrect_no_args(tmpdir):
    "Incorrect number of arguments"
    with py.test.raises(Response) as response:
        runner.run('envdir', str(tmpdir))
    assert 'incorrect number of arguments' in response.value.message
    assert 2 == response.value.status


@run
def test_doesnt_exist(tmpdir):
    with py.test.raises(Response) as response:
        runner.run('envdir', str(tmpdir.join('missing')), 'ls')
    assert 'does not exist' in response.value.message
    assert 111 == response.value.status

    with py.test.raises(Response) as response:
        runner.run('envdir', str(tmpdir), 'doesnt-exist')
    assert 'Unable to find command' in response.value.message
    assert 2 == response.value.status


@run
def test_must_be_directory(tmpdir):
    "The envdir must be a directory"
    tmpdir.join('not-a-directory').write('')
    with py.test.raises(Response) as response:
        runner.run('envdir', str(tmpdir.join('not-a-directory')), 'ls')
    assert 'not a directory' in response.value.message
    assert 111 == response.value.status


@run
def test_error_code(tmpdir):
    tmp = tmpdir.mkdir('errorcode')
    with py.test.raises(Response) as response:
        runner.run('envdir', str(tmp),
                   'python', '-c', 'import sys; sys.exit(19)')
    assert response.value.status == 19


@run
def test_equal_sign(tmpdir):
    tmp = tmpdir.mkdir('equalsign')
    tmp.join('EQUAL_SIGN=').write('test')
    with py.test.raises(Response):
        runner.run('envdir', str(tmp), 'printenv')
    assert 'EQUAL_SIGN' not in os.environ


timeout = py.path.local.sysfind('timeout') or py.path.local.sysfind('gtimeout')


@run
@py.test.mark.skipif(timeout is None, reason="(g)timeout command not found")
def test_keyboard_interrupt(tmpdir):
    tmp = tmpdir.mkdir('keyboard')
    with py.test.raises(SystemExit) as exit:
        go(runner.run, (str(timeout), '--signal=SIGTERM', '--', '1', 'envdir',
                        str(tmp), 'ls'))
    if py.std.sys.version_info[:2] == (2, 6):
        assert exit.value == 2
    else:
        assert exit.value.code == 2


@shell
def test_shell(tmpdir, capfd):
    tmp = tmpdir.mkdir('envshell')
    tmp.join('TEST_SHELL').write('test')
    with py.test.raises(Response) as response:
        runner.shell('envshell', str(tmp))
    out, err = capfd.readouterr()
    assert response.value.status == 0
    assert "Launching envshell for " in out

    with py.test.raises(Response) as response:
        runner.shell('envshell')
    assert "incorrect number of arguments" in response.value.message


@shell
def test_shell_doesnt_exist(tmpdir):
    tmp = tmpdir.mkdir('envshell')
    tmp.join('NO_TEST_SHELL').write('test')
    os.environ['SHELL'] = '/does/not/exist'
    with py.test.raises(Response) as response:
        runner.shell('envshell', str(tmp))
    assert "Unable to find shell" in response.value.message


@api
def test_read(tmpdir):
    tmp = tmpdir.mkdir('pythonuse')
    tmp.join('READ').write('test')
    applied = envdir.read(str(tmp))
    assert 'READ' in os.environ
    assert 'READ' in applied


@api
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


@api
def test_read_existing_var(tmpdir):
    tmp = tmpdir.mkdir('pythonuse2')
    tmp.join('READ_EXISTING').write('override')
    os.environ['READ_EXISTING'] = 'test'
    envdir.read(str(tmp))
    assert os.environ['READ_EXISTING'] == 'override'


@api
def test_write(tmpdir):
    tmp = tmpdir.mkdir('pythonuse3')
    env = envdir.open(str(tmp))
    env.write(WRITE='test')
    assert tmp.ensure('WRITE')
    assert tmp.join('WRITE').read() == 'test'
    envdir.read(str(tmp))
    assert os.environ['WRITE'] == 'test'


@api
def test_write_magic(tmpdir):
    tmp = tmpdir.mkdir('envdir')
    magic_scripts = tmpdir.join('test_magic_write.py')
    magic_scripts.write("""
import envdir, os, sys
env = envdir.open()
env.write(WRITE_MAGIC='test')
""")
    subprocess.call(['python', str(magic_scripts)])
    assert tmp.join('WRITE_MAGIC').read() == 'test'
    envdir.read(str(tmp))
    assert os.environ['WRITE_MAGIC'] == 'test'


@api
def test_context_manager(tmpdir):
    tmp = tmpdir.mkdir('envdir')
    tmp.join('CONTEXT_MANAGER').write('test')

    with envdir.open(str(tmp)) as env:
        assert 'CONTEXT_MANAGER' not in os.environ
        env.read()
        assert 'CONTEXT_MANAGER' in os.environ
    assert 'CONTEXT_MANAGER' not in os.environ
    assert repr(env) == "<envdir.Env '%s'>" % tmp


@api
def test_context_manager_reset(tmpdir):
    tmp = tmpdir.mkdir('envdir')
    tmp.join('CONTEXT_MANAGER_RESET').write('test')
    # make the var exist in the enviroment
    os.environ['CONTEXT_MANAGER_RESET'] = 'moot'
    with envdir.open(str(tmp)) as env:
        env.read()
        assert os.environ['CONTEXT_MANAGER_RESET'] == 'test'
        env.clear()
        # because we reset the original value
        assert os.environ['CONTEXT_MANAGER_RESET'] == 'moot'
        assert 'CONTEXT_MANAGER_RESET' in os.environ


@api
def test_context_manager_write(tmpdir):
    tmp = tmpdir.mkdir('envdir')
    with envdir.open(str(tmp)) as env:
        env.read()
        env.write(CONTEXT_MANAGER_WRITE='test')
        assert 'CONTEXT_MANAGER_WRITE' not in os.environ
        env.read()
        assert 'CONTEXT_MANAGER_WRITE' in os.environ
    assert 'CONTEXT_MANAGER_WRITE' not in os.environ


@api
def test_context_manager_item(tmpdir):
    tmp = tmpdir.mkdir('envdir')
    tmp.join('CONTEXT_MANAGER_ITEM').write('test')

    with envdir.open(str(tmp)) as env:
        # loaded but not read yet
        assert 'CONTEXT_MANAGER_ITEM' not in os.environ
        # the variable is in the env, but not in the env
        assert env['CONTEXT_MANAGER_ITEM'] == 'test'
        del env['CONTEXT_MANAGER_ITEM']
        assert 'CONTEXT_MANAGER_ITEM' not in os.environ
        assert 'CONTEXT_MANAGER_ITEM' not in env

        env['CONTEXT_MANAGER_ITEM_SET'] = 'test'
        assert 'CONTEXT_MANAGER_ITEM_SET' in os.environ
        assert tmp.join('CONTEXT_MANAGER_ITEM_SET').check()
        del env['CONTEXT_MANAGER_ITEM_SET']
        assert 'CONTEXT_MANAGER_ITEM_SET' not in os.environ
        assert not tmp.join('CONTEXT_MANAGER_ITEM_SET').check()
    assert tmp.ensure('CONTEXT_MANAGER_ITEM_SET')
    assert 'CONTEXT_MANAGER_ITEM_SET' not in os.environ
