from os import path
from setuptools import setup

setup(
    name='selfieclub',
    # Please read the following for setting the version number:
    #    - https://pythonhosted.org/setuptools/setuptools.html#specifying-your-project-s-version  # noqa
    version='1.4.0-dev',
    author='Pedro H <pedro@builtinmenlo.com>, Phillip Winn <phillip@builtinmenlo.com>',
    author_email='pedro@builtinmenlo.com',
    install_requires=[
        'Django>=1.6.5',
        'MySQL-python>=1.2.5',
        'amqp>=1.4.5',
        'boto>=2.32.1',
        'celery>=3.1.13',
        'djangorestframework>=2.3.14',
        'drf-compound-fields>=0.2.1',
        'nexmomessage>=0.1.1',
        'requests>=2.4.1'],
    # It is because of this we have to use `--process-dependency-links` with
    # `pip install`.  Although pip 1.5.x says that `--process-dependency-links`
    # will be depricated, it seems that it will be kept:
    #    - https://github.com/pypa/pip/pull/1955/files - removal reverted
    #    - https://groups.google.com/forum/#!topic/pypa-dev/tJ6HHPQpyJ4 - 
    #      thread discussing the revert.
    # 
    # "libpynexmo" was forked for stability, and security.
    dependency_links = [
        'https://github.com/BuiltInMenlo/libpynexmo/tarball/0.1.1#egg=nexmomessage-0.1.1'])
