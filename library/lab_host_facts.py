#!/usr/bin/python

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