=============================================
OpenShift Virtualization Collection for Ansible Release Notes
=============================================

.. contents:: Topics

This changelog describes changes after version 1.0.0.

v2.1.0
======

Release Summary
---------------

The redhat_vmi_info module was added to this collection.

Minor Changes
-------------

- Run integration tests in random namespaces `#130 <https://github.com/redhat/redhat.openshift_virtualization/pull/130>`_
- feat: Add redhat_vmi_info module `#129 <https://github.com/redhat/redhat.openshift_virtualization/pull/129>`_

v2.0.0
======

Release Summary
---------------

The deprecation of the 'connections' parameter is continued by dropping support for multiple connections. Inventory configurations with a single connection remain working for now. This backwards compatibility will be dropped in version 3.0.0 of the collection.
Inventory source caching is now working and allows to reduce the load on the control plane of a cluster from which an inventory is built.

Minor Changes
-------------

- Several small cleanups `#122 <https://github.com/redhat/redhat.openshift_virtualization/pull/122>`_
- feat(redhat_vm): Add support for RunStrategy `#124 <https://github.com/redhat/redhat.openshift_virtualization/pull/124>`_

Breaking Changes / Porting Guide
--------------------------------

- chore: Bump version to 2.0.0 `#125 <https://github.com/redhat/redhat.openshift_virtualization/pull/125>`_
- cleanup(inventory): Drop support for multiple connections `#117 <https://github.com/redhat/redhat.openshift_virtualization/pull/117>`_

Bugfixes
--------

- fix(inventory): Fix inventory source caching `#119 <https://github.com/redhat/redhat.openshift_virtualization/pull/119>`_

v1.5.0
======

Release Summary
---------------

Support for stopped VMs, deprecation of the 'connections' parameter and many cleanups.

Major Changes
-------------

- chore: Update supported ansible-openshift_virtualization versions to >=2.15 `#105 <https://github.com/redhat/redhat.openshift_virtualization/pull/105>`_
- feat,test(inventory): Support listing stopped VMs and major rework of unit tests  `#114 <https://github.com/redhat/redhat.openshift_virtualization/pull/114>`_

Minor Changes
-------------

- Bump e2e software versions `#109 <https://github.com/redhat/redhat.openshift_virtualization/pull/109>`_
- Make redhat_vm tests more robust `#103 <https://github.com/redhat/redhat.openshift_virtualization/pull/103>`_
- Several minor improvements `#115 <https://github.com/redhat/redhat.openshift_virtualization/pull/115>`_
- chore: Ensure compatibility with kubernetes.openshift_virtualization >=3.1.0,<6.0.0 `#111 <https://github.com/redhat/redhat.openshift_virtualization/pull/111>`_
- redhat_vm integration tests: changed ssh key type to RSA for FIPS mode `#108 <https://github.com/redhat/redhat.openshift_virtualization/pull/108>`_

Bugfixes
--------

- fix(tests,redhat_vm): Fix assertion in verify.yml `#106 <https://github.com/redhat/redhat.openshift_virtualization/pull/106>`_

v1.4.0
======

Release Summary
---------------

Compatibility with kubernetes.openshift_virtualization >=3.1.0,<4.1.0 and some minor enhancements.

Minor Changes
-------------

- Provide links for docsite and improve docs by adding markup `#95 <https://github.com/redhat/redhat.openshift_virtualization/pull/95>`_
- cleanup: Cleanup YAML passed to k8s module `#88 <https://github.com/redhat/redhat.openshift_virtualization/pull/88>`_
- docs: Use proper type for connections parameter `#90 <https://github.com/redhat/redhat.openshift_virtualization/pull/90>`_
- feat(kubevirt_vm_info): Set wait_condition based on running `#91 <https://github.com/redhat/redhat.openshift_virtualization/pull/91>`_

Bugfixes
--------

- fix(redhat_vm): Set wait_condition based on running `#89 <https://github.com/redhat/redhat.openshift_virtualization/pull/89>`_
- fix: Ensure compatibility with kubernetes.openshift_virtualization >=3.10,<4.1.0 `#100 <https://github.com/redhat/redhat.openshift_virtualization/pull/100>`_

v1.3.2
======

Release Summary
---------------

No functional changes, hotfix release to retrigger the downstream build and to keep in sync with Ansible Automation Hub.

v1.3.1
======

Release Summary
---------------

No functional changes, only updates to the shipped documentation.

v1.3.0
======

Minor Changes
-------------

- feat: Add append_base_domain option to connections `#72 <https://github.com/redhat/redhat.openshift_virtualization/pull/72>`_
- feat: Give secondary interfaces a higher priority over services `#76 <https://github.com/redhat/redhat.openshift_virtualization/pull/76>`_

Bugfixes
--------

- feat: Set ansible_connection to winrm for Windows hosts `#75 <https://github.com/redhat/redhat.openshift_virtualization/pull/75>`_
- fix: Explicity set ansible_port `#70 <https://github.com/redhat/redhat.openshift_virtualization/pull/70>`_
- fix: Return early to avoid adding empty groups. `#73 <https://github.com/redhat/redhat.openshift_virtualization/pull/73>`_

v1.2.3
======

Release Summary
---------------

No functional changes, hotfix release to retrigger the downstream build and to keep in sync with Ansible Automation Hub.

v1.2.2
======

Release Summary
---------------

No functional changes, only cleanup of files included in the release tarball and vendoring of documentation fragments.

v1.2.1
======

Release Summary
---------------

Mostly code cleanups and dependency updates to ensure compatibility with KubeVirt >= 1.1.0

v1.2.0
======

Release Summary
---------------

Not released due to issues in the release process

v1.1.0
======

Minor Changes
-------------

- Add kubevirt_vm_info module to describe existing VirtualMachines
- inventory: Allow to control creation of additional groups
- inventory: Drop creation of the namespace_vmis_group as it is redundant

v1.0.0
======

Release Summary
---------------

Initial release
