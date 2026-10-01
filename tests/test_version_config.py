# SPDX-FileCopyrightText: 2022-present Ofek Lev <oss@ofek.dev>
#
# SPDX-License-Identifier: MIT
import warnings

import pytest

from hatch_vcs.version_source import VCSVersionSource

from .conftest import create_project


class TestTagPattern:
    def test_correct(self, new_project_basic):
        config = {'tag-pattern': '.+'}
        version_source = VCSVersionSource(new_project_basic, config)

        assert version_source.config_tag_pattern == '.+'

    def test_not_string(self, new_project_basic):
        config = {'tag-pattern': 9000}
        version_source = VCSVersionSource(new_project_basic, config)

        with pytest.raises(TypeError, match='option `tag-pattern` must be a string'):
            _ = version_source.config_tag_pattern

    def test_no_tag_pattern(self, new_project_basic):
        config = {}
        version_source = VCSVersionSource(new_project_basic, config)

        assert version_source.config_tag_pattern == ''

        # Should not raise any deprecation warnings
        with warnings.catch_warnings():
            warnings.simplefilter('error')
            _ = version_source.get_version_data()

    def test_custom_tag_pattern_get_version(self, new_project_basic):
        config = {'tag-pattern': '(?P<version>.+)'}
        version_source = VCSVersionSource(new_project_basic, config)

        assert version_source.get_version_data() == {'version': '1.2.3'}


class TestFallbackVersion:
    def test_correct(self, new_project_basic):
        config = {'fallback-version': '0.0.1'}
        version_source = VCSVersionSource(new_project_basic, config)

        assert version_source.config_fallback_version == '0.0.1'

    def test_not_string(self, new_project_basic):
        config = {'fallback-version': 9000}
        version_source = VCSVersionSource(new_project_basic, config)

        with pytest.raises(TypeError, match='option `fallback-version` must be a string'):
            _ = version_source.config_fallback_version


class TestRawOptions:
    def test_correct(self, new_project_basic):
        config = {'raw-options': {'normalize': False}}
        version_source = VCSVersionSource(new_project_basic, config)

        assert version_source.config_raw_options == {'normalize': False}

    def test_not_table(self, new_project_basic):
        config = {'raw-options': 9000}
        version_source = VCSVersionSource(new_project_basic, config)

        with pytest.raises(TypeError, match='option `raw-options` must be a table'):
            _ = version_source.config_raw_options


def test_coverage(new_project_basic):
    version_source = VCSVersionSource(new_project_basic, {})

    assert version_source.config_tag_pattern is version_source.config_tag_pattern
    assert version_source.config_fallback_version is version_source.config_fallback_version
    assert version_source.config_raw_options is version_source.config_raw_options


def test_parent_repo_error_uses_hatch_config(temp_dir):
    metadata = """\
[build-system]
requires = ["hatchling", "hatch-vcs"]
build-backend = "hatchling.build"

[project]
name = "my-app"
dynamic = ["version"]

[tool.hatch.version]
source = "vcs"
"""
    with create_project(temp_dir, metadata, nested=True) as project:
        version_source = VCSVersionSource(project, {})

        with pytest.raises(LookupError) as excinfo:
            version_source.get_version_data()

    message = str(excinfo.value)
    assert '[tool.hatch.version.raw-options]' in message
    assert 'search_parent_directories = true' in message
    assert '[tool.setuptools_scm]' not in message
    assert 'setuptools_scm.get_version' not in message
