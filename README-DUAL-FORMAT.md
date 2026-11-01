# Mihomo + Xray 双格式输出

本升级包不改动 `src/build.py`、现有规则源、白名单或 FIClash 脚本。现有 `domain.yaml` 经 Mihomo 编译为 `domain.mrs`，同时经 `src/build_geosite.py` 转成 Xray GeoSite protobuf。

生成文件（`rules` 分支）：
- `domain.mrs`：FIClash / Mihomo，原有地址不变。
- `adblock.dat`：**推荐**用于 v2rayNG 的独立 GeoSite 文件，包含 `ADBLOCK` 分类。
- `geosite.dat`：同内容的兼容命名文件，**仅包含 ADBLOCK 分类**，绝对不要直接覆盖客户端原有的 `geosite.dat`，否则 `geosite:cn` 等其他分类将丢失。
- `geosite-info.json`：规则数、SHA256、大小。

v2rayNG/Xray 路由规则示例（在 Xray JSON 的 `routing.rules` 中，放在普通分流规则前；确保出站存在 `block`）：

```json
{"type":"field","domain":["ext:adblock.dat:adblock"],"outboundTag":"block"}
```

下载：`https://raw.githubusercontent.com/CryFun/mihomo-adblock/rules/adblock.dat`。通过 v2rayNG 当前版本提供的资源文件导入或自定义资源机制放入 Xray **实际使用的资源目录**；不同安装渠道/Android 版本路径不同。不要只把文件放在 Downloads 后就期待自动生效。Xray 对 `ext:` 支持的路径与资源加载行为以客户端实际配置为准。

重要限制：此转换只包含域名规则，不包含 IP、网页元素隐藏、URL 路径或 AdGuard 脚本规则。Xray 对目标域名的识别受 DNS/嗅探/路由设置影响。生成文件自动随原工作流发布，**v2rayNG 不一定会自动更新本地 dat 文件**。
