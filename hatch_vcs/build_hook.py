# SPDX-FileCopyrightText: 2022-present Ofek Lev <oss@ofek.dev>
#
# SPDX-License-Identifier: MIT
from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class VCSBuildHook(BuildHookInterface):
    PLUGIN_NAME = 'vcs'

    def __init__(self, *args, **kwargs):
        super(VCSBuildHook, self).__init__(*args, **kwargs)

        self.__config_version_file = None
        self.__config_template = None

    @property
    def config_version_file(self):
        if self.__config_version_file is None:
            version_file = self.config.get('version-file', '')
            if not isinstance(version_file, str):
                raise TypeError('Option `version-file` for build hook `{}` must be a string'.format(self.PLUGIN_NAME))
            elif not version_file:
                raise ValueError('Option `version-file` for build hook `{}` is required'.format(self.PLUGIN_NAME))

            self.__config_version_file = version_file

        return self.__config_version_file

    @property
    def config_template(self):
        if self.__config_template is None:
            template = self.config.get('template', '')
            if not isinstance(template, str):
                raise TypeError('Option `template` for build hook `{}` must be a string'.format(self.PLUGIN_NAME))

            self.__config_template = template

        return self.__config_template

    def initialize(self, version, build_data):
        from setuptools_scm import dump_version

        dump_version(self.root, self.metadata.version, self.config_version_file, template=self.config_template)

        build_data['artifacts'].append('/{}'.format(self.config_version_file))
