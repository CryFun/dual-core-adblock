# Dual Core AdBlock · Mihomo + Xray 广告规则

[![Build](https://github.com/CryFun/dual-core-adblock/actions/workflows/build.yml/badge.svg)](https://github.com/CryFun/dual-core-adblock/actions/workflows/build.yml)

面向 **FIClash（Mihomo）** 和 **v2rayNG（Xray）** 的自动广告域名规则构建仓库。统一收集 Clash YAML、AdGuard 文本和 Hosts 规则，进行保守转换、去重与检查，然后生成两种客户端各自可读取的规则文件。

> 本项目实现的是**域名/路由级拦截**，不是完整 AdGuard 浏览器过滤引擎；不支持网页元素隐藏、脚本注入和 URL 路径级广告过滤。

## 立即使用

| 客户端 | 文件/脚本 | 使用方法 |
| --- | --- | --- |
| FIClash | [**订阅扩展脚本 `ficlash.js`**](https://raw.githubusercontent.com/CryFun/dual-core-adblock/main/ficlash.js) | 将脚本内容用于订阅扩展的 **Script** 模式；脚本加载 `domain.mrs` 并将广告规则置于前面 |
| v2rayNG | [**`adblock.dat`**](https://raw.githubusercontent.com/CryFun/dual-core-adblock/rules/adblock.dat) | 在 **Geo 资源管理**中添加自定义下载 URL 与文件名 `adblock.dat`，下载成功后添加域名路由 `ext:adblock.dat:adblock`，出站 `block` |

**FIClash 已正常工作的用户不必重装扩展脚本；如果旧订阅脚本仍指向原仓库地址，建议更新为本仓库的新地址。** 只要当前脚本 URL 没变化，后续规则会按客户端设置更新。

**v2rayNG 2.3.14 已验证的加载方式：** 单纯复制 DAT 到 `/sdcard/Android/data/.../files/assets/` 不一定生效；该版本的 Xray 可能从应用私有的 `app_assets` 读取。请优先通过客户端的 **Geo 资源 URL 下载功能**管理自定义 `adblock.dat`，然后使用带 `ext:` 的规则。去掉 `ext:` 不能真正加载规则库。详细步骤：[客户端使用指南](docs/CLIENTS.md)。

## 下载与输出

构建结果由 GitHub Actions 发布到 [`rules` 分支](https://github.com/CryFun/dual-core-adblock/tree/rules)，**不要手工修改这个分支**。

| 文件 | 用途 |
| --- | --- |
| [`domain.mrs`](https://raw.githubusercontent.com/CryFun/dual-core-adblock/rules/domain.mrs) | FIClash / Mihomo 域名规则集（主要输出） |
| [`adblock.dat`](https://raw.githubusercontent.com/CryFun/dual-core-adblock/rules/adblock.dat) | v2rayNG / Xray 的独立 GeoSite 广告分类 `ADBLOCK`（主要输出） |
| [`domain.yaml`](https://raw.githubusercontent.com/CryFun/dual-core-adblock/rules/domain.yaml) | 便于检查的 Mihomo 域名源规则 |
| [`stats.json`](https://raw.githubusercontent.com/CryFun/dual-core-adblock/rules/stats.json) | 各规则源计数、重复及未转换规则的统计 |
| [`geosite-info.json`](https://raw.githubusercontent.com/CryFun/dual-core-adblock/rules/geosite-info.json) | Xray DAT 条目数量、大小与 SHA-256 |
| `geosite.dat` | 仅包含 `ADBLOCK` 分类的兼容副本；**切勿覆盖 v2rayNG 自带的完整 `geosite.dat`** |

如果上游规则不包含 IP 或 Classical 条目，相应的可选输出文件不会生成；FIClash 扩展脚本也只引用域名 MRS。

## 规则源

当前收录：**REIJI007、anti-AD、AWAvenue（秋风）、HaGeZi Multi、AdGuard 中文过滤器、AdGuard 移动广告过滤器、乘风**。来源网址与格式见 [`config/sources.yaml`](config/sources.yaml)。添加新订阅、了解解析范围或误拦截处理，请阅读 [规则维护指南](docs/SOURCES.md)。

说明：AdGuard/ABP 规则只提取可安全映射为域名匹配的部分；`@@` 例外规则和网页过滤语法不会完整继承。规则数多不代表全部场景更强，发现误拦截应优先排查对应域名。

## 自动构建

- GitHub Actions：[`Build adblock rules`](https://github.com/CryFun/dual-core-adblock/actions/workflows/build.yml)；每天 **02:17 UTC** 定时运行，也可手动执行。修改 `src/`、`tests/`、`config/` 或工作流后亦会触发。
- 检查：单元测试、来源下载、Mihomo MRS 编译、上次规则数量对比、Xray DAT 生成；失败则停止发布，保留此前 `rules` 分支输出。
- 来源减少导致最终域名数比上次下降 **超过 30%** 时，校验会阻止发布。此阈值是异常保护，不是规则质量评分。
- GitHub 规则库发布成功**不代表 v2rayNG 本地 DAT 已更新**；是否自动更新取决于客户端的 Geo 资源更新设置。

## 仓库结构

```text
.github/workflows/build.yml   # 自动构建与发布
config/sources.yaml           # 上游订阅及格式
config/allowlist.txt          # 编译端排除项（非万能白名单）
docs/CLIENTS.md               # FIClash / v2rayNG 接入与排障
docs/SOURCES.md               # 新增规则源、解析范围、误拦截
docs/MAINTENANCE.md           # PC 端维护、测试、回滚
ficlash.js                    # FIClash 订阅扩展脚本（可直接复制）
src/                          # 解析、合并、验证、GeoSite 编译
tests/                        # 自动化测试
```

PC 端克隆、提交、手动构建及故障恢复，请阅读 [维护指南](docs/MAINTENANCE.md)。

## 使用须知

- **误拦截风险：** 广告过滤以域名为粒度，可能影响登录、图片或部分 App 功能；请先确认可疑域名再加到拦截源。
- **白名单限制：** `config/allowlist.txt` 只能避免某些条目被加入，不能保证绕过已经存在的上级域名后缀拦截。发现冲突时构建会失败；应在客户端为必要域名设置更高优先级的 DIRECT 规则。
- **上游版权及许可证：** 此仓库聚合第三方规则。使用、再分发前请分别核实各上游项目的许可和使用条款。
- **安全与可靠性：** 自动化依赖上游下载地址和 Mihomo 官方构建产物；外部资源变更、网络故障可能导致构建失败。`rules` 是自动发布分支，不要作为人工维护入口。

## 反馈与贡献

如果发现误拦截，请提供**应用名称、经过复测的可疑域名、阻断前后差异**；不要公开分享登录凭据、代理订阅或包含隐私的完整抓包。手工补充规则前请阅读 [规则维护指南](docs/SOURCES.md)。

项目地址：[CryFun/dual-core-adblock](https://github.com/CryFun/dual-core-adblock)。
