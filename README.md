# opendoor

一个支持规则管理和订阅转换的工具，旨在提供更灵活的网络配置生成方案。

## 功能特性

- **多平台支持**: 支持为 Surge、Clash 和 Quantumult X 生成配置文件。
- **规则分类管理**: 可自由选择开启或关闭特定的规则类别（如 Apple, Telegram, Netflix 等）。
- **内网/公司环境支持**: 针对公司内网域名（如 `*.company.com`）提供专门配置，自动处理 DNS 解析策略、Fake-IP 过滤及代理绕过，确保内网服务访问无误。
- **链式代理 (Chain Proxy)**: 支持通过家庭 IP 或特定节点进行二次转发。
- **Gist 集成**: 支持一键将生成的配置上传至 GitHub Gist，方便移动端订阅使用。

## 使用方法

1. 访问: [https://onlinefchen.github.io/opendoor/](https://onlinefchen.github.io/opendoor/)
2. 输入你的订阅链接。
3. (可选) 在 **Company/Intranet Settings** 中输入需要直连的公司域名或内网地址。
4. 选择输出格式并生成配置。

## 内网配置说明

在 Web 界面中添加公司域名后，系统会自动应用以下逻辑：
- **Clash**: 将域名添加至 `skip-proxy`、`fake-ip-filter` 和 `nameserver-policy` (指向 system)，并设置为 `DIRECT`。
- **Surge**: 将域名添加至 `skip-proxy`、`always-real-ip` 和 `[Host]` 映射 (指向 system DNS)，并设置优先直连规则。
