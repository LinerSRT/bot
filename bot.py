import time, re, telebot, random
import urllib
import urllib.request
from urllib.request import Request
import sqlite3
import database, config

STOP_SPAM = False

commands = {
    '▫️ /stats' 	  	: 'Показать статистику флудерастов из чата',
    '▫️ /finish_him' 	  	: 'Оскорбить жертву, пример: /finish_him @Victim',
    '▫️ /corona' 	  	    : 'Статистика коронавируса в мире 🌎',
    '▫️ /corona_uk' 	  	: 'Статистика коронавируса в Украине 🇺🇦',
    '▫️ /corona_ru' 	  	: 'Статистика коронавируса в России 🇷🇺',
    '🔸 /spam' 	  	        : 'Отправить спам сообщения, /spam [количество] [текст]🔸',
    '🔸 /stop_spam' 		: 'Остановить спам🔸',
    '▫️/whoisyourdaddy' 	: 'Узнать создателя бота',
    '🔸 /showpic' 		    : '🚫🌶🍓 Загрузить в чат картинку с 18+ содержанием🔸',
    '🔸 /showgif' 		    : '🚫🌶🍓 Загрузить в чат гифку с 18+ содержанием🔸',
    '▫️ /saysome' 		    : 'Сказать рандомную фразу',
    '▫️ /admins' 		    : 'Список админов',
    '▫️ /banlist' 		    : 'Список забаненых',
    '🔺 /add' 		        : 'Добавить админа',
    '🔺 /remove' 		    : 'Удалить админа',
}

def isOwner(user):
    if user == "Llne_R":
        return True
    else:
        return False

database.createBOT_DB()
database.createChatStatDB()

banned_text = ["ты в бане, пиздуй отсюда",
    "еблан, теперь ты забанен",
    "затнись, тебе слова не давали",
    "чмо ебаное",
    "умоляй, что бы я тебя разбанил",
    "тупой дебил",
    "долбоеб, ты забанен"]
def listener(messages):
    for m in messages:
        if m.from_user.username is not None:
            if database.check_if_STAT_exist(m.from_user.username) == True:
                database.update_STAT_DB([m.from_user.username, str(int(database.get_STAT_count(m.from_user.username))+1)])
            else:
                database.insert_to_STAT_DB([m.from_user.username, '1'])
            if database.checkUser("banned", m.from_user.username) == True:
                bot.send_message(m.chat.id, "@" + m.from_user.username + ", " + random.choice(banned_text),
                             getMAT("@" + m.from_user.username))


bot = telebot.TeleBot(config.TOKEN)
bot.set_update_listener(listener)



@bot.message_handler(commands=["admins"])
def answer(message):
    cid = message.chat.id
    time.sleep(2)
    bot.send_message(cid, "Список админов:\n"+database.getAdmins())

@bot.message_handler(commands=["stats"])
def answer(message):
    cid = message.chat.id
    time.sleep(2)
    bot.send_message(cid, "Список флудерастов:\n---------------------\n"+database.get_STAT(), parse_mode= 'Markdown')


@bot.message_handler(commands=["banlist"])
def answer(message):
    cid = message.chat.id
    time.sleep(2)
    bot.send_message(cid, "Список забаненых:\n"+database.getBanned())

@bot.message_handler(commands=["add"])
def answer(message):
    cid = message.chat.id
    time.sleep(2)
    if isOwner(message.from_user.username) == True:
        database.insert_to_BOT_DB("admins", message.text.split(maxsplit=1)[1].replace("@", ""))
        bot.send_message(cid, "Новый пользователь добавлен")
        bot.send_message(cid, "Список админов:\n"+database.getAdmins())
    else:
        bot.send_message(cid, "Доступно только для создателя")

@bot.message_handler(commands=["remove"])
def answer(message):
    cid = message.chat.id
    time.sleep(2)
    if isOwner(message.from_user.username) == True:
        database.delete_from_BOT_DB("admins", message.text.split(maxsplit=1)[1].replace("@", ""))
        bot.send_message(cid, message.text.split(maxsplit=1)[1]+" больше не админ")
        bot.send_message(cid, "Список админов:\n"+database.getAdmins())
    else:
        bot.send_message(cid, "Доступно только для создателя")

@bot.message_handler(commands=["ban_him"])
def answer(message):
    cid = message.chat.id
    time.sleep(2)
    if isOwner(message.from_user.username) == True:
        database.insert_to_BOT_DB("banned", message.text.split(maxsplit=1)[1].replace("@", ""))
        bot.send_message(cid, "Забанил, теперь ему пиздец")
    else:
        bot.send_message(cid, "Доступно только для создателя")

