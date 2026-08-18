# 部署上线指南 · 小赖还不赖官网（纯静态 · Git 自动部署）

本站点 3 个文件，零依赖零构建，推到 Git 仓库后平台自动部署，以后每次改完 `git push` 就上线。

- `index.html` 页面结构（已按真实信息更新：三年实战 / 18 家制造业 / 常驻东莞 / 微信手机 15112850612）
- `styles.css` 样式（移动优先响应式）
- `script.js` 移动端菜单 + 数字滚动

---

## 一、本地预览（改完先自己看）

```bash
cd site
python3 -m http.server 8123
# 浏览器开 http://localhost:8123 ，F12 切手机视图看响应式
```

---

## 二、自动部署原理（一句话）

你把 `site/` 推到 GitHub → 平台监听仓库 → 每次 push 自动拉取并发布。你以后只管改文件、push，不用登后台手动传。

---

## 三、具体一步步操作（以 Cloudflare Pages 为例，国内访问稳）

**第 1 步：建 GitHub 仓库**
1. 打开 github.com，登录（没有就注册，用邮箱即可）。
2. 右上角 「＋」→ New repository。
3. Repository name 填 `xiaolai-site`（随便起，英文）。
4. 其它**全留默认**，**不要**勾 "Add a README"，**不要**选 .gitignore / License。
5. 点 Create repository。
6. 建好后页面会显示仓库地址，形如 `https://github.com/你的用户名/xiaolai-site.git`，**先复制这行地址**。

> 我已经帮你在本地 `site/` 目录初始化好 Git 并提交了一版，你只需补远程地址和推送：

**第 2 步：本地推送到 GitHub**（把下面地址换成你第 1 步复制的）
```bash
cd site
git remote add origin https://github.com/你的用户名/xiaolai-site.git
git branch -M main
git push -u origin main
# 会弹窗要你登录 GitHub，按提示授权即可
```
推送成功 → 刷新 GitHub 页面能看到 3 个文件。

**第 3 步：Cloudflare Pages 连 GitHub 自动部署**
1. 打开 dash.cloudflare.com → 左侧 **Workers & Pages** → **Create** → **Pages** → **Connect to Git**。
2. 首次会要授权 GitHub，点 **Authorize** 允许。
3. 选刚才的仓库 `xiaolai-site` → **Begin setup**。
4. 项目名随意（如 `xiaolai-note`）。
5. 关键配置（其余默认）：
   - Production branch：`main`
   - **Build command：留空**
   - **Build output directory：`/`（因为 index.html 在仓库根）**
6. 点 **Save and Deploy**，约 30 秒后出 `https://xiaolai-note.pages.dev` 这种地址，立刻能访问。
7. 以后改文件 → `git push` → 平台自动重新部署，不用再来这里。

**第 4 步：绑自己的域名 + 开 HTTPS（可选，国内顶级域名需先 ICP 备案）**
1. Pages 项目 → **Custom domains** → 输入你的域名（如 `note.xxx.com`）→ **Continue**。
2. 按提示去你的域名商 DNS 加一条 **CNAME**，指向 `xiaolai-note.pages.dev`。
3. Cloudflare 自动签发免费证书；在 SSL/TLS 里把模式设为 **Full**，并开启 **Always Use HTTPS**。
4. 国内顶级域名（.cn/.com 等）必须先完成工信部备案，否则解析不了——子域名 `*.pages.dev` 不用备案，可直接用。

---

## 四、备选：用 Netlify（拖拽也能，但自动部署同样走 Git）

1. app.netlify.com → **Add new site** → **Import an existing project** → 连 GitHub。
2. 选 `xiaolai-site` 仓库。
3. Branch：`main`；**Build command 留空**；**Publish directory：`.`**（根目录）。
4. Deploy site → 出 `xxx.netlify.app`。
5. Domain settings 里绑自定义域名，HTTPS 自动开。

> Cloudflare 和 Netlify 二选一即可，体验几乎一样。面向国内客户、要快 → Cloudflare Pages 更稳。

---

## 五、上线后验证清单

- [ ] 手机 / 平板 / 桌面三种宽度布局正常
- [ ] 导航锚点跳转正确
- [ ] 微信/手机号 `15112850612` 可点击拨号
- [ ] HTTPS 小锁亮起，http 自动跳 https
- [ ] 改一处文字 → `git push` → 平台自动出新版（验证自动部署生效）

---

## 六、改内容与回滚

- **改文案**：编辑 `index.html` 对应段落 → `git add . && git commit -m "改文案" && git push`，自动上线。
- **换色/字体**：改 `styles.css` 顶部 `:root` 变量（`--brand` 主色等）。
- **回滚**：Cloudflare/Netlify 每次部署都有历史版本，控制台一键 Rollback 到上一版，无需重新推。

---

## 七、待您补充的真实内容（不要编数据）

「关于我」数字已按您给的真实背景填（3年、18家）。建议后续用真实服务过的工厂案例补一个「客户案例」区块，B 端信任靠证据，这块最能促单。需要我加，您给素材我填。
