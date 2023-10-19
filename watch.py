import time
import asyncio
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from telegram import Bot

TOKEN = "6842213660:AAFw2x8JyqJgSTVexfavkaRmhJQ4LI_zJo0"
CHAT_ID = "33009331"

bot = Bot(token=TOKEN)

driver = webdriver.Chrome(service= Service(ChromeDriverManager().install()))

# 웹사이트 방문
driver.get("https://txbus.t-money.co.kr/otck/trmlInfEnty.do")

time.sleep(5)
# # 출발지 설정
departure = driver.find_element(By.NAME, "depr_Trml_Nm")  # id나, xpath, css_selector 등으로 요소를 찾을 수 있습니다.
departure.click()
time.sleep(1)
departure = driver.find_element(By.XPATH, "//*[contains(text(), '동서울')]")
departure.click()
time.sleep(1)

# 도착지 설정
destination = driver.find_element(By.NAME, "arvl_Trml_Nm")
destination.click()
time.sleep(5)
departure = driver.find_element(By.XPATH, "//*[contains(text(), '한계령')]")
departure.click()
time.sleep(1)

# 달력에서 21일 선택
departure = driver.find_element(By.NAME, "depr_Dt")
departure.click()
time.sleep(1)
departure = driver.find_element(By.XPATH, '//*[@id="ui-datepicker-div"]/table/tbody/tr[3]/td[7]/a')
departure.click()
time.sleep(1)

# scroll down
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# 조회
departure = driver.find_element(By.XPATH, '//*[@id="onewayInfo"]/div/p[2]/a/span[1]')
departure.click()
time.sleep(2)  # 팝업 창이 완전히 뜰 때까지 기다립니다. 필요한 경우 시간을 조절해주세요.
alert = driver.switch_to.alert
alert.accept()

time.sleep(10)

async def send_telegram_message(message):
    await bot.send_message(chat_id=CHAT_ID, text=message)

while True:
    # refresh
    driver.refresh()
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="contents"]/div[2]/div/div[3]/div/div[4]/table/tbody/tr[5]/td[7]/div/a'))
    )
    if button.text == '예약하기':
        loop = asyncio.get_event_loop()
        loop.run_until_complete(send_telegram_message("예약 가능"))
        button.click()
        break
    else:
        # loop = asyncio.get_event_loop()
        # loop.run_until_complete(send_telegram_message("예약 불가능"))
        print("예약 불가능.. 다시 조회합니다.")
        time.sleep(10)
        continue
