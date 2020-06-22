import telebot
from telebot import types
import sqlite3
import wikipediaapi

BOT_TOKEN = ''
wiki_wiki = wikipediaapi.Wikipedia('ru')
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)


@bot.message_handler(commands=['start'])
def send_welcome(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
	btn1 = types.KeyboardButton('Терминология')
	btn2 = types.KeyboardButton('Философы')
	btn3 = types.KeyboardButton('Философские течения')
	markup.add(btn1, btn2, btn3)
	bot.send_message(message.chat.id, "🤖 Бот запущен!\n⚙Что Вас интересует?", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def term(message):
	chat_id = message.chat.id
	if message.text == 'Терминология':
		markup_term = telebot.types.ReplyKeyboardMarkup(True, False)
		markup_term.row('А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж')
		markup_term.row('З', 'И', 'К', 'Л', 'М', 'Н', 'О')
		markup_term.row('П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Э')
		bot.send_message(chat_id, "Вы выбрали раздел, хранящий в себе термины", reply_markup=markup_term)
	msg = bot.reply_to(message, """Нажмите на первую букву искомого термина""")
	bot.register_next_step_handler(msg, send_letter_list)

dict_of_letters = {'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ж': 'ZH', 'З': 'Z',
					'И': 'I', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R',
					'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'PH', 'Х': 'H', 'Э': 'EE'}


@bot.message_handler(content_types=['text'])
def send_letter_list(message):
	letter = dict_of_letters.get(message.text)
	con = sqlite3.connect("baseforbot.db")
	letter_list = ''
	cursor = con.cursor()
	with con:
		cursor.execute("SELECT ID, name, link FROM Terminology WHERE alpha = '{}'".format(letter))
		while True:
			row = cursor.fetchone()
			if row == None:
				break
			letter_list = letter_list + "{}: {}\n".format(row[1], row[2])
	bot.send_message(message.chat.id, 'Выберите термин:\n' + letter_list)



bot.polling()
