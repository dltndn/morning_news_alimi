import telegram
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--start-fullscreen')


def clsoe_chromedriver() :
    driver = webdriver.Chrome('C:/Users/james/Desktop/morning_news_alimi/chromedriver.exe', chrome_options=options)
    cmcURL = 'https://coinmarketcap.com/currencies/bitcoin/'
    driver.get(cmcURL)
    driver.implicitly_wait(time_to_wait=2)
    element = driver.find_element_by_xpath('//*[@id="__next"]/div/div[1]/div[2]/div/div[1]/div[2]/div[2]/div[1]/div').text
    print(type(element))
    driver.close()

def bitcoin_dominance() :
    driver = webdriver.Chrome('C:/Users/james/Desktop/morning_news_alimi/chromedriver.exe', chrome_options=options)
    URL = 'https://coinmarketcap.com/ko/'
    driver.get(URL)
    driver.implicitly_wait(time_to_wait=2)
    driver.find_element_by_xpath('//*[@id="__next"]/div/div[1]/div[2]/div/div/section/div[1]/div[1]/div/div').click()
    element = driver.find_element_by_xpath('//*[@id="__next"]/div/div[1]/div[2]/div/div/section/div[1]/div[2]/div/p[3]').text
    print(element)

def bitcoin_price_dollar() :
    driver = webdriver.Chrome('C:/Users/james/Desktop/morning_news_alimi/chromedriver.exe', chrome_options=options)
    cmcURL = 'https://coinmarketcap.com/currencies/bitcoin/'
    driver.get(cmcURL)
    driver.implicitly_wait(time_to_wait=2)
    element = driver.find_element_by_xpath('//*[@id="__next"]/div/div[1]/div[2]/div/div[1]/div[2]/div[2]/div[1]/div').text

    text = '비트코인 달러가는 '
    text2 = ' 입니다.'
    result = text + element + text2
    driver.close()
    return result

text = bitcoin_price_dollar()
print(text)


# my_token = '1234'   #토큰을 변수에 저장합니다.

# bot = telegram.Bot(token = my_token)   #bot을 선언합니다.

# updates = bot.getUpdates()  #업데이트 내역을 받아옵니다.

# for u in updates :   # 내역중 메세지를 출력합니다.

#     print(u.message)

    
    

# '/home/ubuntu/morning_news_alimi/morning/chromedriver.exe'

