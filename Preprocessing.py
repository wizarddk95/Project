import pandas as pd
import re
from collections import Counter

# 파일 로드
file_path = "job_information.csv"  # 파일 경로를 실제 경로로 변경

df = pd.read_csv(file_path)

data_analyst_keywords = [
    # 프로그래밍 언어
    "Python", "파이썬", "R", "SQL", "MySQL", "PostgreSQL", "BigQuery",
    # 데이터 처리 및 분석
    "데이터", "분석", "Pandas", "NumPy", "Spark", "ETL", "데이터베이스",
    # 머신러닝/딥러닝 관련
    "머신러닝", "딥러닝", "AI", "모델링", "예측",
    # 통계 및 수학 관련
    "통계", "회귀", "가설검정", "확률", "통계학",
    # 데이터 시각화 관련
    "Tableau", "Power BI", "시각화", "대시보드",
    # 비즈니스 분석 관련
    "A/B 테스트", "KPI", "인사이트", "최적화",
    # 클라우드 및 배포 관련
    "AWS", "GCP", "Azure", "API", "배포"
]

# 불필요한 기호 제거 및 단어 추출 함수
def simple_tokenize(text):
    text = re.sub(r'\n|\[.*?\]|[^가-힣a-zA-Z0-9\s]', ' ', text)  # 특수문자 제거
    words = text.split()  # 공백 기준 분할
    return [word for word in words if len(word) > 1]  # 한 글자 단어 제외

# 회사별, 카테고리별 핵심 단어 추출
word_freq_by_company_category = {}

for (company, category), group in df.groupby(["회사", "카테고리"]):
    words = []
    for content in group["내용"]:
        words.extend(simple_tokenize(content))
    
    # 단어 빈도수 계산
    word_counts = Counter(words)
    
    # 상위 단어 선택 (데이터 분석 키워드만 필터링)
    filtered_counts = {word: count for word, count in word_counts.items() if word in data_analyst_keywords}
    
    # "데이터"와 "분석"을 "데이터 분석"으로 통합
    filtered_counts["데이터 분석"] = filtered_counts.get("데이터", 0) + filtered_counts.get("분석", 0)
    filtered_counts.pop("데이터", None)
    filtered_counts.pop("분석", None)
    
    # 저장
    word_freq_by_company_category[(company, category)] = sorted(filtered_counts.items(), key=lambda x: x[1], reverse=True)

# 데이터프레임 변환
word_freq_df = pd.DataFrame(
    [(company, category, word, count) for (company, category), words in word_freq_by_company_category.items() for word, count in words],
    columns=["회사", "카테고리", "단어", "빈도"]
)

# 결과 저장
word_freq_df.to_csv('wrod_statistics.csv', index=False, encoding='utf-8-sig')

# 결과 출력
word_freq_df.head()  # 상위 몇 개 행만 출력
