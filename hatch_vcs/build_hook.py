# SPDX-FileCopyrightText: 2022-present Ofek Lev <oss@ofek.dev>
#
# SPDX-License-Identifier: MIT
from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class VCSBuildHook(BuildHookInterface):
    PLUGIN_NAME = 'vcs'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__config_version_file = None
        self.__config_template = None

    @property
    def config_version_file(self):
        if self.__config_version_file is None:
            version_file = self.config.get('version-file', '')
            if not isinstance(version_file, str):
                raise TypeError(f'Option `version-file` for build hook `{self.PLUGIN_NAME}` must be a string')
            elif not version_file:
                raise ValueError(f'Option `version-file` for build hook `{self.PLUGIN_NAME}` is required')

            self.__config_version_file = version_file

        return self.__config_version_file

    @property
    def config_template(self):
        if self.__config_template is None:
            template = self.config.get('template', '')
            if not isinstance(template, str):
                raise TypeError(f'Option `template` for build hook `{self.PLUGIN_NAME}` must be a string')

            self.__config_template = template

        return self.__config_template

    def initialize(self, version, build_data):
        from setuptools_scm import dump_version

        dump_version(self.root, self.metadata.version, self.config_version_file, template=self.config_template)

        build_data['artifacts'].append(f'/{self.config_version_file}')
