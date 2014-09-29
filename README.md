# selficlub!!!

## Developing

### Setting up your virtualenv

Quick and dirty way to get set up:

```
$ git clone git@github.com:BuiltInMenlo/selfieclub.git
$ cd selfieclub.git
$ virtualenv --python python2.7 .virtualenv
$ source .virtualenv/bin/activate
$ pip install --process-dependency-links -r requirements.txt
```


### Useful commands

#### Django

To run the built in development server:

```
$./manage.py runserver
```

#### Celery

***TODO***

### Before you commit/push!

Before you commit/push those changes you made:

- If you are working on a feature branch, make sure to update master then
  rebase: `git rebase master`
- Make sure that you pull in changes and rebase, `git pull --rebase`.
- Execute all tests using `tox`.

The flow should look something like this:

```
$ git checkout master
$ git pull
$ git checkout feature/ci
$ git rebase master
$ tox
```

### Working with Vim

A suggested work flow is use [Syntastic][SYNTASTIC] in `vim` to execute most of
the code checkers used by `tox` on every save.  This will help you catch errors
as early as possible.

For instructions on how to install *Syntastic*, please refer to their site
[Github-Syntastic][SYNTASTIC].

Add the following to you `~/.vimrc` file:

```
let g:syntastic_python_checkers = ['python', 'flake8', 'pylint', 'py3kwarn', 'pep257']
```

Note that the checkers are executed in order.  Feel free to modify as you like.

In order to help `pylint` find its configuration file, make sure to set
`PYLINTRC` before starting `vim`:

```
$ export PYLINTRC=~/dev/src-bim/selfieclub-ci/pylintrc
```


### Bash helper

You might want to add the following to you `~/.bashrc`.  It will let you use
the `py-activate-env`, and `py-deactivate-env` commands to activate, and
deactivate` your `virtualenv`.  They also help you manage the `PYLINTRC`
environment variable.

```
#------------------------------------------------------------------------------
# Python virtualenv management
#------------------------------------------------------------------------------
function py-activate-env ()
{
    # Make sure we do not nest environments
    if [ -n "$VIRTUAL_ENV" ]; then
        echo "ERROR - $FUNCNAME already set to '$VIRTUAL_ENV'"
        return 1
    fi

    # Is there a local virtualenv
    local l_activate="$PWD/.virtualenv/bin/activate"
    if [ ! -e "$l_activate" ]; then
        echo "ERROR - Could not find '$l_activate'"
        return 1
    fi

    echo "Activating: $l_activate"
    source $l_activate
    if [ $? -ne 0 ]; then
        echo "ERROR - Failed to exectute '$l_activate'"
        return 1
    fi

    export PYLINTRC="$PWD/pylintrc"
    export __VIRTUAL_ENV_LOC=$(basename "$PWD")
    export VIRTUAL_ENV_DISABLE_PROMPT="true"
}

function py-deactivate-env ()
{
    # Make sure we are in a virtual environment
    if [ -z "$VIRTUAL_ENV" ]; then
        echo "ERROR - No virtualenv set"
        return 1
    fi

    # Does the deactivate function actually exist?
    local l_func=$(type -t "deactivate")
    if [ -z "$l_func" ]; then
        echo "ERROR - Could not find 'deactivate'"
        return 1
    fi

    echo "Deactivating: $VIRTUAL_ENV"
    deactivate
    if [ $? -ne 0 ]; then
        echo "ERROR - Failed to exectute 'deactivate'"
        return 1
    fi

    unset __VIRTUAL_ENV_LOC VIRTUAL_ENV_DISABLE_PROMPT PYLINTRC
    export __VIRTUAL_ENV_LOC VIRTUAL_ENV_DISABLE_PROMPT PYLINTRC
}
```


## Continuous integration

This project uses `tox` to execute the following code quality tools:

- flake8
- pylint
- py3kwarn
- pep257

**NOTE:** Virtually all of the descriptions of the tools, in the following
subsections, were taken dirctly from the indivdual tool's documenation.

### Tox

Tox as is a generic virtualenv management and test command line tool you can
use for:

- checking your package installs correctly with different Python versions
  and interpreters
- running your tests in each of the environments, configuring your test
  tool of choice
- acting as a frontend to Continuous Integration servers, greatly
  reducing boilerplate and merging CI and shell-based testing.

For more information:

  - [Tox - Pypi][TOX-PYPI]
  - [Tox - documentation][TOX-RTD]


### flake8

Flake8 is a wrapper around these tools:

- PyFlakes - Passive checker of Python programs.  A simple program which checks
  Python source files for errors.  Pyflakes analyzes programs and detects
  various errors. It works by parsing the source file, not importing it, so it
  is safe to use on modules with side effects. It's also much faster.
- pep8 - pep8 is a tool to check your Python code against some of the style
  conventions in PEP 8.
- Ned Batchelder’s McCabe script - Cyclomaniacs code complexity checker.

For more information:

  - [PEP 8 -- Style Guide for Python Code][PEP8]
  - [flake8 - Pypi][FLAKE8-PYPI]
  - [flake8 - documentation][FLAKE8-RTD]


### pylint

Pylint is a Python source code analyzer which looks for programming errors,
helps enforcing a coding standard and sniffs for some code smells (as defined
in Martin Fowler's Refactoring book).

For more information:

  - [pyline - Pypi][PYLINE-PYPI]
  - [pyline - documentation][PYLINE-RTD]


### py3kwarn

py3kwarn detects code that is not Python 3 compatible. It provides flake8-style
warning messages.

For more information:

  - [py3kwarn - Pypi][PY3KWARN-PYPI]
  - [py3kwarn - documentation][PY3KWARN-RTD]


### pep257

For more information:

  - [PEP 257 -- Docstring Conventions][PEP257]
  - [pep257 - Pypi][PEP257-PYPI]
  - [pep257 - documentation][PEP257-RTD]




[TOX-PYPI]: https://pypi.python.org/pypi/tox
[TOX-RTD]: https://tox.readthedocs.org/en/latest/
[PEP8]: http://legacy.python.org/dev/peps/pep-0008/
[FLAKE8-PYPI]: https://pypi.python.org/pypi/flake8
[FLAKE8-RTD]: https://flake8.readthedocs.org/en/
[PYLINE-PYPI]: https://pypi.python.org/pypi/pylint
[PYLINE-RTD]: http://www.pylint.org/
[PY3KWARN-PYPI]: https://pypi.python.org/pypi/py3kwarn
[PY3KWARN-RTD]: https://github.com/liamcurry/py3kwarn
[PEP257]: http://legacy.python.org/dev/peps/pep-0257/
[PEP257-PYPI]: https://pypi.python.org/pypi/pep257
[PEP257-RTD]: https://github.com/GreenSteam/pep257/
[SYNTASTIC]: https://github.com/scrooloose/syntastic (Syntastic)
