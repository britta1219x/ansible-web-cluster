#!/usr/bin/python3

from ansible.module_utils.basic import AnsibleModule
import subprocess


def main():
    module = AnsibleModule(
        argument_spec=dict(
            vip=dict(type='str', required=True),
        ),
        supports_check_mode=True
    )

    result = {
        "changed": False,
        "node": module.get_bin_path('hostname', required=True),
        "nginx_status": "unknown",
        "keepalived_status": "unknown",
        "vip_status": "unknown"
    }

    try:
        # 检查 Nginx 状态
        nginx = subprocess.run(['systemctl', 'is-active', 'nginx'],
                               capture_output=True, text=True)
        result["nginx_status"] = nginx.stdout.strip()

        # 检查 Keepalived 状态
        keepalived = subprocess.run(['systemctl', 'is-active', 'keepalived'],
                                    capture_output=True, text=True)
        result["keepalived_status"] = keepalived.stdout.strip()

        # 检查 VIP 是否在本机（VIP 由 inventory 的 vip 变量传入，全仓库保持一致）
        ip_check = subprocess.run(['ip', 'addr'], capture_output=True, text=True)
        if module.params['vip'] in ip_check.stdout:
            result["vip_status"] = "active"
        else:
            result["vip_status"] = "standby"

    except Exception as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)


if __name__ == '__main__':
    main()
