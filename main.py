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


if __name__ == '__main__':
    CrawlerApp().run()