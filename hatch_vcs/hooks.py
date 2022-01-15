# SPDX-FileCopyrightText: 2022-present Ofek Lev <oss@ofek.dev>
#
# SPDX-License-Identifier: MIT
from hatchling.plugin import hookimpl

from .build_hook import VCSBuildHook
from .version_source import VCSVersionSource


@hookimpl
def hatch_register_version_source():
    return VCSVersionSource


@hookimpl
def hatch_register_build_hook():
    return VCSBuildHook
