# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "0075ACDD5E431C471100BF1477F4C5C4D1C8603494A82D62D6047B4C3332E0F0ADAE37D7CA7B56B92F2AB811A9106B6B9BD68EF36C6DCD07F482B488A721796F9828D2489EAEA0B3D6A2FCD1710EAFB62928DA0E1FAF898AA3FCD4D5CC2EFBC8B5F9E031193D53467BCC9B7ACB6E8B9F7B47680D2C6774769306E60370EFCF25EB2B266D6EC4F583056128B04B1625768E71EC985DC0680F7297694236E55E9D7B20BD2D4BC352ABD079A974AD2503E24929BD9CBFAA631575E609353F0607B2C35A8C1A0FAE87A693AFEF416B3722080851D62ABF8AE4532646D1A5978F5555E0A20C5D44613F7BC8C54480092770913D75D390863475F1B7DC9A86684DCF89ED1AF7173F80567758BF39629B08F2DB3701DBF4ED46AD0282863D919D766B420C1D73B2402E37C353F85DAB40DDEB9C3B99AA5BEFC01688593AEF7E410DF7B399CE39E4B77F50A1D7EF0EEBEFB63A28EBBFC8A21367A43815169ACF7666FD5EB0"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
