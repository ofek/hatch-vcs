# SPDX-FileCopyrightText: 2022-present Ofek Lev <oss@ofek.dev>
#
# SPDX-License-Identifier: MIT
import logging
import os
from contextlib import contextmanager
from functools import cached_property

try:
    from importlib.metadata import entry_points
except ImportError:
    from importlib_metadata import entry_points  # type: ignore

import pathspec
from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class SuppressMessage(logging.Handler):
    def __init__(self, level=logging.NOTSET, *, ignore_message: str):
        self.ignore_message = ignore_message
        super().__init__(level=level)

    def filter(self, record: logging.LogRecord) -> bool:  # noqa: A003
        if record.msg == self.ignore_message:
            return False
        return True

    @contextmanager
    def inject(self, logger: logging.Logger):
        logger.addHandler(self)
        yield
        logger.removeHandler(self)


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

    @cached_property
    def config_detect_files(self):
        detect_files = self.config.get('detect-files', False)
        if not isinstance(detect_files, bool):
            raise TypeError(f'Option `detect-files` for build hook `{self.PLUGIN_NAME}` must be a boolean')

        return detect_files

    def initialize(self, version, build_data):
        from setuptools_scm import dump_version

        if self.config_detect_files:
            file_finders = entry_points().select(group='setuptools.file_finders', name='setuptools_scm')
            file_finder = next(iter(file_finders)).load()

            # setuptools_scm doesn't provide an easy way to predict noise
            suppressor = SuppressMessage(ignore_message="listing git files failed - pretending there aren't any")

            # If working from a repository, retrieve files; empty if building from archive or sdist
            with suppressor.inject(logging.getLogger('setuptools_scm')):
                vcs_files = {os.path.relpath(f, self.root) for f in file_finder(self.root)}

            if vcs_files:
                # Artifacts are included after exclusions are applied, so add VCS-identified files
                # to artifacts
                included = vcs_files - set(self.build_config.exclude_spec.match_files(vcs_files))
                build_data['artifacts'].extend(f'/{f}' for f in sorted(included))

                # Exclude everything else, unless overridden as an artifact or force-include
                self.build_config.exclude_spec.patterns[:] = [pathspec.GitIgnorePattern('*')]

        kwargs = {}
        if self.config_template:
            kwargs['template'] = self.config_template
        dump_version(self.root, self.metadata.version, self.config_version_file, **kwargs)

        build_data['artifacts'].append(f'/{self.config_version_file}')
