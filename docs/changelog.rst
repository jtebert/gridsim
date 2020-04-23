=========
Changelog
=========

This documents changes for each Gridsim release. These can also be found with each `Github release <https://github.com/jtebert/gridsim/releases>`_.

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_, and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

.. contents:: Versions
  :local:
  :depth: 1

Unreleased
==========

Added
-----

- :class:`~gridsim.message.Message` now has "truthiness": null messages are ``False`` and non-null messages are ``True``.
- Created this changelog

Changed
-------

- ``Message.tx_id()`` has been renamed to the (more informative) :meth:`~gridsim.message.Message.sender`.

Removed
-------

- ``Message.is_null`` has been removed. Instead, directly use the boolean conversion described above.

`0.2 <https://github.com/jtebert/gridsim/releases/tag/v0.2>`_ (2020-04-20)
=============================================================================

Added
-----

- Worlds now have environments (images) that can be sensed by Robots.
- Documentation has been improved, now with complete instructions for basic setup and usage.