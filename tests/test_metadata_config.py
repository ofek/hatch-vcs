# SPDX-FileCopyrightText: 2022-present Ofek Lev <oss@ofek.dev>
#
# SPDX-License-Identifier: MIT
import pytest

from hatch_vcs.metadata_hook import VCSMetadataHook


class TestURLs:
    def test_correct(self, new_project_basic):
        config = {'urls': {'foo': 'url'}}
        metadata_hook = VCSMetadataHook(new_project_basic, config)

        assert metadata_hook.config_urls == {'foo': 'url'}

    def test_not_table(self, new_project_basic):
        config = {'urls': 9000}
        metadata_hook = VCSMetadataHook(new_project_basic, config)

        with pytest.raises(TypeError, match='option `urls` must be a table'):
            _ = metadata_hook.config_urls

    def test_url_not_string(self, new_project_basic):
        config = {'urls': {'foo': 9000}}
        metadata_hook = VCSMetadataHook(new_project_basic, config)

        with pytest.raises(TypeError, match='URL `foo` in option `urls` must be a string'):
            _ = metadata_hook.config_urls


def test_coverage(new_project_basic):
    metadata_hook = VCSMetadataHook(new_project_basic, {})

    assert metadata_hook.config_urls is metadata_hook.config_urls
