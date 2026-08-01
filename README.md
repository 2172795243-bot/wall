# 🕷️ Python 爬虫 APK 打包指南

## 📁 项目文件
- `main.py` - 主程序入口（Kivy UI界面）
- `crawler.py` - 爬虫核心逻辑模块
- `buildozer.spec` - 打包配置文件
- `README.md` - 本说明文件

---

## 🖥️ 第一步：在电脑上准备打包环境

### Windows 用户：

1. **安装 WSL（Linux子系统）**
   ```powershell
   # 在PowerShell管理员模式运行
   wsl --install
   ```
   安装完重启电脑，然后打开Ubuntu

2. **安装依赖**
   ```bash
   sudo apt update
   sudo apt install -y python3 python3-pip build-essential git \
       zip unzip openjdk-17-jdk autoconf libtool pkg-config \
       zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 \
       cmake libffi-dev libssl-dev
   pip3 install --user buildozer cython
   ```

3. **设置环境变量**
   ```bash
   export PATH=$PATH:$HOME/.local/bin
   ```

---

## 📦 第二步：打包成APK

1. **把项目文件传到Ubuntu**（假设在 `~/python_crawler_apk` 目录）

2. **进入项目目录**
   ```bash
   cd ~/python_crawler_apk
   ```

3. **执行打包命令**（第一次会下载SDK和NDK，需要较长时间）
   ```bash
   buildozer -v android debug
   ```

4. **等待编译完成**，APK 会在 `bin/` 目录下，例如：
   ```
   bin/pythoncrawler-1.0.0-arm64-v8a_armeabi-v7a-debug.apk
   ```

---

## 📱 第三步：安装到手机

1. 把APK文件传到手机
2. 手机打开"允许安装未知来源应用"
3. 点击APK文件安装
4. 安装完成后，桌面会出现"Python Crawler"图标
5. 打开就能用！

---

## ⚙️ 应用功能说明

打开APP后：
- **URL输入框**：输入要爬取的网址
- **类型下拉框**：
  - 网页标题 - 只爬标题
  - 网页正文 - 提取正文段落
  - 所有链接 - 提取所有超链接
  - 所有图片 - 提取所有图片URL
  - 完整信息 - 综合信息
- **开始爬取按钮**：执行爬取
- **保存结果按钮**：把结果保存为JSON文件
- **清空按钮**：重置界面

---

## 💡 使用技巧

1. **首次打包**会下载约2-3GB的SDK/NDK，可能需要1-2小时
2. **再次打包**很快，几分钟即可
3. 可以在手机上给APP授权**存储权限**，方便保存爬取结果
4. 部分网站有反爬机制，可能需要自定义User-Agent

---

## 🐛 常见问题

**Q: 打包报错 "Android SDK not found"**
A: buildozer首次运行会自动下载SDK，保持网络畅通

**Q: APK安装后闪退**
A: 检查 `android.permissions` 是否包含 `INTERNET` 权限

**Q: 爬取失败/超时**
A: 目标网站可能有反爬，尝试在User-Agent输入框填入浏览器的UA

---

## 🚀 进阶：想要免电脑直接打包？

可以使用 **GitHub Actions 云打包**（免费）：
1. 把项目传到GitHub
2. 配置workflow自动调用buildozer
3. 在网页下载打包好的APK

需要的话我可以帮你写GitHub Actions配置~