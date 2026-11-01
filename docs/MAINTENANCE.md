# PC 端维护与 GitHub Actions

仓库只把**源码和配置放在 `main`**；构建产物自动发布到 **`rules`**。切勿向 `rules` 人工提交文件。

## 第一次在 PC 上克隆

先安装 Git 和 Python 3.12+，然后打开 PowerShell（Windows）或终端（macOS/Linux）：

```bash
git clone https://github.com/CryFun/dual-core-adblock.git
cd dual-core-adblock
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

Windows 上如无 `python` 命令，可使用 `py -3` 替代。**本地完整运行 `src/build.py` 会下载多个大规则源**；通常只需先跑单元测试，在线构建交给 GitHub Actions。

## 常用维护操作

修改 `README.md`、`docs/` 或 `ficlash.js` 后：

```bash
git add README.md docs ficlash.js
git commit -m "Update docs and FIClash script"
git push origin main
```

修改 `config/sources.yaml` 或程序后：

```bash
python -m unittest discover -s tests -v
git add config src tests
git commit -m "Update rule sources"
git push origin main
```

每日构建时间为 **02:17 UTC**（日本时间 11:17）。需要立即重建：打开 [Actions → Build adblock rules](https://github.com/CryFun/dual-core-adblock/actions/workflows/build.yml)，选择 **Run workflow**，分支选 `main`。默认路径过滤不会因单独修改 README 或 `ficlash.js` 而触发构建；这是正常设计。

## 核对发布情况

1. Actions 最新运行变绿。
2. [`rules/stats.json`](https://raw.githubusercontent.com/CryFun/dual-core-adblock/rules/stats.json) 能正常查看。
3. [`rules/domain.mrs`](https://raw.githubusercontent.com/CryFun/dual-core-adblock/rules/domain.mrs) 与 [`rules/adblock.dat`](https://raw.githubusercontent.com/CryFun/dual-core-adblock/rules/adblock.dat) 能下载。
4. 在客户端更新规则后确认广告域名命中，避免“只加载了路由文本”却没真正拦截。

构建遇到规则数突然下降超过 30%、源失效、白名单冲突、MRS 编译失败等情况，会停止发布，因此 `rules` 保留上次成功产物。检查 Actions 的**失败步骤及日志**，优先修复问题后手动重建，不要直接禁用校验。

## 回滚与安全

- 仅文档出错：在 GitHub 选择旧提交，或本地使用 `git revert <commit>` 创建回滚提交。
- 源码出错：优先 `git revert` 出错提交，再手动执行构建；不要直接编辑自动生成的 `rules` 分支。
- 不要在仓库或截图中上传 GitHub PAT、代理订阅、私钥或个人日志。
- 第三方广告规则源可能有限制再分发条款；向外公开聚合产物前核实各来源许可证。
- GitHub Actions 下载 Mihomo 官方最新兼容二进制，尚未固定校验摘要；如果有严格的供应链安全要求，应另外加入固定版本与 SHA-256 验证。
