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
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Selenium 감지 방지
chrome_options.add_argument("--remote-debugging-port=9222")  # 디버깅 활성화
chrome_options.add_argument("--window-size=1920x1080")  # 창 크기 지정
chrome_options.add_argument("--start-maximized")  # 창 최대화

# ChromeDriver 설정 및 실행
service = Service(ChromeDriverManager().install())  # Service 객체 사용
driver = webdriver.Chrome(service=service, options=chrome_options)

# 1. 웹 드라이버 실행
driver.get("https://www.wanted.co.kr")

# 2. WebDriverWait 설정
wait = WebDriverWait(driver, 10) # 10초가 지나도 요소가 나타나지 않으면 오류 발생

# 2.5 버튼 닫기
close_xpath = '/html/body/div[2]/div/div/button'

try:
    close_button = wait.until(EC.element_to_be_clickable((By.XPATH, close_xpath)))
    close_button.click()
except:
    print("기본 클릭 실패, ActionsChains 사용")

    try:
        menu_button = driver.find_element(By.XPATH, close_xpath)
        ActionChains(driver).move_to_element(close_button).click().perform()
    except Exception as e:
        print(f"ActionChians 클릭 실패: {e}")

# 3. 네비게이터 검색 버튼 클릭
menu_xpath = '//*[@id="__next"]/div[1]/div[2]/nav/aside/ul/li[1]/button'

try:
    menu_button = wait.until(EC.element_to_be_clickable((By.XPATH, menu_xpath)))
    menu_button.click()
except:
    print("기본 클릭 실패, ActionChains 사용")

    try:
        menu_button = driver.find_element(By.XPATH, menu_xpath)
        ActionChains(driver).move_to_element(menu_button).click().perform()
    except Exception as e:
        print(f"ActionChains 클릭 실패: {e}")

# 검색창 찾기 및 검색어 입력
search_xpath = '//*[@id="nav_searchbar"]/div/div[2]/div/form/input'

try:
    search_box = wait.until(EC.presence_of_element_located((By.XPATH, search_xpath)))
    search_box.send_keys("데이터 분석가")
    search_box.send_keys(Keys.RETURN)
except:
    print("검색창을 찾을 수 없음")

# 포지션 전체보기 클릭
total_position_xpath = '//*[@id="search_tabpanel_overview"]/div[1]/div[3]/button'

try:
    total_position_button = wait.until(EC.element_to_be_clickable((By.XPATH, total_position_xpath)))
    total_position_button.click()
except:
    print("기본 클릭 실패, ActionChains 사용")

    try:
        total_position_button = driver.find_element(By.XPATH, total_position_xpath)
        ActionChains(driver).move_to_element(total_position_button).click().perform()
    except Exception as e:
        print(f"ActionChains 클릭 실패: {e}")


# 스크롤을 끝까지 내리면서 채용 공고를 모두 로딩
def scroll_down():
    # 초기 페이지 높이
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # 스크롤 다운
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        # 새로운 페이지 높이 확인
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        # 스크롤 후에도 높이가 변하지 않으면 로딩 완료
        if new_height == last_height:
            print("모든 공고가 로드됨!")
            break
        last_height = new_height

# 스크롤 끝까지 내리기
scroll_down()

# 모든 채용 공고 요소 가져오기
xpath = '//*[@id="search_tabpanel_position"]/div/div[3]/div'
job_elements = driver.find_elements(By.XPATH, xpath)

job_links = []
for job in job_elements:
    try:
        # 공고 링크 추출
        link = job.find_element(By.TAG_NAME, "a").get_attribute("href")
        job_links.append(link)
    except:
        continue

print(f"총 {len(job_links)}개의 채용 공고 수집 완료!")

job_data = []
for job_link in tqdm(job_links):
    # 개별 공고 페이지 이동
    driver.get(job_link)
    time.sleep(2)

    company_xpath = '//*[@id="__next"]/main/div[1]/div/section/header/div/div[1]/a'
    company = driver.find_element(By.XPATH, company_xpath).text

    detail_information_xpath = '//*[@id="__next"]/main/div[1]/div/section/section/article[1]/div/button/span[2]'

    try:
        detail_information_button = wait.until(EC.element_to_be_clickable((By.XPATH, detail_information_xpath)))
        detail_information_button.click()
    except:
        
        try:
            # 요소 다시 찾기
            detail_information_button = driver.find_element(By.XPATH, detail_information_xpath)
            ActionChains(driver).move_to_element(detail_information_button).click().perform()
        except Exception as e:
            print(f"ActionChains 클릭 실패 {e}")

    # h3 탐색 (자격요건, 우대사항)
    h3s = driver.find_elements(By.XPATH, '//*[@id="__next"]/main/div[1]/div/section/section/article[1]/div/div/h3')

    for h3 in h3s:
        h3_text = h3.text.strip()
    
        # 자격요건 또는 우대사항이 포함된 경우만 처리
        if "주요업무" in h3_text or "자격요건" in h3_text or "우대사항" in h3_text:
            # 해당 제목의 부모 div에서 span/span 내부 텍스트 가져오기
            contents = h3.find_elements(By.XPATH, "./following-sibling::span/span")
            content_text = " ".join([c.text.strip() for c in contents]) if contents else "내용 없음"
            job_data.append({"회사": company, "카테고리":h3_text, "내용": content_text, "링크": job_link})

    # 뒤로 가기
    driver.back()

    # 채용 공고 리스트가 다시 로드될 때까지 대기
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="search_tabpanel_position"]/div/div[3]/div')))

# 데이터 저장
df = pd.DataFrame(job_data)
df.to_csv("job_information.csv", index=False, encoding='utf-8-sig')

print("모든 공고 크롤링 완료!")
driver.quit()
