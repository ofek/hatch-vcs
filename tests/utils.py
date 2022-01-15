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
    with open(path, 'r') as f:
        return f.read()


def write_file(path, contents):
    with open(path, 'w') as f:
        f.write(contents)


def build_project(*args):
    _run_command(sys.executable, '-m', 'hatchling', 'build', *args)


def git(*args):
    _run_command('git', *args)


def _run_command(*command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, _ = process.communicate()

    if process.returncode:  # no cov
        raise Exception(stdout.decode('utf-8'))
