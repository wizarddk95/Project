# 데이터 수집 적재 자동화

1. 크롤링을 통한 데이터 수집 (BeautifulSoup, Selenium)
2. 수집한 데이터를 전처리한 후 Google BigQuery 적재
3. GCP 인스턴스를 생성한 후 cron을 통해 해당 과정을 자동화
4. 빅쿼리에 적재된 데이터를 태블로와 연동
5. 태블로 대시보드로 시각화
