import time, re, telebot, random, csv
from PIL import Image, ImageDraw
from io import BytesIO
import shutil
import urllib
import requests
from telebot import types
import urllib.request, json
import lxml.html
import data
knownUsers = []
userStep = {} 
WEATHER_TOKEN = '*********************************'
IP_TOKEN = '*************************************'
commands = {
    'spam' 	  	: 'Отправить 10 сообщений с вашим текстом',
    'whoisyourdaddy' 	: 'Узнать создателя бота',
    'showpic' 		: 'Загрузить в чат картинку с 18+ содержанием',
    'saysome' 		: 'Сказать рандомную фразу',
    'weather' 		: 'Узнать погоду, использование <город> <страна>',
    'generateface' 		: 'Сгенерировать случайное лицо используя маски, к сожалению поддерживается текст только на английском, использование <любые символы>',
    'genmem' 		: 'Сгенерировать мем, к сожалению поддерживается текст только на английском, использование <ключ> <текст сверху> <текст снизу>',
    'memlist' 		: 'Показать доступные ключи для genmem',
    'say' 		: 'Сгенерирует голосовое сообщение из текста, поддержывает только русский язык. Пробел между словами создается знаком -',
    'whois' 		: 'Используйте /whois <IP адрес>, что бы узнать информацию об IP',
    'howmuch' 		: 'Показать пасхалку',
    'porngif' 		: 'Показать 18+ гифку. Использование /porngif <число> (числа от 50, до хуй его знает :D). Если не сработало, попробуйте другое число',
}

def listener(messages):
	for m in messages:
		if m.content_type == 'text':
			if re.match(r'[а-яА-яa-zA-Z0-9,\.! ]*(орео*)[а-яА-яa-zA-Z0-9,\.! ]*', m.text) is not None:
				bot.send_message(m.chat.id, "Android 8.1 на Doogee X5 Pro еще не готов, Llne_R не знает как чинить связь, так что отьебись")
			print(str(m.from_user.username) + " [" + str(m.chat.id) + "]: " + m.text)


bot = telebot.TeleBot(data.TOKEN)
bot.set_update_listener(listener)

@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = "\n"
    for key in commands:
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n---------------------------------------------------------------------------------------\n"
    bot.send_message(m.chat.id, "Привет, " + str(m.from_user.username) + " рад снова тебя видеть. Вот что я могу:\n" + help_text)

@bot.message_handler(commands=["spam"])
def answer(message):
    cid = message.chat.id
    test = message.text
    val = test.split(maxsplit=1)[1]
    if val == "@Line_R" or val == "@Llne_R" or val == "@Llne_r" or val == "@linehelp_bot" or val == "@rock12345":
    	bot.send_message(cid, "Простите, но " + val + " сейчас не доступен")
    else:
    	for i in range(1,21):
    		time.sleep(2)
    		bot.send_message(cid, "№" + str(i) + " " + val)

@bot.message_handler(commands=["whoisyourdaddy"])
def answer(message):
    cid = message.chat.id
    time.sleep(2)
    bot.send_message(cid, "Меня написал - @Llne_R")

@bot.message_handler(commands=["saysome"])
def answer(message):
	lst = ["Я использую машинное обучение, что бы понимать тебя.", "Half-Life 3 выйдет в 2023 году.", "Ошибка! Вызов в функции int(), завершился с ошибкой: 1.", "Вы мне отвратительны!", "Прости, но я тебя не понимаю.", "Попробуй еще разок."]
	cid = message.chat.id
	test = message.text
	textrand = random.randint(0,5)
	bot.send_message(cid, lst[textrand])

@bot.message_handler(commands=['showpic'])
def send_photo(message):
	def check_img(data):
		try:
			data = urllib.request.urlopen("https://www.scrolller.com/media/" + str(random.randint(20,2000)) + ".jpg").read()
			f = open('out.jpg','wb')
			f.write(data)
			f.close()
			img = open('out.jpg', 'rb')
			bot.send_photo(message.chat.id, img)
			img.close()
		except:
			bot.send_message(message.chat.id, "Cервис сейчас не доступен! Попробуйте еще раз!")
			return False
	print(str(message.from_user.username))
	if str(message.from_user.username) == "ZessL" or str(message.from_user.username) == "ZessLL":
		bot.send_message(message.chat.id, "Простите но сервис для вас не доступен!")
	else:
		check_img(urllib.request.urlopen("https://www.scrolller.com/media/" + str(random.randint(20,5000)) + ".jpg").read())

