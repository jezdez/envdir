The usage

  $ envdir
  Usage: envdir [--help] [--version] dir child
  
  envdir: error: incorrect number of arguments
  [2]

Checking version

  $ envdir --version
  [\d\.]+ (re)

Default cases.

  $ mkdir testenvdir
  $ echo "test" > testenvdir/TEST_VAR
  $ envdir testenvdir printenv | grep TEST_VAR
  TEST_VAR=test

Using an extra pipe

  $ envdir testenvdir -- printenv | grep TEST_VAR
  TEST_VAR=test

Overriding an env var inline

  $ TEST_VAR2=test2 envdir testenvdir printenv | grep TEST_VAR
  TEST_VAR2=test2
  TEST_VAR=test

Resetting an env var with an empty file

  $ echo "" > testenvdir/TEST_VAR3
  $ TEST_VAR3=test3 envdir testenvdir printenv | grep TEST_VAR
  TEST_VAR=test

Multiline envdir file

  $ echo "multi    
  > line
  > " > testenvdir/MULTI_LINE
  $ envdir testenvdir python -c "import os; print(os.environ['MULTI_LINE'])"
  multi.* (re)
  line

NULLs are translated into newline

  $ printf "null\0character" > testenvdir/TEST_NULL
  $ envdir testenvdir printenv TEST_NULL
  null
  character

Incorrect number of arguments

  $ mkdir incorrect
  $ envdir incorrect
  Usage: envdir [--help] [--version] dir child
  
  envdir: error: incorrect number of arguments
  [2]

The envdir does not exist

  $ envdir non-existant ls
  Usage: envdir [--help] [--version] dir child
  
  envdir: error: envdir 'non-existant' does not exist
  [111]

The envdir must be a directory

  $ touch not-a-directory
  $ envdir not-a-directory ls
  Usage: envdir [--help] [--version] dir child
  
  envdir: error: envdir 'not-a-directory' not a directory
  [111]

Error code proxy

  $ mkdir errorcode
  $ envdir errorcode python -c "import sys; sys.exit(19)"
  [19]

Name cannot contain =

  $ mkdir equalsign
  $ echo "test" > "equalsign/EQUAL_SIGN="
  $ envdir equalsign printenv | grep EQUAL_SIGN
  [1]

Shell

  $ mkdir envshell
  $ echo "test" > "envshell/TEST_VAR4"
  $ envshell envshell
  Launching envshell for *. Type 'exit' or 'Ctrl+D' to return. (glob)

Python usage with a specific directory

  $ mkdir pythonuse
  $ echo "test" > "pythonuse/TEST_VAR5"
  $ python -c "import envdir, subprocess; envdir.read('pythonuse'); subprocess.call('printenv')" | grep TEST_VAR5
  TEST_VAR5=test

Python usage with magic envdir

  $ mkdir envdir
  $ echo "test" > "envdir/TEST_VAR6"
  $ echo "import envdir, os, sys
  > envdir.read()
  > if 'TEST_VAR6' in os.environ:
  >     sys.exit(42)
  > " > test.py
  $ python test.py
  [42]

Python usage with preexisting env var

  $ mkdir pythonuse2
  $ echo "override" > "pythonuse2/TEST_VAR7"
  $ TEST_VAR7=test python -c "import envdir, subprocess; envdir.read('pythonuse2'); subprocess.call('printenv')" | grep TEST_VAR7
  TEST_VAR7=override

Python usage writing envdir

  $ python -c "import envdir; envdir.write('pythonuse3', TEST_VAR_8='hello')"
  $ ls pythonuse3
  TEST_VAR_8

  $ cat ./pythonuse3/TEST_VAR_8
  hello (no-eol)

  $ python -c "import envdir, subprocess; envdir.read('pythonuse3'); subprocess.call('printenv')" | grep TEST_VAR_8
  TEST_VAR_8=hello

Python usage trying to write to existing envdir

  $ python -c "import envdir; envdir.write('pythonuse4/envdir', TEST_VAR_9='hello')"
  $ ls pythonuse4/envdir
  TEST_VAR_9

  $ python -c "import envdir; envdir.write('pythonuse4/envdir', TEST_VAR_10='hello')"
  Traceback * (glob)
    File "<string>", line (\d+), in <module> (re)
    File "(.+)envdir/__main__.py", line (\d+), in write (re)
      os.makedirs(path)
    File "(.+)os.py", line (\d+), in makedirs (re)
      mkdir(name, mode)
  *: [Errno 17] File exists: 'pythonuse4/envdir' (glob)
  [1]
