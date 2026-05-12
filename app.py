import feedparser
import urllib.parse
from datetime import datetime, timedelta

# 精準關鍵字策略
keywords = '("商用不動產" OR "辦公室" OR "商辦" OR "廠辦" OR "資料中心" OR "飯店" OR "旅館" OR "商場" OR "標售" OR "土地買賣" OR "取得不動產" OR "處分不動產")'
query = urllib.parse.quote(f'{keywords} when:1d')
rss_url = f'https://news.google.com/rss/search?q={query}&hl=zh-TW&gl=TW&ceid=TW:zh-Hant'

def fetch_news():
    feed = feedparser.parse(rss_url)
    if not feed.entries:
        return "<p class='text-center'>過去 24 小時內暫無相關商用不動產新聞。</p>"
    
    items = []
    for entry in feed.entries:
        items.append(f"""
        <div class='card mb-3 shadow-sm'>
            <div class='card-body'>
                <h5 class='card-title'><a href='{entry.link}' target='_blank' style='text-decoration:none; color:#0d6efd;'>{entry.title}</a></h5>
                <p class='card-text'><small class='text-muted'>來源：{entry.source.get('title', '媒體')} | 發布時間：{entry.published}</small></p>
            </div>
        </div>
        """)
    return "".join(items)

update_time = (datetime.now() + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')

html_content = f"""
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>台灣商用不動產快訊</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>body {{ background: #f8f9fa; padding: 30px 10px; }} .container {{ max-width: 900px; }}</style>
</head>
<body>
    <div class="container">
        <h2 class="text-center mb-2">🏢 台灣商用不動產新聞 (24H)</h2>
        <p class="text-center text-secondary mb-4">更新時間：{update_time} (台北時區)</p>
        <hr>
        {fetch_news()}
    </div>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)
