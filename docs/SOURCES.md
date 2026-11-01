# 规则源维护与新增

规则来源在 [`config/sources.yaml`](../config/sources.yaml)，自动合并脚本为 [`src/build.py`](../src/build.py)。构建会按顺序去重并统计各来源贡献；统计结果在 `rules/stats.json`。

## 已配置的来源

| name | 来源 | behavior |
| --- | --- | --- |
| `reiji` | REIJI007 AdBlock Rule For Clash | `classical` |
| `antiad` | anti-AD | `domain` |
| `awavenue` | AWAvenue / 秋风 | `domain` |
| `hagezi_normal` | HaGeZi Multi | `adguard` |
| `adguard_chinese` | AdGuard 中文过滤器 | `adguard` |
| `adguard_mobile` | AdGuard 移动广告过滤器 | `adguard` |
| `chengfeng` | 乘风规则 | `adguard` |

精确下载地址见 `config/sources.yaml`；部分来源会改变路径、许可证或内容，遇到下载失败时应首先检查上游。

## 如何增加来源

编辑 `config/sources.yaml`，在 `sources:` 下追加一个项目。例如：

```yaml
  - name: extra_adguard_dns
    url: https://example.com/filters.txt
    behavior: adguard
```

`name` 不得重复；`url` 必须是可公开获取的可信文本地址。当前支持四种 `behavior`：

| behavior | 输入格式 | 输出 |
| --- | --- | --- |
| `domain` | Clash `payload:` 域名 YAML | 精确域名 / 域名后缀 |
| `classical` | Clash `payload:` Classical YAML | 域名、IP 以及不能解析的其他 Classical 规则 |
| `adguard` | AdGuard / ABP 文本的安全子集 | 可转换的域名规则 |
| `hosts` | Hosts 文本 | 可转换的精确域名规则 |

**不能直接把任意 TXT 放入 `config/` 就期望自动加载**：目前 `build.py` 只会从 `sources.yaml` 列出的 URL 下载内容。若想支持本地手写规则，需要再添加明确的本地文件输入功能。

## 语法转换边界

- `||ads.example.com^` → 域名后缀 `+.ads.example.com`。
- 纯域名 `ads.example.com` → 精确域名。
- `0.0.0.0 ads.example.com` → 精确域名。
- `@@` 例外、元素隐藏 `##`、脚本规则、URL 路径、修饰符等 **不进行等价转换**，仅统计为例外/不支持。

**特别注意**：某些 AdGuard 规则表包含例外，转换后由于丢失例外语义，可能造成误拦截。新增来源应先小范围测试，检查 `stats.json` 中的 `exceptions` 和 `unsupported`。

## 误拦截和手工补规则

发现某个 App 开屏广告时，先查看按应用筛选的 DNS/连接日志，使用精确域名进行单项阻断测试；确认应用仍能正常使用后，再将该域名加入受信任的自维护规则源。不要仅凭 `ad` 或 `splash` 关键词就屏蔽整个后缀。

`config/allowlist.txt` 支持精确域名和 `+.example.com` 后缀的构建期排除，但它**不是客户端 DIRECT 白名单**，无法覆盖已生效的更宽泛后缀。构建检测到这类冲突会拒绝发布；客户端确有必要放行时，应在广告阻断规则前加明确的 DIRECT 规则。

新增来源提交后到 [Actions](https://github.com/CryFun/dual-core-adblock/actions/workflows/build.yml) 检查绿勾，并核对 [`stats.json`](https://raw.githubusercontent.com/CryFun/dual-core-adblock/rules/stats.json) 是否有异常变化。
