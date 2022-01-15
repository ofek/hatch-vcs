# SPDX-FileCopyrightText: 2022-present Ofek Lev <oss@ofek.dev>
#
# SPDX-License-Identifier: MIT
import errno
import os
import shutil
import stat
import tempfile
from contextlib import contextmanager

import pytest

from .utils import create_file, git, write_file


def handle_remove_readonly(func, path, exc):  # no cov
    # PermissionError: [WinError 5] Access is denied: '...\\.git\\...'
    if func in (os.rmdir, os.remove, os.unlink) and exc[1].errno == errno.EACCES:
        os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        func(path)
    else:
        raise


@pytest.fixture
def temp_dir():
    directory = tempfile.mkdtemp()
    try:
        directory = os.path.realpath(directory)
        yield directory
    finally:
        shutil.rmtree(directory, ignore_errors=False, onerror=handle_remove_readonly)


@contextmanager
def create_project(directory, metadata, setup_vcs=True):
    project_dir = os.path.join(directory, 'my-app')
    os.mkdir(project_dir)

    gitignore_file = os.path.join(project_dir, '.gitignore')
    write_file(gitignore_file, '/my_app/version.py')

    project_file = os.path.join(project_dir, 'pyproject.toml')
    write_file(project_file, metadata)

    package_dir = os.path.join(project_dir, 'my_app')
    os.mkdir(package_dir)

    create_file(os.path.join(package_dir, '__init__.py'))
    create_file(os.path.join(package_dir, 'foo.py'))
    create_file(os.path.join(package_dir, 'bar.py'))
    create_file(os.path.join(package_dir, 'baz.py'))

    origin = os.getcwd()
    os.chdir(project_dir)
    try:
        if setup_vcs:
            git('init')
            git('config', '--local', 'user.name', 'foo')
            git('config', '--local', 'user.email', 'foo@bar.baz')
            git('add', '.')
            git('commit', '-m', 'test')
            git('tag', '1.2.3')

        yield project_dir
    finally:
        os.chdir(origin)


@pytest.fixture
def new_project_basic(temp_dir):
    with create_project(
        temp_dir,
        """\
[build-system]
requires = ["hatchling", "hatch-vcs"]
build-backend = "hatchling.build"

[project]
name = "my-app"
dynamic = ["version"]

[tool.hatch.version]
source = "vcs"
""",
    ) as project:
        yield project


@pytest.fixture
def new_project_write(temp_dir):
    with create_project(
        temp_dir,
        """\
[build-system]
requires = ["hatchling", "hatch-vcs"]
build-backend = "hatchling.build"

[project]
name = "my-app"
dynamic = ["version"]

[tool.hatch.version]
source = "vcs"

[tool.hatch.build.targets.wheel.hooks.vcs]
version-file = "my_app/_version.py"
""",
    ) as project:
        yield project


@pytest.fixture
def new_project_fallback(temp_dir):
    with create_project(
        temp_dir,
        """\
[build-system]
requires = ["hatchling", "hatch-vcs"]
build-backend = "hatchling.build"

[project]
name = "my-app"
dynamic = ["version"]

[tool.hatch.version]
source = "vcs"
fallback-version = "7.8.9"
""",
        setup_vcs=False,
    ) as project:
        yield project
