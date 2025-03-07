# 데이터 수집 적재 자동화

1. 크롤링을 통한 채용공고, 뉴스 데이터 수집 - WebCrawling.py, NewsCrawling.py
2. 수집한 데이터를 전처리한 후 Google BigQuery 적재 - Preprocessing.py, UploadGCP.py
3. GCP 인스턴스를 생성한 후 cron을 통해 해당 과정을 자동화
4. 빅쿼리에 적재된 데이터를 태블로와 연동
5. 태블로 대시보드로 시각화
6. 슬랙을 통한 작업 완료 알림 - slackbot.py
