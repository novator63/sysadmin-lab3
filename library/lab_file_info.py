#!/usr/bin/python

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