# -*- coding: utf-8 -*-
"""
爬虫核心逻辑模块
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from urllib.parse import urljoin, urlparse


class WebCrawler:
    """网页爬虫核心类"""
    
    DEFAULT_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 12; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }

    def __init__(self, url, custom_headers=None):
        self.url = url
        self.headers = self.DEFAULT_HEADERS.copy()
        if custom_headers:
            self.headers.update(custom_headers)
        self.soup = None
        self.html_text = None
        self.error = None

    def fetch(self, timeout=15):
        """获取网页内容"""
        try:
            # 禁用SSL警告
            requests.packages.urllib3.disable_warnings()
            response = requests.get(self.url, headers=self.headers, timeout=timeout, verify=False)
            response.encoding = response.apparent_encoding or 'utf-8'
            if response.status_code != 200:
                self.error = f"HTTP {response.status_code} 请求失败"
                return False
            self.html_text = response.text
            self.soup = BeautifulSoup(self.html_text, 'html.parser')
            return True
        except requests.exceptions.Timeout:
            self.error = "请求超时，请检查网络"
        except requests.exceptions.SSLError:
            self.error = "SSL证书错误"
        except requests.exceptions.ConnectionError:
            self.error = "网络连接失败"
        except Exception as e:
            self.error = f"请求出错: {str(e)[:80]}"
        return False

    def get_title(self):
        """获取网页标题"""
        if not self.soup:
            return None
        title = self.soup.find('title')
        return title.get_text(strip=True) if title else None

    def get_text(self):
        """获取正文文本"""
        if not self.soup:
            return []
        # 移除script和style
        for tag in self.soup(['script', 'style', 'noscript']):
            tag.decompose()
        paragraphs = self.soup.find_all('p')
        texts = [p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)]
        # 如果没有p标签，尝试div
        if not texts:
            divs = self.soup.find_all('div')
            for d in divs[:50]:
                t = d.get_text(strip=True)
                if len(t) > 30:
                    texts.append(t)
        return texts

    def get_links(self, max_count=200):
        """获取所有链接"""
        if not self.soup:
            return []
        links = []
        for a in self.soup.find_all('a', href=True):
            href = a['href'].strip()
            if not href or href.startswith('javascript:') or href.startswith('#'):
                continue
            # 转成绝对路径
            full_url = urljoin(self.url, href)
            text = a.get_text(strip=True)[:50] or '(无文本)'
            links.append({'text': text, 'url': full_url})
            if len(links) >= max_count:
                break
        return links

    def get_images(self, max_count=100):
        """获取所有图片"""
        if not self.soup:
            return []
        images = []
        for img in self.soup.find_all('img'):
            src = img.get('src') or img.get('data-src') or img.get('data-original')
            if not src:
                continue
            src = src.strip()
            if src.startswith('data:'):
                continue
            full_url = urljoin(self.url, src)
            alt = img.get('alt', '')[:50]
            images.append({'alt': alt, 'url': full_url})
            if len(images) >= max_count:
                break
        return images

    def get_meta(self):
        """获取meta信息"""
        if not self.soup:
            return {}
        meta = {}
        for tag in self.soup.find_all('meta'):
            name = tag.get('name') or tag.get('property') or tag.get('http-equiv')
            content = tag.get('content')
            if name and content:
                meta[name.lower()] = content[:300]
        return meta

    def get_full_info(self):
        """获取完整信息"""
        return {
            'url': self.url,
            'title': self.get_title(),
            'meta': self.get_meta(),
            'paragraphs': self.get_text()[:50],
            'links_count': len(self.get_links(max_count=9999)),
            'images_count': len(self.get_images(max_count=9999)),
        }


def format_result(crawler, crawl_type):
    """格式化爬取结果为显示文本"""
    lines = []
    lines.append(f"[b]🎯 目标:[/b] {crawler.url}\n")
    
    if crawler.error:
        lines.append(f"[b]❌ 错误:[/b] {crawler.error}")
        return "\n".join(lines)

    if crawl_type == "网页标题":
        title = crawler.get_title() or "（未找到）"
        lines.append(f"[b]📌 网页标题:[/b]\n\n{title}")

    elif crawl_type == "网页正文":
        texts = crawler.get_text()
        if texts:
            lines.append(f"[b]📝 正文 ({len(texts)}段):[/b]\n")
            for i, t in enumerate(texts[:50], 1):
                lines.append(f"{i}. {t}")
        else:
            lines.append("（未找到正文）")

    elif crawl_type == "所有链接":
        links = crawler.get_links(max_count=300)
        if links:
            lines.append(f"[b]🔗 链接 ({len(links)}个):[/b]\n")
            for i, link in enumerate(links, 1):
                lines.append(f"{i}. {link['text']}\n   → {link['url']}")
        else:
            lines.append("（未找到链接）")

    elif crawl_type == "所有图片":
        images = crawler.get_images(max_count=200)
        if images:
            lines.append(f"[b]🖼️ 图片 ({len(images)}张):[/b]\n")
            for i, img in enumerate(images, 1):
                lines.append(f"{i}. {img['alt'] or '(无描述)'}\n   → {img['url']}")
        else:
            lines.append("（未找到图片）")

    elif crawl_type == "完整信息":
        info = crawler.get_full_info()
        lines.append(f"[b]📌 标题:[/b] {info['title'] or '（无）'}")
        lines.append(f"\n[b]🔗 链接数:[/b] {info['links_count']}")
        lines.append(f"[b]🖼️ 图片数:[/b] {info['images_count']}")
        if info['meta']:
            lines.append(f"\n[b]📋 Meta信息:[/b]")
            for k, v in list(info['meta'].items())[:10]:
                lines.append(f"  • {k}: {v}")
        if info['paragraphs']:
            lines.append(f"\n[b]📝 正文预览 (前5段):[/b]")
            for i, t in enumerate(info['paragraphs'][:5], 1):
                lines.append(f"  {i}. {t[:100]}")

    return "\n".join(lines)


def save_to_file(result_data, save_dir="/sdcard/Download/python_crawler_apk/results"):
    """保存结果到文件"""
    if not result_data:
        return None, "没有可保存的数据"
    try:
        os.makedirs(save_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"crawl_result_{timestamp}.json"
        filepath = os.path.join(save_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)
        return filepath, f"已保存到 {filepath}"
    except Exception as e:
        return None, f"保存失败: {e}"


from datetime import datetime
import os