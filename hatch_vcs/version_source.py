# SPDX-FileCopyrightText: 2022-present Ofek Lev <oss@ofek.dev>
#
# SPDX-License-Identifier: MIT
from hatchling.version.source.plugin.interface import VersionSourceInterface


class VCSVersionSource(VersionSourceInterface):
    PLUGIN_NAME = 'vcs'

    def __init__(self, *args, **kwargs):
        super(VCSVersionSource, self).__init__(*args, **kwargs)

        self.__config_tag_pattern = None
        self.__config_fallback_version = None
        self.__config_raw_options = None

    @property
    def config_tag_pattern(self):
        if self.__config_tag_pattern is None:
            tag_pattern = self.config.get('tag-pattern', '')
            if not isinstance(tag_pattern, str):
                raise TypeError('option `tag-pattern` must be a string')

            self.__config_tag_pattern = tag_pattern

        return self.__config_tag_pattern

    @property
    def config_fallback_version(self):
        if self.__config_fallback_version is None:
            fallback_version = self.config.get('fallback-version', '')
            if not isinstance(fallback_version, str):
                raise TypeError('option `fallback-version` must be a string')

            self.__config_fallback_version = fallback_version

        return self.__config_fallback_version

    @property
    def config_raw_options(self):
        if self.__config_raw_options is None:
            raw_options = self.config.get('raw-options', {})
            if not isinstance(raw_options, dict):
                raise TypeError('option `raw-options` must be a table')

            self.__config_raw_options = raw_options

        return self.__config_raw_options

    def get_version_data(self):
        from copy import deepcopy

        from setuptools_scm import get_version

        config = deepcopy(self.config_raw_options)
        config['root'] = self.root

        config.setdefault('tag_regex', self.config_tag_pattern)
        config.setdefault('fallback_version', self.config_fallback_version)

        # Writing only occurs when the build hook is enabled
        config.pop('write_to', None)
        config.pop('write_to_template', None)

        version = get_version(**config)
        return {'version': version}