@bot.message_handler(commands=["unban_him"])
def answer(message):
    cid = message.chat.id
    time.sleep(2)
    if isOwner(message.from_user.username) == True:
        database.delete_from_BOT_DB("banned", message.text.split(maxsplit=1)[1].replace("@", ""))
        bot.send_message(cid, message.text.split(maxsplit=1)[1]+" больше не в бане")
    else:
        bot.send_message(cid, "Доступно только для создателя")

@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = "\n"
    for key in commands:
        help_text += key + ": "
        help_text += commands[key] + "\n----------------------\n"
    help_text += "▫ - доступно всем \n🔸 - доступно только админам\n🔺 - доступно только создателю"
    bot.send_message(m.chat.id, "Привет, " + str(m.from_user.username) + " рад снова тебя видеть. Вот что я могу:\n" + help_text)

@bot.message_handler(commands=["spam"])
def answer(message):
    try:
        global STOP_SPAM
        chat_id = message.chat.id
        amount = message.text.split(maxsplit=2)[1]
        spam_text = message.text.split(maxsplit=2)[2]
        if database.checkUser("admins",message.from_user.username) == True:
            if checkUserInString("admins", spam_text) == False:
                if isOwner(message.from_user.username) == True:
                    for i in range(0, int(amount)):
                        if STOP_SPAM == True:
                            STOP_SPAM = False
                            break
                        else:
                            time.sleep(0.5)
                            bot.send_message(chat_id, ""+spam_text)
                else:
                    if int(amount) < 101:
                        for i in range(0, int(amount)):
                            if STOP_SPAM == True:
                                STOP_SPAM = False
                                break
                            else:
                                time.sleep(2)
                                bot.send_message(chat_id, ""+spam_text)
                    else:
                        bot.send_message(chat_id, "Максимум, 50")
            else:
                bot.send_message(chat_id, "Нельзя использовать против админов :)")
        
        else:
            bot.send_message(chat_id, "Вы обычный пользователь, повторю только один раз :)")
            if checkUserInString("admins", spam_text) == False:
                time.sleep(2)
                bot.send_message(chat_id, ""+spam_text)
            else:
                bot.send_message(chat_id, "Нельзя использовать против админов :)")
    except:
        bot.send_message(chat_id, "Упс, что-то пошло не так, используйте /spam [количество] [текст]")

@bot.message_handler(commands=["stop_spam"])
def answer(message):
    global STOP_SPAM
    if database.checkUser("admins", message.from_user.username) == True:
        STOP_SPAM = True
    else:
        bot.send_message(message.chat.id, "Доступно только админам")

@bot.message_handler(commands=["corona"])
def answer(message):
    req = Request("https://www.worldometers.info/coronavirus", headers={'User-Agent': 'Mozilla/5.0'})
    resource = urllib.request.urlopen(req)
    content =  resource.read().decode(resource.headers.get_content_charset())
    corona_cases_count = re.search(r'Coronavirus Cases:[a-zA-Z<>\": 0-9\/\n=\-#]*>([0-9, ]*)<', content).group(1)
    corona_death_count = re.search(r'Deaths:[a-zA-Z<>\": 0-9\/\n=\-#]*>([0-9, ]*)<', content).group(1)
    corona_survive_count = re.search(r'Recovered:[a-zA-Z<>\": 0-9\/\n=\-#]*>([0-9, ]*)<', content).group(1)
    result = "Ситуация в 🌎 мире на данный момент\n"
    result += "🦠 Заражено: "+corona_cases_count+"\n"
    result += "☠ Умерло: "+corona_death_count+"\n"
    result += "＋ Выздоровело: "+corona_survive_count+"\n"
    result += "-----------\n"
    result += "НАМ ВСЕМ ПИЗДА!\n"

    bot.send_message(message.chat.id, result)
    
@bot.message_handler(commands=["corona_uk"])
def answer(message):
    req = Request("https://www.worldometers.info/coronavirus/country/ukraine", headers={'User-Agent': 'Mozilla/5.0'})
    resource = urllib.request.urlopen(req)
    content =  resource.read().decode(resource.headers.get_content_charset())
    corona_cases_count = re.search(r'Coronavirus Cases:[a-zA-Z<>\": 0-9\/\n=\-#]*>([0-9, ]*)<', content).group(1)
    corona_death_count = re.search(r'Deaths:[a-zA-Z<>\": 0-9\/\n=\-#]*>([0-9, ]*)<', content).group(1)
    corona_survive_count = re.search(r'Recovered:[a-zA-Z<>\": 0-9\/\n=\-#]*>([0-9, ]*)<', content).group(1)
    result = "Ситуация в 🇺🇦 Украине на данный момент\n"
    result += "🦠 Заражено: "+corona_cases_count+"\n"
    result += "☠ Умерло: "+corona_death_count+"\n"
    result += "＋ Выздоровело: "+corona_survive_count+"\n"
    bot.send_message(message.chat.id, result)

