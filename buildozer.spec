[app]
# 应用的名称(显示在手机桌面)
title = Python Crawler

# 包名(类似java包名,唯一标识)
package.name = pythoncrawler

# 域名(包名的一部分)
package.domain = org.crawler

# 主入口文件
source.filename = main.py

# 源文件目录
source.dir = .

# 源码包含的目录
source.include_exts = py,png,jpg,kv,atlas

# 应用版本号
version = 1.0.0

# 至少需要的安卓版本
os.android.api = 21

# SDK版本
os.android.sdk = 21

# 最低安卓版本
android.minapi = 21

# 支持的架构(armeabi-v7a是大部分手机,arm64-v8a是64位)
android.archs = arm64-v8a, armeabi-v7a

# 权限(需要联网)
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# 全屏显示
fullscreen = 0

# 屏幕方向(portrait竖屏,landscape横屏,sensor自动)
orientation = portrait


[buildozer]
# 日志等级
log_level = 2


[requirements]
# 需要的Python第三方库
# kivy是UI框架, requests是HTTP库, beautifulsoup4是HTML解析库
# urllib3, chardet, idna, certifi 是requests的依赖
requirements = python3,kivy==2.3.0,requests,beautifulsoup4,urllib3,chardet,idna,certifi,lxml


[source]
# 引入项目内的所有模块
source.include_patterns = *.py,*.kv


[app:icon]
# 应用的图标(可选,需要自己放icon.png到项目目录)
# icon.filename = %(source.dir)s/icon.png

[app:presplash]
# 启动画面(可选)
# presplash.filename = %(source.dir)s/presplash.png
