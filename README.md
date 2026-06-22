# 基于 Ansible 的 Web 高可用集群自动化部署

**技术栈**：Ansible + Rocky Linux 9 + Nginx + Keepalived + Docker

**项目目标**：
- 实现 3 节点 Web 集群一键自动化部署
- Nginx 负载均衡 + Keepalived VIP 高可用
- 配置自动下发 + 服务热更新 (Handlers)
- 自定义 Ansible Module 做节点健康检查

**部署时间**：约 8-10 分钟完成 3 节点初始化

## 快速开始

1. 修改 inventory/hosts.ini 中的 IP 地址和认证信息
2. 配置 Controller 到各节点的 SSH 免密登录（推荐）
3. 执行部署命令： ansible-playbook -i inventory/hosts.ini site.yml

## 项目亮点
- 使用 Roles 进行模块化管理
- Handlers 实现 Nginx 配置修改后自动热重载
- 自定义 Module 实现节点状态检查
- 支持 Docker 容器化 Nginx（后续扩展）

**作者**：郑佳艺  
**GitHub**：https://github.com/britta1219x/ansible-web-cluster
