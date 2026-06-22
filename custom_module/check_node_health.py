#!/usr/bin/python3

from ansible.module_utils.basic import AnsibleModule
import subprocess
import json

def main():
    module = AnsibleModule(
        argument_spec=dict(),
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

        # 检查 VIP 是否在本机
        ip_check = subprocess.run(['ip', 'addr'], capture_output=True, text=True)
        if "192.168.56.200" in ip_check.stdout:   # 修改成你的VIP
            result["vip_status"] = "active"
        else:
            result["vip_status"] = "standby"

    except Exception as e:
        module.fail_json(msg=str(e))

    module.exit_json(**result)

if __name__ == '__main__':
    main()
