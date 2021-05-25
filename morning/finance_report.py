import telegram
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler 
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

my_token = '1234'
chat_id = 12344

bot = telegram.Bot(token=my_token)
options = Options()
options.add_argument('--start-fullscreen')
driver = webdriver.Chrome('/home/ubuntu/chromedriver', chrome_options=options)

def morning_summary():
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

def bitcoin_price_dollar() :
    cmcURL = 'https://coinmarketcap.com/currencies/bitcoin/'
    driver.get(cmcURL)
    driver.implicitly_wait(time_to_wait=2)
    element = driver.find_element_by_xpath('//*[@id="__next"]/div/div[1]/div[2]/div/div[1]/div[2]/div[2]/div[1]/div').text

    text = '비트코인 달러가는 '
    text2 = '입니다.'
    result = text + element + text2
    driver.close()
    return result

def bitcoin_dominance() :
    URL = 'https://coinmarketcap.com/ko/'
    driver.get(URL)
    driver.implicitly_wait(time_to_wait=2)
    driver.find_element_by_xpath('//*[@id="__next"]/div/div[1]/div[2]/div/div/section/div[1]/div[1]/div/div').click()
    element = driver.find_element_by_xpath('//*[@id="__next"]/div/div[1]/div[2]/div/div/section/div[1]/div[2]/div/p[3]').text

    driver.close()
    return element

def fear_greed_index() : 
    URL = 'https://alternative.me/crypto/fear-and-greed-index/'
    driver.get(URL)
    driver.implicitly_wait(time_to_wait=2)
    driver.find_element_by_xpath('//*[@id="history"]/div[3]').screenshot(r'/home/ubuntu/important_data/fear_greed_graph_screenshot.png')

    driver.close()



# message reply function
def get_message(update, context) :
    update.message.reply_text("got text")
    update.message.reply_text(update.message.text)


# rate reply function
def get_morning_summary(update, context) :
    update.message.reply_text("잠시만 기다려 주세요!")
    morning_summary()

def get_bitcoin_price(update, context) :
    update.message.reply_text("잠시만 기다려 주세요!")
    text = bitcoin_price_dollar()
    bot.sendMessage(chat_id=chat_id, text=text)

def get_bitcoin_dominance(update, context) :
    update.message.reply_text("잠시만 기다려 주세요!")
    text = bitcoin_dominance()
    bot.sendMessage(chat_id=chat_id, text=text)

def get_fear_greed_index(update, context) :
    update.message.reply_text("잠시만 기다려 주세요!")
    fear_greed_index()
    bot.sendPhoto(chat_id=chat_id, photo=open('/home/ubuntu/important_data/fear_greed_graph_screenshot.png', 'rb'))

updater = Updater(my_token, use_context=True)

message_handler = MessageHandler(Filters.text & (~Filters.command), get_message) # 메세지중에서 command 제외
updater.dispatcher.add_handler(message_handler)

morning_summary_handler = CommandHandler('morning', get_morning_summary)
updater.dispatcher.add_handler(morning_summary_handler)

bitcoin_price_handler = CommandHandler('bitcoin', get_bitcoin_price)
updater.dispatcher.add_handler(bitcoin_price_handler)

bitcoin_dominance_handler = CommandHandler('domi', get_bitcoin_dominance)
updater.dispatcher.add_handler(bitcoin_dominance_handler)

fear_greed_index_handler = CommandHandler('fgindex', get_fear_greed_index)
updater.dispatcher.add_handler(fear_greed_index_handler)

updater.start_polling(timeout=3, clean=True)
updater.idle()


