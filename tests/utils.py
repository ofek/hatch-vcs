# SPDX-FileCopyrightText: 2022-present Ofek Lev <oss@ofek.dev>
#
# SPDX-License-Identifier: MIT
import os
import subprocess
import sys


def create_file(path):
    with open(path, 'a'):
        os.utime(path, None)


def read_file(path):
    with open(path) as f:
        return f.read()


def write_file(path, contents):
    with open(path, 'w') as f:
        f.write(contents)


def build_project(*args, **kwargs):
    if 'env' not in kwargs:
        env = os.environ.copy()
        env.pop('SETUPTOOLS_SCM_PRETEND_VERSION', None)
    else:
        env = kwargs['env']
    _run_command(sys.executable, '-m', 'hatchling', 'build', *args, env=env)


def git(*args):
    return _run_command('git', *args)


def _run_command(*command, **kwargs):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, **kwargs)
    stdout, _ = process.communicate()
    stdout = stdout.decode('utf-8')

    if process.returncode:  # no cov
        raise Exception(stdout)

    return stdout
