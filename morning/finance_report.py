import telegram
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

my_token = '1234'
chat_id = 1134

bot = telegram.Bot(token=my_token)

options = Options()
options.add_argument('--start-fullscreen')
driver = webdriver.Chrome(r'C:/Users/james/Desktop/morning_news/morning/chromedriver.exe', chrome_options=options)

def crawling_screenshot() :
    usd_materialsURL = 'https://finance.naver.com/marketindex/'

    find_xpath = {
        'finance' : ['https://finance.naver.com/world/', '//*[@id="wrap"]/div[1]', 'finance'],
        'fear_greed' : ['https://alternative.me/crypto/fear-and-greed-index/', '//*[@id="main"]/section/div/div[3]', 'fear_greed'],
        'btcvolume' : ['https://www.cryptocompare.com/coins/btc/analysis/KRW', '//*[@id="col-body"]/div/div[2]/div[3]/div[1]/symbol-tosymbol-share-table/div/div/table', 'btcvolume'],
    }

    keys = find_xpath.keys()
    
    def screenshot(name) :
        png_name = f'/home/ubuntu/important_data/{name}_screenshot.png'
        driver.get(find_xpath[name][0])
        driver.implicitly_wait(time_to_wait=5)
        driver.find_element_by_xpath(find_xpath[name][1]).screenshot(png_name)
        bot.sendPhoto(chat_id=chat_id, photo=open(png_name, 'rb'))

    driver.get(usd_materialsURL)  
    driver.implicitly_wait(time_to_wait=1)
    element1 = driver.find_element_by_xpath('//*[@id="worldExchangeList"]/li[4]')
    element2 = driver.find_element_by_xpath('//*[@id="oilGoldList"]/li[3]')
    ActionChains(driver).click_and_hold(element1).perform()
    ActionChains(driver).click_and_hold(element2).perform()
    driver.find_element_by_xpath('//*[@id="container"]/div[1]/div').screenshot(r'/home/ubuntu/important_data/usd_materials_screenshot.png')
    bot.sendPhoto(chat_id=chat_id, photo=open('/home/ubuntu/important_data/usd_materials_screenshot.png', 'rb'))

    for k in keys : 
        screenshot(k)


def crawling_text() :
    cmcURL = 'https://coinmarketcap.com/ko/' 
    kimchi_premiumURL = 'https://scolkg.com/'

    driver.get(cmcURL)
    driver.implicitly_wait(time_to_wait=2)
    driver.find_element_by_xpath('//*[@id="__next"]/div/div[1]/div[2]/div/div/section/div[1]/div[1]/div/div').click()
    tv = driver.find_element_by_xpath('//*[@id="__next"]/div/div[1]/div[2]/div/div/section/div[1]/div[1]/div/p').text
    bit_domi = driver.find_element_by_xpath('//*[@id="__next"]/div/div[1]/div[2]/div/div/section/div[1]/div[2]/div/p[3]').text
    
    driver.get(kimchi_premiumURL)
    driver.implicitly_wait(time_to_wait=3)
    kimchi = driver.find_element_by_xpath('//*[@id="app_section"]/div[1]/div[5]/div/div/div[5]/div[2]/div[1]/span').text

    return tv, bit_domi, kimchi


def sending_information() :
    text1, text2, text3 = crawling_text()
    text3 = '실시간 김치프리미엄은 ' + text3 + ' 입니다.'
    text_sum = text1 + '\n' + text2 + '\n' + text3
    bot.sendMessage(chat_id=chat_id, text=text_sum)

crawling_screenshot()
sending_information()

driver.close()


