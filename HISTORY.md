# History

-----

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

## 0.5.0 - 2025-05-27

***Changed:***

- Drop support for Python 3.8

***Added:***

- Officially support Python 3.13
- Avoid a deprecation warning emitted by a dependency when using the `tag-pattern` option

## 0.4.0 - 2023-11-06

***Changed:***

- Drop support for Python 3.7

***Added:***

- Officially support Python 3.12

***Fixed:***

- Prevent `UserWarning` when a template is not defined explicitly

## 0.3.0 - 2022-12-10

***Changed:***

- Drop support for Python 2

***Added:***

- Add a metadata hook for injecting VCS metadata
- Bump the minimum supported version of Hatchling

## 0.2.1 - 2022-12-06

***Fixed:***

- Allow `root` in `raw-options`

## 0.2.0 - 2022-03-18

***Added:***

- Bump the minimum supported version of Hatchling

***Fixed:***

- Fix handling of `fallback_version` default value

## 0.1.0 - 2022-01-18

This is the initial public release.
