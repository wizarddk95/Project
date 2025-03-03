import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

# 네이버 금융 뉴스 URL
url = "https://finance.naver.com/news/mainnews.naver"

# HTML 요청
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# 기사 리스트 선택
news_list = soup.select(".newsList li")

news_df = []
for news in news_list:
    # 기사 제목 & 링크
    title_tag = news.select_one(".articleSubject a")
    if title_tag:
        title = title_tag.text.strip()
        raw_link = title_tag["href"]

        article_id_match = re.search(r'article_id=(\d+)', raw_link)
        office_id_match = re.search(r'office_id=(\d+)', raw_link)

        # 값이 존재하는 경우 추출
        if article_id_match and office_id_match:
            article_id = article_id_match.group(1)
            office_id = office_id_match.group(1)

            # 변환된 URL 생성
            base_url = 'https://n.news.naver.com/mnews/article'
            link = f"{base_url}/{office_id}/{article_id}"
    
    # 기사 요약
    summary_tag = news.select_one(".articleSummary")
    summary = summary_tag.text.strip() if summary_tag else "요약 없음"

    # 언론사
    press_tag = news.select_one(".press")
    press = press_tag.text.strip() if press_tag else "출처 없음"

    # 날짜
    date_tag = news.select_one(".wdate")
    date = date_tag.text.strip() if date_tag else "날짜 없음"

    news_df.append({
        '제목': title,
        '링크': link,
        '요약': summary,
        '언론사': press,
        '날짜': date
    })
df = pd.DataFrame(news_df)

df.to_csv('news_summary.csv', index=False, encoding='utf-8-sig')
print('csv 파일 저장 완료')

print(df.head())
