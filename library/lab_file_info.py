#!/usr/bin/python
DOCUMENTATION = r"""
---
module: lab_file_info
short_description: Read file metadata
description:
  - Returns file existence, size and permissions.
  - Follows symbolic links and does not modify files.
options:
  path:
    description:
      - Path to inspect on the managed host.
    type: path
    required: true
author:
  - Pachkalov
"""

EXAMPLES = r"""
- name: Inspect nginx configuration
  lab_file_info:
    path: /etc/nginx/nginx.conf
  register: nginx_config
"""

RETURN = r"""
file_info:
  description: Metadata of the requested path.
  returned: success
  type: dict
  contains:
    path:
      description: Requested path.
      type: str
      returned: always
    exists:
      description: Whether the target exists.
      type: bool
      returned: always
    size_bytes:
      description: File size in bytes.
      type: int
      returned: when the target exists
    mode:
      description: Permissions in octal notation.
      type: str
      returned: when the target exists
"""

import os

from ansible.module_utils.basic import AnsibleModule


def main():
    module = AnsibleModule(
        argument_spec={
            "path": {"type": "path", "required": True},
        },
        supports_check_mode=True,
    )

    path = module.params["path"]

    try:
        stat_result = os.stat(path)
    except FileNotFoundError:
        module.exit_json(
            changed=False,
            file_info={"path": path, "exists": False},
        )
    except OSError as exc:
        module.fail_json(
            msg=f"Cannot read file information: {exc}",
            path=path,
        )

    info = {
        "path": path,
        "exists": True,
        "size_bytes": stat_result.st_size,
        "mode": format(stat_result.st_mode & 0o7777, "04o"),
    }

    module.exit_json(changed=False, file_info=info)


if __name__ == "__main__":
    main()