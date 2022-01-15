# hatch-vcs

| | |
| --- | --- |
| CI/CD | [![CI - Test](https://github.com/ofek/hatch-vcs/actions/workflows/test.yml/badge.svg)](https://github.com/ofek/hatch-vcs/actions/workflows/test.yml) [![CD - Build](https://github.com/ofek/hatch-vcs/actions/workflows/build.yml/badge.svg)](https://github.com/ofek/hatch-vcs/actions/workflows/build.yml) |
| Package | [![PyPI - Version](https://img.shields.io/pypi/v/hatch-vcs.svg?logo=pypi&label=PyPI&logoColor=gold)](https://pypi.org/project/hatch-vcs/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/hatch-vcs.svg?logo=python&label=Python&logoColor=gold)](https://pypi.org/project/hatch-vcs/) |
| Meta | [![code style - black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![types - Mypy](https://img.shields.io/badge/types-Mypy-blue.svg)](https://github.com/ambv/black) [![imports - isort](https://img.shields.io/badge/imports-isort-ef8336.svg)](https://github.com/pycqa/isort) [![License - MIT](https://img.shields.io/badge/license-MIT-9400d3.svg)](https://spdx.org/licenses/) [![GitHub Sponsors](https://img.shields.io/github/sponsors/ofek?logo=GitHub%20Sponsors&style=social)](https://github.com/sponsors/ofek) |

-----

This provides a plugin for [Hatch](https://github.com/ofek/hatch) that uses your preferred version control system (like Git) to determine project versions.

**Table of Contents**

- [Global dependency](#global-dependency)
- [Version source](#version-source)
  - [Version source options](#version-source-options)
- [Build hook](#build-hook)
  - [Build hook options](#build-hook-options)
- [License](#license)

## Global dependency

Ensure `hatch-vcs` is defined within the `build-system.requires` field in your `pyproject.toml` file.

```toml
[build-system]
requires = ["hatchling", "hatch-vcs"]
build-backend = "hatchling.build"
```

## Version source

The [version source plugin](https://ofek.dev/hatch/latest/plugins/version-source/) name is `vcs`.

- ***pyproject.toml***

    ```toml
    [tool.hatch.version]
    ```

- ***hatch.toml***

    ```toml
    [version]
    ```

### Version source options

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `tag-pattern` | `str` | see [code](https://github.com/pypa/setuptools_scm/blob/v6.4.0/src/setuptools_scm/config.py#L13) | A regular expression used to extract the version part from VCS tags. The pattern needs to contain either a single match group, or a group named `version`, that captures the actual version information. |
| `fallback-version` | `str` | | The version that will be used if no other method for detecting the version is successful. If not specified, unsuccessful version detection will raise an error. |
| `raw-options` | `dict` | | A table of [`setuptools-scm` parameters](https://github.com/pypa/setuptools_scm#configuration-parameters) that will override any of the options listed above. The `write_to` and `write_to_template` parameters are ignored. |

## Build hook

The [build hook plugin](https://ofek.dev/hatch/latest/plugins/build-hook/) name is `vcs`.

- ***pyproject.toml***

    ```toml
    [tool.hatch.build.hooks.vcs]
    ```

- ***hatch.toml***

    ```toml
    [build.hooks.vcs]
    ```

### Build hook options

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `version-file` | `str` | ***REQUIRED*** | The relative path to the file that gets updated with the current version. |
| `template` | `str` | | The template used to overwrite the `version-file`. See the [code](https://github.com/pypa/setuptools_scm/blob/v6.4.0/src/setuptools_scm/__init__.py#L30-L39) for the default template for each file extension. |

## License

`hatch-vcs` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
