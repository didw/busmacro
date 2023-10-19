# 버스 예약 자동화 스크립트

이 스크립트는 Selenium을 사용하여 T-money 웹사이트에서 버스 예약 가능 여부를 확인하고, 예약이 가능하면 Telegram 메시지를 보내는 기능을 제공합니다.

## 설정

1. **Telegram Bot 생성**: 
   - Telegram에서 BotFather를 통해 봇을 생성합니다.
   - 생성한 봇에서 토큰을 얻습니다.
2. **Chat ID 확인**: 
   - Telegram에서 `@userinfobot`을 통해 개인 채팅의 ID를 얻습니다.

## 코드

### Telegram 설정

```python
from telegram import Bot
import asyncio

TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"
bot = Bot(token=TOKEN)

async def send_telegram_message(message):
    await bot.send_message(chat_id=CHAT_ID, text=message)
```

### 웹드라이버 설정 및 웹사이트 방문
```python
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://txbus.t-money.co.kr/otck/trmlInfEnty.do")
```

### 예약 여부 확인 및 Telegram 메시지 전송
```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

loop = asyncio.get_event_loop()
if loop.is_closed():
    asyncio.set_event_loop(asyncio.new_event_loop())

while True:
    driver.refresh()
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, 'YOUR_BUTTON_XPATH'))
    )
    if button.text == '예약하기':
        loop.run_until_complete(send_telegram_message("예약 가능"))
        button.click()
        break
    else:
        loop.run_until_complete(send_telegram_message("예약 불가능"))
        time.sleep(10)
        continue
```

### 주의사항
- `YOUR_TELEGRAM_BOT_TOKEN`, `YOUR_CHAT_ID`, `YOUR_BUTTON_XPATH` 위치에 알맞은 값을 입력해주세요.
- Selenium을 사용하여 웹사이트를 스크래핑할 때는 해당 웹사이트의 이용 약관을 반드시 확인하고 이용해주세요.

