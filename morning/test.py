import telegram


my_token = '1234'   #토큰을 변수에 저장합니다.

bot = telegram.Bot(token = my_token)   #bot을 선언합니다.

updates = bot.getUpdates()  #업데이트 내역을 받아옵니다.

for u in updates :   # 내역중 메세지를 출력합니다.

    print(u.message)