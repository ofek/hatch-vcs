# SPDX-FileCopyrightText: 2022-present Ofek Lev <oss@ofek.dev>
#
# SPDX-License-Identifier: MIT
import os
import sys
import zipfile

import pytest

from .utils import build_project, git, read_file


def test_basic(new_project_basic):
    build_project('-t', 'wheel')

    build_dir = os.path.join(new_project_basic, 'dist')
    assert os.path.isdir(build_dir)

    artifacts = os.listdir(build_dir)
    assert len(artifacts) == 1
    wheel_file = artifacts[0]

    assert wheel_file == 'my_app-1.2.3-py2.py3-none-any.whl'

    extraction_directory = os.path.join(os.path.dirname(new_project_basic), '_archive')
    os.mkdir(extraction_directory)

    with zipfile.ZipFile(os.path.join(build_dir, wheel_file), 'r') as zip_archive:
        zip_archive.extractall(extraction_directory)

    metadata_directory = os.path.join(extraction_directory, 'my_app-1.2.3.dist-info')
    assert os.path.isdir(metadata_directory)

    package_directory = os.path.join(extraction_directory, 'my_app')
    assert os.path.isdir(package_directory)
    assert len(os.listdir(package_directory)) == 4

    assert os.path.isfile(os.path.join(package_directory, '__init__.py'))
    assert os.path.isfile(os.path.join(package_directory, 'foo.py'))
    assert os.path.isfile(os.path.join(package_directory, 'bar.py'))
    assert os.path.isfile(os.path.join(package_directory, 'baz.py'))


def test_write(new_project_write):
    build_project('-t', 'wheel')

    build_dir = os.path.join(new_project_write, 'dist')
    assert os.path.isdir(build_dir)

    artifacts = os.listdir(build_dir)
    assert len(artifacts) == 1
    wheel_file = artifacts[0]

    assert wheel_file == 'my_app-1.2.3-py2.py3-none-any.whl'

    extraction_directory = os.path.join(os.path.dirname(new_project_write), '_archive')
    os.mkdir(extraction_directory)

    with zipfile.ZipFile(os.path.join(build_dir, wheel_file), 'r') as zip_archive:
        zip_archive.extractall(extraction_directory)

    metadata_directory = os.path.join(extraction_directory, 'my_app-1.2.3.dist-info')
    assert os.path.isdir(metadata_directory)

    package_directory = os.path.join(extraction_directory, 'my_app')
    assert os.path.isdir(package_directory)
    assert len(os.listdir(package_directory)) == 5

    assert os.path.isfile(os.path.join(package_directory, '__init__.py'))
    assert os.path.isfile(os.path.join(package_directory, 'foo.py'))
    assert os.path.isfile(os.path.join(package_directory, 'bar.py'))
    assert os.path.isfile(os.path.join(package_directory, 'baz.py'))

    version_file = os.path.join(package_directory, '_version.py')
    assert os.path.isfile(version_file)

    lines = read_file(version_file).splitlines()
    version_starts = ('version = ', '__version__ = ')
    assert any(line.startswith(version_starts) for line in lines)
    version_line = next(line for line in lines if line.startswith(version_starts))
    assert version_line.endswith(" = '1.2.3'")


@pytest.mark.skipif(sys.version_info[0] == 2, reason='Depends on fix in 6.4.0 which is Python 3-only')
def test_fallback(new_project_fallback):
    build_project('-t', 'wheel')

    build_dir = os.path.join(new_project_fallback, 'dist')
    assert os.path.isdir(build_dir)

    artifacts = os.listdir(build_dir)
    assert len(artifacts) == 1
    wheel_file = artifacts[0]

    assert wheel_file == 'my_app-7.8.9-py2.py3-none-any.whl'

    extraction_directory = os.path.join(os.path.dirname(new_project_fallback), '_archive')
    os.mkdir(extraction_directory)

    with zipfile.ZipFile(os.path.join(build_dir, wheel_file), 'r') as zip_archive:
        zip_archive.extractall(extraction_directory)

    metadata_directory = os.path.join(extraction_directory, 'my_app-7.8.9.dist-info')
    assert os.path.isdir(metadata_directory)

    package_directory = os.path.join(extraction_directory, 'my_app')
    assert os.path.isdir(package_directory)
    assert len(os.listdir(package_directory)) == 4

    assert os.path.isfile(os.path.join(package_directory, '__init__.py'))
    assert os.path.isfile(os.path.join(package_directory, 'foo.py'))
    assert os.path.isfile(os.path.join(package_directory, 'bar.py'))
    assert os.path.isfile(os.path.join(package_directory, 'baz.py'))


def test_root(new_project_root_elsewhere):
    build_project('-t', 'wheel')

    build_dir = os.path.join(new_project_root_elsewhere, 'dist')
    assert os.path.isdir(build_dir)

    artifacts = os.listdir(build_dir)
    assert len(artifacts) == 1
    wheel_file = artifacts[0]

    assert wheel_file == 'my_app-1.2.3-py2.py3-none-any.whl'

    extraction_directory = os.path.join(os.path.dirname(new_project_root_elsewhere), '_archive')
    os.mkdir(extraction_directory)

    with zipfile.ZipFile(os.path.join(build_dir, wheel_file), 'r') as zip_archive:
        zip_archive.extractall(extraction_directory)

    metadata_directory = os.path.join(extraction_directory, 'my_app-1.2.3.dist-info')
    assert os.path.isdir(metadata_directory)

    package_directory = os.path.join(extraction_directory, 'my_app')
    assert os.path.isdir(package_directory)
    assert len(os.listdir(package_directory)) == 4

    assert os.path.isfile(os.path.join(package_directory, '__init__.py'))
    assert os.path.isfile(os.path.join(package_directory, 'foo.py'))
    assert os.path.isfile(os.path.join(package_directory, 'bar.py'))
    assert os.path.isfile(os.path.join(package_directory, 'baz.py'))


def test_metadata(new_project_metadata):
    build_project('-t', 'wheel')

    build_dir = os.path.join(new_project_metadata, 'dist')
    assert os.path.isdir(build_dir)

    artifacts = os.listdir(build_dir)
    assert len(artifacts) == 1
    wheel_file = artifacts[0]

    assert wheel_file == 'my_app-1.2.3-py2.py3-none-any.whl'

    extraction_directory = os.path.join(os.path.dirname(new_project_metadata), '_archive')
    os.mkdir(extraction_directory)

    with zipfile.ZipFile(os.path.join(build_dir, wheel_file), 'r') as zip_archive:
        zip_archive.extractall(extraction_directory)

    metadata_directory = os.path.join(extraction_directory, 'my_app-1.2.3.dist-info')
    assert os.path.isdir(metadata_directory)

    package_directory = os.path.join(extraction_directory, 'my_app')
    assert os.path.isdir(package_directory)
    assert len(os.listdir(package_directory)) == 4

    assert os.path.isfile(os.path.join(package_directory, '__init__.py'))
    assert os.path.isfile(os.path.join(package_directory, 'foo.py'))
    assert os.path.isfile(os.path.join(package_directory, 'bar.py'))
    assert os.path.isfile(os.path.join(package_directory, 'baz.py'))

    metadata_file = os.path.join(metadata_directory, 'METADATA')
    with open(metadata_file, encoding='utf-8') as f:
        contents = f.read()

        assert f'Project-URL: foo, https://github.com/bar/baz#{git("rev-parse", "HEAD")}' in contents
