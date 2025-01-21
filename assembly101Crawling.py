from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# ChromeDriver 경로 설정
driver_path = "C:/Download/chromedriver-win64/chromedriver-win64/chromedriver.exe"  # chromedriver 경로로 변경
url = "https://assembly101.kr/" # 시작 URL

# Selenium WebDriver 설정
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # 브라우저 창을 띄우지 않음
driver = webdriver.Chrome(options=options)

# 사이트 열기
driver.get(url)
wait = WebDriverWait(driver, 30) # 최대 20초 대기

# Crawling Data 저장용 리스트
data = []
try:
    while True:
        # 1. 첫번째 grid 클릭
        first_grid = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "member-card"))
        )
        ActionChains(driver).move_to_element(first_grid).click().perform()

        # 2. 이름 및 URL 추출
        time.sleep(2)
        name_element = driver.find_elements(By.CLASS_NAME, "name-kr bold-text")
        url_element = driver.current_url

        for name, url in zip(name_element, url_element):
            data.append({
                "name": name.text.strip(),
                "url": url
            })

        # 3. 다음 페이지 버튼 클릭
        try:
            # 다음 버튼 찾기
            next_button = wait.until(
                EC.element_to_be_clickable((By.CLASS_NAME, "move-to-next"))
            )
            next_button.click()  # 버튼 클릭
            time.sleep(2)  # 다음 페이지 로딩 대기
        except Exception as e:
            print("다음 버튼을 찾을 수 없거나 마지막 페이지입니다.")
            break
finally:
    driver.quit()

# 결과 출력
print("Extracted Names:")
for i in range(len(data)):
    print(data[i]['name'])
    print(data[i]['url'])

df = pd.DataFrame(data)
df.to_csv("assembly_names_urls.csv", index=False, encoding="utf-8-sig")
print("크롤링 완료! 데이터가 'assembly_names_urls.csv'에 저장되었습니다.")