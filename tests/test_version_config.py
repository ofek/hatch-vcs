# SPDX-FileCopyrightText: 2022-present Ofek Lev <oss@ofek.dev>
#
# SPDX-License-Identifier: MIT
import warnings

import pytest

from hatch_vcs.version_source import VCSVersionSource


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

    def test_write_to_removed_from_config(self, new_project_basic):
        config = {'raw-options': {'write_to': 'foo.py', 'write_to_template': 'bar', 'other': True}}
        version_source = VCSVersionSource(new_project_basic, config)
        result = version_source.construct_setuptools_scm_config()
        assert 'write_to' not in result
        assert 'write_to_template' not in result
        assert 'other' in result


def test_coverage(new_project_basic):
    version_source = VCSVersionSource(new_project_basic, {})

    assert version_source.config_tag_pattern == ''
    assert version_source.config_fallback_version == ''
    assert version_source.config_raw_options == {}


def test_get_version_data_calls_get_version(monkeypatch, new_project_basic):
    config = {}
    version_source = VCSVersionSource(new_project_basic, config)
    monkeypatch.delenv('HATCH_VERSION_OVERRIDE', raising=False)

    # Patch setuptools_scm.get_version to a dummy function
    def dummy_get_version(**kwargs):
        return 'dummy-version'

    monkeypatch.setattr('setuptools_scm.get_version', dummy_get_version)
    assert version_source.get_version_data() == {'version': 'dummy-version'}


def test_get_version_data_env_override(monkeypatch, new_project_basic):
    config = {}
    version_source = VCSVersionSource(new_project_basic, config)
    monkeypatch.setenv('HATCH_VERSION_OVERRIDE', 'override-version')
    monkeypatch.delenv('HATCH_VCS_PRETEND_VERSION', raising=False)
    monkeypatch.delenv('HATCH_VCS_PRETEND_VERSION_FOR_NEW_PROJECT_BASIC', raising=False)
    assert version_source.get_version_data() == {'version': 'override-version'}


def test_get_version_data_setuptools_scm_pretend_version(monkeypatch, new_project_basic):
    config = {}
    version_source = VCSVersionSource(new_project_basic, config)
    monkeypatch.setenv('HATCH_VCS_PRETEND_VERSION', 'pretend-version')
    monkeypatch.delenv('HATCH_VERSION_OVERRIDE', raising=False)
    monkeypatch.delenv('HATCH_VCS_PRETEND_VERSION_FOR_NEW_PROJECT_BASIC', raising=False)
    assert version_source.get_version_data() == {'version': 'pretend-version'}


def test_get_version_data_setuptools_scm_pretend_version_for_dist(monkeypatch, new_project_basic):
    config = {'dist_name': 'new_project_basic'}
    version_source = VCSVersionSource(new_project_basic, config)
    # The normalized dist name for the test fixture is 'new_project_basic', uppercase and underscores
    monkeypatch.setenv('HATCH_VCS_PRETEND_VERSION_FOR_NEW_PROJECT_BASIC', 'specific-pretend-version')
    monkeypatch.setenv('HATCH_VCS_PRETEND_VERSION', 'pretend-version')
    monkeypatch.setenv('HATCH_VERSION_OVERRIDE', 'override-version')
    assert version_source.get_version_data() == {'version': 'specific-pretend-version'}


def test_get_version_data_env_precedence(monkeypatch, new_project_basic):
    config = {'dist_name': 'new_project_basic'}
    version_source = VCSVersionSource(new_project_basic, config)
    monkeypatch.setenv('HATCH_VCS_PRETEND_VERSION_FOR_NEW_PROJECT_BASIC', 'specific-pretend-version')
    monkeypatch.setenv('HATCH_VCS_PRETEND_VERSION', 'pretend-version')
    monkeypatch.setenv('HATCH_VERSION_OVERRIDE', 'override-version')
    # Should prefer the specific dist override
    assert version_source.get_version_data() == {'version': 'specific-pretend-version'}
    monkeypatch.delenv('HATCH_VCS_PRETEND_VERSION_FOR_NEW_PROJECT_BASIC', raising=False)
    # Should prefer the generic override
    assert version_source.get_version_data() == {'version': 'pretend-version'}
    monkeypatch.delenv('HATCH_VCS_PRETEND_VERSION', raising=False)
    # Should prefer the legacy override
    assert version_source.get_version_data() == {'version': 'override-version'}
