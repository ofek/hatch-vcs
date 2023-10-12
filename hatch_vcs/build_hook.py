# SPDX-FileCopyrightText: 2022-present Ofek Lev <oss@ofek.dev>
#
# SPDX-License-Identifier: MIT
from functools import cached_property

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class VCSBuildHook(BuildHookInterface):
    PLUGIN_NAME = 'vcs'

    @cached_property
    def config_version_file(self):
        version_file = self.config.get('version-file')
        if not version_file:
            raise ValueError(f'Option `version-file` for build hook `{self.PLUGIN_NAME}` is required')
        elif not isinstance(version_file, str):
            raise TypeError(f'Option `version-file` for build hook `{self.PLUGIN_NAME}` must be a string')

        return version_file

    @cached_property
    def config_template(self):
        template = self.config.get('template')
        if template is not None and not isinstance(template, str):
            raise TypeError(f'Option `template` for build hook `{self.PLUGIN_NAME}` must be a string')
        return template

    def initialize(self, version, build_data):
        from setuptools_scm import dump_version

        kwargs = {}
        if self.config_template:
            kwargs['template'] = self.config_template
        dump_version(self.root, self.metadata.version, self.config_version_file, **kwargs)

        build_data['artifacts'].append(f'/{self.config_version_file}')
