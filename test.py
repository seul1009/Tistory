import feedparser
from datetime import datetime
import urllib.request

POST_COUNT = 5
BLOG_RSS_URL = "https://seulow-down.tistory.com/rss"

# 캐시 우회를 위해 현재 시간으로 쿼리 스트링 추가
rss_url_with_timestamp = BLOG_RSS_URL + "?" + datetime.now().strftime("%Y%m%d%H%M%S")
req = urllib.request.Request(rss_url_with_timestamp, headers={"Cache-Control": "no-cache"})
feed = feedparser.parse(urllib.request.urlopen(req))

entries = feed['entries']
entries.sort(key=lambda x: datetime.strptime(x.published, '%a, %d %b %Y %H:%M:%S %z'), reverse=True)

posts = []
for entry in entries[:POST_COUNT]:
    published_date = datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %z').strftime('%Y-%m-%d')
    posts.append(f"- {published_date} [{entry.title}]({entry.link})")

readme_path = './README.md'

with open(readme_path, 'r', encoding='utf-8') as readme_md_file:
    original_readme = readme_md_file.read()

start_comment = '<!-- RECENT POST START -->'
end_comment = '<!-- RECENT POST END -->'
start_index = original_readme.find(start_comment)
end_index = original_readme.find(end_comment)

joined_str = '\n'.join(posts)
updated_readme = (
    original_readme[:start_index] +
    start_comment + '\n' +
    joined_str + '\n' +
    original_readme[end_index:]
)

if updated_readme != original_readme:
    with open(readme_path, 'w', encoding='utf-8') as readme_md_file:
        readme_md_file.write(updated_readme)
    with open(readme_path, 'a', encoding='utf-8') as readme_md_file:
        readme_md_file.truncate()
else:
    print("no change. no update")
