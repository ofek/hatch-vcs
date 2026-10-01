# SPDX-FileCopyrightText: 2022-present Ofek Lev <oss@ofek.dev>
#
# SPDX-License-Identifier: MIT
from hatchling.version.source.plugin.interface import VersionSourceInterface


class VCSVersionSource(VersionSourceInterface):
    PLUGIN_NAME = 'vcs'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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

    def construct_setuptools_scm_config(self):
        from copy import deepcopy

        config = deepcopy(self.config_raw_options)
        config.setdefault('root', self.root)

        # Only set for non-empty strings
        if self.config_tag_pattern:
            config['tag_regex'] = self.config_tag_pattern

        # Only set for non-empty strings
        if self.config_fallback_version:
            config['fallback_version'] = self.config_fallback_version

        # Writing only occurs when the build hook is enabled
        config.pop('write_to', None)
        config.pop('write_to_template', None)
        return config

    def get_version_data(self):
        from setuptools_scm import get_version

        try:
            version = get_version(**self.construct_setuptools_scm_config())
        except LookupError as exc:
            raise LookupError(_rewrite_setuptools_scm_hint(str(exc))) from exc
        return {'version': version}


def _rewrite_setuptools_scm_hint(message):
    """Point setuptools-scm's parent-repo hints at Hatch config keys."""
    rewritten = message.replace('[tool.setuptools_scm]', '[tool.hatch.version.raw-options]')
    return rewritten.replace(
        '   setuptools_scm.get_version(relative_to=__file__)',
        '   [tool.hatch.version.raw-options]\n   relative_to = "pyproject.toml"',
    )
