# -*- coding: utf-8 -*-
"""
Python 爬虫 APK - 主程序
基于 Kivy 框架，打包后可在安卓手机上直接运行
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle
import threading
import os
import json
from datetime import datetime
import requests
from bs4 import BeautifulSoup


class CrawlerApp(App):
    """爬虫APK主应用"""
    title = "Python 爬虫工具"
    result_data = None

    def build(self):
        root = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))
        
        # 标题
        title_label = Label(text="[b]🕷️ Python 爬虫工具[/b]", markup=True,
                           size_hint_y=None, height=dp(50), font_size='22sp')
        root.add_widget(title_label)
        
        # URL输入
        url_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(45), spacing=dp(5))
        url_box.add_widget(Label(text="URL:", size_hint_x=None, width=dp(50)))
        self.url_input = TextInput(hint_text="输入网址，如 https://example.com", multiline=False)
        url_box.add_widget(self.url_input)
        root.add_widget(url_box)
        
        # 用户代理输入
        ua_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(45), spacing=dp(5))
        ua_box.add_widget(Label(text="UA:", size_hint_x=None, width=dp(50)))
        self.ua_input = TextInput(hint_text="自定义User-Agent（可选）", multiline=False)
        ua_box.add_widget(self.ua_input)
        root.add_widget(ua_box)
        
        # 爬取类型
        type_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(45), spacing=dp(5))
        self.type_spinner = Spinner(text="网页标题", 
                                   values=("网页标题", "网页正文", "所有链接", "所有图片", "完整信息"),
                                   size_hint_x=None, width=dp(160))
        type_box.add_widget(Label(text="类型:", size_hint_x=None, width=dp(50)))
        type_box.add_widget(self.type_spinner)
        root.add_widget(type_box)
        
        # 按钮区
        btn_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50), spacing=dp(10))
        self.crawl_btn = Button(text="🚀 开始爬取", background_color=(0.2, 0.7, 0.3, 1))
        self.save_btn = Button(text="💾 保存结果", background_color=(0.2, 0.5, 0.8, 1), disabled=True)
        self.clear_btn = Button(text="🧹 清空", background_color=(0.8, 0.3, 0.3, 1))
        self.crawl_btn.bind(on_press=self.start_crawl)
        self.save_btn.bind(on_press=self.save_result)
        self.clear_btn.bind(on_press=self.clear_all)
        btn_box.add_widget(self.crawl_btn)
        btn_box.add_widget(self.save_btn)
        btn_box.add_widget(self.clear_btn)
        root.add_widget(btn_box)
        
        # 状态
        self.status_label = Label(text="✅ 就绪 - 请输入URL后点击开始爬取", 
                                size_hint_y=None, height=dp(30), color=(0.5, 0.5, 0.5, 1))
        root.add_widget(self.status_label)
        
        # 结果区
        scroll = ScrollView(size_hint_y=None)
        scroll.bind(size=lambda s, v: setattr(s, 'height', v[1]))
        self.result_label = Label(text="📊 爬取结果将在这里显示...", size_hint_y=None,
                                 font_size='14sp', markup=True, valign='top', padding=(dp(10), dp(10)))
        self.result_label.bind(texture_size=lambda l, v: setattr(l, 'height', v[1] + dp(20)))
        scroll.add_widget(self.result_label)
        root.add_widget(scroll)
        
        return root

    def start_crawl(self, instance):
        url = self.url_input.text.strip()
        if not url:
            self.status_label.text = "❌ 请输入有效的URL"
            return

        crawl_type = self.type_spinner.text
        ua = self.ua_input.text.strip()
        custom_headers = {'User-Agent': ua} if ua else None

        self.status_label.text = "⏳ 正在爬取中，请稍候..."
        self.crawl_btn.disabled = True

        def worker():
            crawler = WebCrawler(url, custom_headers=custom_headers)
            crawler.fetch(timeout=20)
            result_text = format_result(crawler, crawl_type)
            result_data = crawler.get_full_info() if crawl_type == "完整信息" else {
                'url': url,
                'type': crawl_type,
                'title': crawler.get_title(),
                'text': crawler.get_text() if crawl_type == "网页正文" else None,
                'links': crawler.get_links() if crawl_type == "所有链接" else None,
                'images': crawler.get_images() if crawl_type == "所有图片" else None,
                'error': crawler.error,
            }

            def update_ui(dt):
                self.result_label.text = result_text
                self.result_data = result_data
                self.save_btn.disabled = False
                self.crawl_btn.disabled = False
                self.status_label.text = "✅ 爬取完成" if not crawler.error else f"❌ {crawler.error}"
            Clock.schedule_once(update_ui, 0)

        threading.Thread(target=worker, daemon=True).start()

    def save_result(self, instance):
        if not self.result_data:
            self.status_label.text = "❌ 没有可保存的数据"
            return
        filepath, msg = save_to_file(self.result_data)
        self.status_label.text = msg
        popup = Popup(title='保存结果', content=Label(text=msg), size_hint=(None, None), size=(dp(360), dp(120)))
        popup.open()

    def clear_all(self, instance):
        self.url_input.text = ''
        self.ua_input.text = ''
        self.type_spinner.text = '网页标题'
        self.result_label.text = '📊 爬取结果将在这里显示...'
        self.status_label.text = '✅ 就绪 - 请输入URL后点击开始爬取'
        self.save_btn.disabled = True
        self.result_data = None


if __name__ == '__main__':
    CrawlerApp().run()