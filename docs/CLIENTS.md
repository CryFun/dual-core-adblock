# 客户端接入指南

本仓库同时输出 FIClash / Mihomo 的 `domain.mrs` 和 v2rayNG / Xray 的 `adblock.dat`。两者共用同一批域名数据，但各自客户端的 DNS、嗅探和路由实现不同，实际拦截效果不一定完全一致。

## FIClash：订阅扩展脚本

1. 打开仓库根目录的 [`ficlash.js`](../ficlash.js)，复制完整内容。
2. 在 FIClash 的**订阅扩展 → Script 模式**使用该脚本（具体菜单以安装版本为准）。
3. 更新订阅。脚本自动注册名为 `custom-ad-domain` 的 MRS Rule Provider，并在 `rules` 开头加入 `RULE-SET,custom-ad-domain,REJECT`。
4. 检查 FIClash 日志或连接记录，确认规则加载与广告拦截正常。

脚本默认使用：

```text
https://raw.githubusercontent.com/CryFun/dual-core-adblock/rules/domain.mrs
```

如果原先 FIClash 已经正常运行，则不必重复导入脚本。遇到网站功能异常，先禁用广告规则进行对照；必要时在 `RULE-SET` 之前加入更高优先级的特定域名 `DIRECT` 规则。

## v2rayNG 2.3.14：自定义 GeoSite

> 本文的 Geo 资源 URL 方案已经在用户的 v2rayNG 2.3.14 上验证可以正常加载并拦截。不同版本菜单名称可能存在差异。

1. 在 v2rayNG 的 **Geo 资源管理 / Geo 文件设置**中，添加一个**自定义 Geo 资源 URL**：

   ```text
   https://raw.githubusercontent.com/CryFun/dual-core-adblock/rules/adblock.dat
   ```

   资源文件名使用 `adblock.dat`，并从客户端执行下载/更新。
2. 新建一条**自定义路由**：

   | 字段 | 值 |
   | --- | --- |
   | domain | `ext:adblock.dat:adblock` |
   | outboundTag | `block` |
   | ip、process、port、protocol | 留空 |
   | network | `tcp,udp`（或默认值） |

3. 把这条规则置于一般代理与直连规则之前，保存后重启代理。
4. 通过连接日志或已确认的广告域名测试是否命中 `block`。

**不要把 `ext:` 去掉。** `adblock.dat:adblock` 不会引用外部 GeoSite 分类；它可能被当作普通域名匹配文本而不报错。也不要将本项目只有广告分类的 `geosite.dat` 覆盖原生 `geosite.dat`，否则可能损坏 `geosite:cn` 等现有路由。

### 找不到 DAT 文件时

可能看到：

```text
illegal domain rule: ext:adblock.dat:adblock
failed to open adblock.dat
stat /data/user/0/com.v2ray.ang/app_assets/adblock.dat: no such file or directory
```

这表示 Xray 无法从**实际运行时的应用资源目录**找到 DAT，不等于文件格式错误。只将文件复制到 `/sdcard/Android/data/com.v2ray.ang/files/assets/` 不能保证成功，因为客户端可能从内部 `app_assets` 目录读取。优先使用 v2rayNG 自带的 Geo 资源 URL 下载方式；修复前暂时禁用此路由避免代理无法启动。

临时替代方案：如果本机标准 `geosite.dat` 包含 `category-ads-all`，可先使用 `geosite:category-ads-all` → `block`。它与本项目自建的广告分类**不是同一套数据**。

### 本地更新

GitHub Actions 更新 `rules/adblock.dat` 后，v2rayNG 端是否刷新取决于客户端的 Geo 资源更新机制。必要时在 Geo 资源管理中手动更新该 URL，并确认路由仍命中 `block`。
