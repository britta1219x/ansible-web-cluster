# 基于 Ansible 的 Web 集群自动化部署

## 项目简介

使用 Ansible 实现 3 节点 Web 高可用集群的全自动化部署，一键完成环境初始化、Nginx 部署、Keepalived 主备配置及健康检查，部署耗时约 10 分钟。

## 架构图
VIP: 192.168.127.200
                       │
      ┌────────────────┴────────────────┐
      │                                 │
[node1] MASTER                    [node2] BACKUP
 Keepalived + Nginx                Keepalived + Nginx
      │                                 │
      └──────────────┬──────────────────┘
                     │
               [node3] Web
                  Nginx
## 技术栈

- **Ansible** — 自动化部署与配置管理
- **Nginx** — Web 服务与反向代理
- **Keepalived** — VIP 主备漂移
- **Rocky Linux 10** — 运行环境
- **Python** — 自定义 Ansible Module

## 项目结构
ansible-web-cluster/

├── inventory/

│   └── hosts.ini          # 节点定义与分组

├── roles/

│   ├── common/            # 系统初始化（防火墙、时区、依赖）

│   ├── nginx/             # Nginx 安装与配置下发

│   └── keepalived/        # Keepalived 主备配置

├── custom_module/

│   └── check_node_health.py  # 自定义健康检查 Module

├── site.yml               # 主入口 Playbook

└── ansible.cfg
## 核心功能

- **一键部署**：`ansible-playbook site.yml` 完成全集群初始化
- **Jinja2 模板**：动态生成 Keepalived / Nginx 配置文件，主备节点差异化下发
- **VIP 漂移**：主节点故障后 VIP 自动切换至备节点，切换时间 < 3s
- **Handlers 热更新**：Nginx 配置变更触发 reload，零停机生效
- **自定义 Module**：Python 实现节点健康检查，输出 Nginx / Keepalived / VIP 状态

## 快速开始

### 环境要求

- Ansible 控制节点 1 台
- Rocky Linux 节点 3 台
- 控制节点到所有节点 SSH 免密登录

### 修改 inventory

```ini
# inventory/hosts.ini
[webservers]
node1 ansible_host=192.168.x.101
node2 ansible_host=192.168.x.102
node3 ansible_host=192.168.x.103

[lb]
node1 keepalived_state=MASTER keepalived_priority=100
node2 keepalived_state=BACKUP  keepalived_priority=90
```

### 修改 VIP 地址

```yaml
# roles/keepalived/vars/main.yml
vip: 192.168.x.200  # 改为同网段未使用的 IP
```

### 一键部署

```bash
ansible-playbook site.yml
```

### 验证 VIP 漂移

```bash
# 停止主节点 Keepalived
ssh root@node1 "systemctl stop keepalived"

# 确认 VIP 漂移到备节点
ssh root@node2 "ip addr show | grep <VIP>"

# 服务访问不中断
curl http://<VIP>
```

## 部署效果
PLAY RECAP

node1 : ok=20  changed=5  failed=0

node2 : ok=20  changed=5  failed=0

node3 : ok=14  changed=1  failed=0
健康检查输出：Node: node1 | Nginx: active | Keepalived: active | VIP: active

Node: node2 | Nginx: active | Keepalived: active | VIP: standby

Node: node3 | Nginx: active | Keepalived: N/A    | VIP: standby