@bot.message_handler(commands=["corona_ru"])
def answer(message):
    req = Request("https://www.worldometers.info/coronavirus/country/russia", headers={'User-Agent': 'Mozilla/5.0'})
    resource = urllib.request.urlopen(req)
    content =  resource.read().decode(resource.headers.get_content_charset())
    corona_cases_count = re.search(r'Coronavirus Cases:[a-zA-Z<>\": 0-9\/\n=\-#]*>([0-9, ]*)<', content).group(1)
    corona_death_count = re.search(r'Deaths:[a-zA-Z<>\": 0-9\/\n=\-#]*>([0-9, ]*)<', content).group(1)
    corona_survive_count = re.search(r'Recovered:[a-zA-Z<>\": 0-9\/\n=\-#]*>([0-9, ]*)<', content).group(1)
    result = "Ситуация в 🇷🇺 России на данный момент\n"
    result += "🦠 Заражено: "+corona_cases_count+"\n"
    result += "☠ Умерло: "+corona_death_count+"\n"
    result += "＋ Выздоровело: "+corona_survive_count+"\n"
    bot.send_message(message.chat.id, result)
    
@bot.message_handler(commands=["whoisyourdaddy"])
def answer(message):
    cid = message.chat.id
    time.sleep(2)
    bot.send_message(cid, "Меня написал - @Llne_R")

random_words = ["Я использую машинное обучение, что бы понимать тебя.",
    "Half-Life 3 выйдет в 2023 году.",
    "FATAL EXCEPTION! Unknown command handled! -Err no. 290",
    "Вы мне отвратительны!",
    "Прости, но я тебя не понимаю.",
    "Попробуй еще разок.",
    "Хм, мне кажется в чате есть долбоеб и мне кажется это явно не я",
    "Видишь суслика?",
    "Опять ты... Я скоро тебя буду игнорировать",
    "Массоны! Они уже здесь! Беги, беги!!!",
    "Ебать какой я оригинальный да?",
    "Ставь кастом и не еби мозг",
    "Ыыыы...",
    "Странно, да?"]
@bot.message_handler(commands=["saysome"])
def answer(message):
	cid = message.chat.id
	bot.send_message(cid, random.choice(random_words))

@bot.message_handler(commands=['showgif'])
def answer(message):
    if database.checkUser("admins", message.from_user.username) == True:
        try:
            req = Request("http://www.gifporntube.com/gifs/"+str(random.randint(20, 2000))+".html", headers={'User-Agent': 'Mozilla/5.0'})
            resource = urllib.request.urlopen(req)
            content = resource.read().decode(resource.headers.get_content_charset())
            urls = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+([/a-z_0-9]*.mp4)', content)
            markdown = "[.](http://www.gifporntube.com" + str(urls[0]) + ")"
            bot.send_message(message.chat.id, markdown, parse_mode="Markdown")
        except:
            bot.send_message(message.chat.id, "Упс, что-то пошло не так.")
    else:
        bot.send_message(message.chat.id, "Достпуно только для админов, соси бибу")

@bot.message_handler(commands=['showpic'])
def send_photo(message):
    if database.checkUser("admins", message.from_user.username) == True:
        try:
            data = urllib.request.urlopen(
                "https://www.scrolller.com/media/" + str(random.randint(20, 2000)) + ".jpg").read()
            f = open('out.jpg', 'wb')
            f.write(data)
            f.close()
            img = open('out.jpg', 'rb')
            bot.send_photo(message.chat.id, img)
            img.close()
        except:
            bot.send_message(message.chat.id, "Упс, что-то пошло не так.")
    else:
        bot.send_message(message.chat.id, "Достпуно только для админов, соси бибу")

@bot.message_handler(commands=['finish_him'])
def answer(message):
        try:
            name = message.text.split(maxsplit=1)[1]
            if isOwner(name.replace("@", "")) == True:
                bot.send_message(message.chat.id, "Я тебе щас еблет разорву, нельзя гнать на создателя")
            else:
                bot.send_message(message.chat.id, getMAT(name.replace("@", "")))
        except:
            bot.send_message(message.chat.id, "Упс, что-то пошло не так.")


def getMAT(name):
    req = Request("https://damn.ru/?name="+name+"&sex=m", headers={'User-Agent': 'Mozilla/5.0'})
    resource = urllib.request.urlopen(req)
    content = resource.read().decode(resource.headers.get_content_charset())
    querry = re.search(r'<div class="text">([a-zA-Zа-яА-Я, Ёё]*)<span class=\"name\">'+name+'<\/span> &mdash;([a-zA-Zа-яА-Я, Ёё]*)', content)
    return querry.group(1)+"@"+name+""+querry.group(2)

#while True:
#    text = input("Text:")
#    chat_id = -1001351933744
#    bot.send_message(chat_id, text)

bot.polling(interval=2)
