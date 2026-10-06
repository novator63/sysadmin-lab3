#!/usr/bin/python
DOCUMENTATION = r"""
---
module: lab_host_facts
short_description: Gather basic host facts
description:
  - Collects host identity and system information.
  - Returns data under ansible_facts.lab_host.
  - Does not modify the managed host.
options: {}
author:
  - Pachkalov
"""

EXAMPLES = r"""
- name: Gather lab facts
  lab_host_facts:

- name: Display hostname
  ansible.builtin.debug:
    var: ansible_facts['lab_host']['hostname']
"""

RETURN = r"""
ansible_facts:
  description: Facts added to the managed host.
  returned: success
  type: dict
  contains:
    lab_host:
      description: Host information collected for the lab.
      type: dict
      returned: always
      contains:
        hostname:
          description: Hostname.
          type: str
          returned: always
        system:
          description: Operating system family.
          type: str
          returned: always
        kernel:
          description: Kernel release.
          type: str
          returned: always
        architecture:
          description: Machine architecture.
          type: str
          returned: always
        cpu_count:
          description: Logical CPU count, or null if unknown.
          type: int
          returned: always
"""

import platform
import os

from ansible.module_utils.basic import AnsibleModule


def main():
    module = AnsibleModule(
        argument_spec={},
        supports_check_mode=True,
    )

    facts = {
        "hostname": platform.node(),
        "system": platform.system(),
        "kernel": platform.release(),
        "architecture": platform.machine(),
        "cpu_count": os.cpu_count(),
    }

    module.exit_json(
        changed=False,
        ansible_facts={"lab_host": facts},
    )


if __name__ == "__main__":
    main()