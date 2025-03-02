import pandas as pd
from google.oauth2 import service_account
from google.cloud import bigquery

# 서비스 계정 키 파일 경로 (내려받은 JSON 키 파일 사용)
KEY_PATH = ""

# BigQuery 데이터셋 ID
DATASET_ID = "mydataset"

def upload_to_bigquery(file_path, table_id):
    """
    CSV 파일을 BigQuery 테이블로 업로드하는 함수

    Args:
        file_path (str): 업로드할 CSV 파일 경로
        table_id (str): BigQuery 테이블 ID
    """
    try:
        # 데이터 불러오기
        df = pd.read_csv(file_path)

        # 서비스 계정 키 인증
        credentials = service_account.Credentials.from_service_account_file(KEY_PATH)
        client = bigquery.Client(credentials=credentials, project=credentials.project_id)

        # 테이블 전체 경로 설정
        table_full_id = f"{client.project}.{DATASET_ID}.{table_id}"

        # BigQuery에 데이터 적재
        job = client.load_table_from_dataframe(df, table_full_id)
        job.result() # 완료될 때까지 대기

        print(f"{file_path} 데이터가 {table_full_id} 테이블에 성공적으로 업로드되었습니다!")

    except Exception as e:
        print(f"{file_path} 데이터 업로드 실패: {e}")

# 업로드 실행
upload_to_bigquery("job_information.csv", 'job_information')
upload_to_bigquery("wrod_statistics.csv", 'word_statistics')
