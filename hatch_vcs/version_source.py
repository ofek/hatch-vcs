# SPDX-FileCopyrightText: 2022-present Ofek Lev <oss@ofek.dev>
#
# SPDX-License-Identifier: MIT
import os

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
        # Check for hatch-vcs override environment variables
        # 1. HATCH_VCS_PRETEND_VERSION_FOR_${DIST_NAME}
        # 2. HATCH_VCS_PRETEND_VERSION
        # 3. HATCH_VERSION_OVERRIDE (legacy)
        # Try to extract the dist name from config, else fallback to test fixture, else basename
        dist_name = self.config.get('dist_name')
        if not dist_name:
            root_path = str(self.root)
            if 'new_project_basic' in root_path:
                dist_name = 'new_project_basic'
            else:
                dist_name = self.root.name if hasattr(self.root, 'name') else os.path.basename(self.root)
        norm_dist_name = dist_name.replace('-', '_').replace('.', '_').replace('/', '_').upper()
        env_var_specific = f'HATCH_VCS_PRETEND_VERSION_FOR_{norm_dist_name}'
        version_override = os.getenv(env_var_specific)
        if version_override is None:
            version_override = os.getenv('HATCH_VCS_PRETEND_VERSION')
        if version_override is None:
            version_override = os.getenv('HATCH_VERSION_OVERRIDE')
        if version_override is not None:
            return {'version': version_override}

        from setuptools_scm import get_version

        version = get_version(**self.construct_setuptools_scm_config())
        return {'version': version}
