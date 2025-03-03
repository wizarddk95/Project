from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from tqdm import tqdm

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Chrome 옵션 설정 (헤드리스 모드)
chrome_options = Options()
chrome_options.add_argument("--headless")  # UI 없이 실행

# ChromeDriver 설정 및 실행
service = Service(ChromeDriverManager().install())  # Service 객체 사용
driver = webdriver.Chrome(service=service, options=chrome_options)

# 1. 웹 드라이버 실행
driver.get("https://www.wanted.co.kr")

# 2. WebDriverWait 설정
wait = WebDriverWait(driver, 10) # 10초가 지나도 요소가 나타나지 않으면 오류 발생
dd = driver.page_source
print(dd)
