import feedparser
from datetime import datetime

POST_COUNT = 5
BLOG_RSS_URL = "https://seulow-down.tistory.com/rss"
feed = feedparser.parse(BLOG_RSS_URL)

entries = feed['entries']
entries.sort(key=lambda x: datetime.strptime(x.published, '%a, %d %b %Y %H:%M:%S %z'), 
             reverse=True)

posts = []
for entry in entries[:POST_COUNT]:
    # 날짜 형식 변경 (yyyy-mm-dd)
    published_date = datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %z').strftime('%Y-%m-%d')
    posts.append(f"- {published_date} [{entry.title}]({entry.link})")

readme_path = './README.md'

# open README.md
with open(readme_path, 'r', encoding='utf-8') as readme_md_file:
    original_readme = readme_md_file.read()

# README.md 파일에서 <!-- RECENT POST START -->와
# <!-- RECENT POST END --> 사이의 부분을 찾아 교체
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

# README.md 파일에 업데이트된 내용 쓰기 (내용이 변경된 경우에만)
if updated_readme != original_readme:
    with open(readme_path, 'w', encoding='utf-8') as readme_md_file:
        readme_md_file.write(updated_readme)

    # 파일의 길이를 맞추기 위해 남는 부분을 삭제
    with open(readme_path, 'a', encoding='utf-8') as readme_md_file:
        readme_md_file.truncate()
else:
    print("no change. no update")