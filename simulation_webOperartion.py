import time

from selenium import webdriver
url = 'https://shopee.tw/buyer/login'
option = webdriver.ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])
option.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=option)
driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',
                       {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
                        })
driver.get(url)
input('click to input account and password')
#
account = 'jahonleu'
password = 'Hugest1146'
driver.find_element('xpath', '//*[@id="main"]/div/div[2]/div/div/div/div[2]/form/div/div[2]/div[2]/div[1]/input').send_keys(account)
driver.find_element('xpath', '//*[@id="main"]/div/div[2]/div/div/div/div[2]/form/div/div[2]/div[3]/div[1]/input').send_keys(password)
time.sleep(2)
driver.find_element('css selector', '#main > div > div.vtexOX > div > div > div > div:nth-child(2) > form > div > div.yXry6s > button').click()
driver.find_element('xpath', '//*[@id="main"]/div/div[2]/div/div/div/div[1]/div/div/div/button')
input()
