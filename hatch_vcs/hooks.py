# SPDX-FileCopyrightText: 2022-present Ofek Lev <oss@ofek.dev>
#
# SPDX-License-Identifier: MIT
from hatchling.plugin import hookimpl

from hatch_vcs.build_hook import VCSBuildHook
from hatch_vcs.metadata_hook import VCSMetadataHook
from hatch_vcs.version_source import VCSVersionSource


@hookimpl
def hatch_register_version_source():
    return VCSVersionSource


@hookimpl
def hatch_register_build_hook():
    return VCSBuildHook


@hookimpl
def hatch_register_metadata_hook():
    return VCSMetadataHook
