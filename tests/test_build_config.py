# SPDX-FileCopyrightText: 2022-present Ofek Lev <oss@ofek.dev>
#
# SPDX-License-Identifier: MIT
import os

import pytest

from hatch_vcs.build_hook import VCSBuildHook


class TestVersionFile:
    def test_correct(self, new_project_basic):
        config = {'version-file': 'foo/_version.py'}
        build_dir = os.path.join(new_project_basic, 'dist')
        build_hook = VCSBuildHook(new_project_basic, config, None, None, build_dir, 'wheel')

        assert build_hook.config_version_file == 'foo/_version.py'

    def test_not_string(self, new_project_basic):
        config = {'version-file': 9000}
        build_dir = os.path.join(new_project_basic, 'dist')
        build_hook = VCSBuildHook(new_project_basic, config, None, None, build_dir, 'wheel')

        with pytest.raises(TypeError, match='Option `version-file` for build hook `vcs` must be a string'):
            _ = build_hook.config_version_file

    def test_missing(self, new_project_basic):
        config = {}
        build_dir = os.path.join(new_project_basic, 'dist')
        build_hook = VCSBuildHook(new_project_basic, config, None, None, build_dir, 'wheel')

        with pytest.raises(ValueError, match='Option `version-file` for build hook `vcs` is required'):
            _ = build_hook.config_version_file


class TestTemplate:
    def test_correct(self, new_project_basic):
        config = {'template': '__version__ = {version!r}'}
        build_dir = os.path.join(new_project_basic, 'dist')
        build_hook = VCSBuildHook(new_project_basic, config, None, None, build_dir, 'wheel')

        assert build_hook.config_template == '__version__ = {version!r}'

    def test_not_string(self, new_project_basic):
        config = {'template': 9000}
        build_dir = os.path.join(new_project_basic, 'dist')
        build_hook = VCSBuildHook(new_project_basic, config, None, None, build_dir, 'wheel')

        with pytest.raises(TypeError, match='Option `template` for build hook `vcs` must be a string'):
            _ = build_hook.config_template


def test_coverage(new_project_basic):
    config = {'version-file': 'foo/_version.py'}
    build_dir = os.path.join(new_project_basic, 'dist')
    build_hook = VCSBuildHook(new_project_basic, config, None, None, build_dir, 'wheel')

    assert build_hook.config_version_file is build_hook.config_version_file
    assert build_hook.config_template is build_hook.config_template