@bot.message_handler(commands=["weather"])
def answer(message):
	cid = message.chat.id
	arg = message.text.split(" ")
	def check(url):
		try:
			url = urllib.request.urlopen("https://api.weatherbit.io/v2.0/current?city="+str(arg[1])+","+str(arg[2])+"&key="+WEATHER_TOKEN)
			data = json.loads(url.read().decode())
			data_array = "Город: "+data["data"][0]["city_name"]+"\nТемпература: "+str(data["data"][0]["temp"])+" ℃\nОщущается как: "+str(data["data"][0]["app_temp"])+" ℃\nВосход: "+data["data"][0]["sunrise"]+"\nЗакат: "+data["data"][0]["sunset"]+"\nДавление: "+str(data["data"][0]["pres"])+" мм рт. ст.\nСкорость ветра: "+str(data["data"][0]["wind_spd"])+" м/с\nНаправление ветра: "+str(data["data"][0]["wind_dir"])
			bot.send_message(cid, data_array)
		except:
			bot.send_message(cid, "Погода для города |"+str(arg[1])+"| и страны |"+str(arg[2])+"| не найдена, скорее всего вы ввели неверные данные, либо сервис сейчас не доступен!")
			return False
	check("https://api.weatherbit.io/v2.0/current?city="+str(arg[1])+","+str(arg[2])+"&key="+WEATHER_TOKEN)


@bot.message_handler(commands=['generateface'])
def send_photo(message):
	cid = message.chat.id
	arg = message.text.split(" ")
	size_arg = len(arg)
	if size_arg < 3:
		print("Data:")
	else:
		print("GET:")
	def check_service(data):
		try:
			data = urllib.request.urlopen("https://api.adorable.io/avatars/241/"+str(arg[1])+".png").read()
			f = open('out.jpg','wb')
			f.write(data)
			f.close()
			img = open('out.jpg', 'rb')
			bot.send_photo(message.chat.id, img)
			img.close()
		except:
			bot.send_message(message.chat.id, "Cервис сейчас не доступен! Попробуйте еще раз!")
			return False
	check_service(urllib.request.urlopen("https://api.adorable.io/avatars/241/"+str(arg[1])+".png").read())


@bot.message_handler(commands=['genmem'])
def send_photo(message):
	cid = message.chat.id
	arg = message.text.split(" ")
	markdown = "[.](https://memegen.link/"+str(arg[1])+"/"+str(arg[2])+"/"+str(arg[3])+".jpg)"
	bot.send_message(message.chat.id, markdown, parse_mode="Markdown")
	
@bot.message_handler(commands=['memlist'])
def send_photo(message):
	cid = message.chat.id
	arg = message.text.split(" ")
	meme_list = "\n"
	for key in data.memes:
		meme_list += "key: "+key + "  ---  "
		meme_list += data.memes[key] + "\n"
	meme_list += "Использование: /genmem <key> <text> <text>\n"	
	bot.send_message(message.chat.id, "Avilable meme\'s list is:\n" + meme_list)

@bot.message_handler(commands=['say'])
def test_send_message_with_markdown(message):
	arg = message.text.split(" ")
	markdown = "[.](http://api.voicerss.org/?key="+data.params["key"]+"&hl="+data.params["hl"]+"&c=mp3&f=44khz_16bit_stereo&src="+str(arg[1])+")"
	bot.send_message(message.chat.id, markdown, parse_mode="Markdown")

@bot.message_handler(commands=['howmuch'])
def test_send_message_with_markdown(message):
	resource = urllib.request.urlopen("http://4pda.ru/forum/index.php?act=idx#stats")
	content =  resource.read().decode(resource.headers.get_content_charset())
	page = lxml.html.fromstring(content)
	title = page.xpath('//*[@id="ShowUsersInOnline_head"]/a[2]/text()')[0]
	users = title.split(" ")
	bot.send_message(message.chat.id, "На сайте 4pda.ru зарегистрированно:"+users[0]+" долбоеба(ов)")

@bot.message_handler(commands=["whois"])
def answer(message):
	cid = message.chat.id
	arg = message.text.split(" ")
	print(arg)
	def check(url):
		try:
			url = urllib.request.urlopen("http://api.ipstack.com/"+arg[1]+"?access_key="+IP_TOKEN)
			data = json.loads(url.read().decode())
			print(data)
			bot.send_message(message.chat.id, "IP: "+data["ip"]+"\nТип: "+data["type"]+"\nСтрана: "+data["location"]["country_flag_emoji"]+" "+data["country_name"]+"\nГород: "+data["city"]+"\nИндекс: "+str(data["zip"])+"\nШирота: "+str(data["latitude"])+"\nДолгота: "+str(data["longitude"])+"\nНомер страны: "+str(data["location"]["calling_code"]))
			
		except:
			bot.send_message(cid, "Ошибка! Данный IP в данный момент не доступен или не существует. Используйте /whois <IP адрес>")
			return False
	check("http://api.ipstack.com/"+arg[1]+"?access_key="+IP_TOKEN)

@bot.message_handler(commands=['porngif'])
def send_photo(message):
	arg = message.text.split(" ")
	resource = urllib.request.urlopen("http://www.gifporntube.com/gifs/"+str(arg[1])+".html")
	content =  resource.read().decode(resource.headers.get_content_charset())
	urls = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+([/a-z_0-9]*.mp4)', content)
	print("http://www.gifporntube.com"+urls[0]+ "  arg:"+str(arg[1]))
	markdown = "[.](http://www.gifporntube.com"+str(urls[0])+")"
	bot.send_message(message.chat.id, markdown, parse_mode="Markdown")

bot.polling(interval=2)
