import json
import logging
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

try:
	with open('token.txt', 'r', encoding='utf-8') as file:
		my_token = file.read().strip()
except FileNotFoundError:
	logging.error("Файл token.txt не найден")
	file.close
	exit(1)
except Exception as exception_error:
	logging.error(f"При чтении файла token.txt возникла ошибка: {exception_error}")
	file.close
	exit(1)

bot = telebot.TeleBot(my_token)

def loadConfig():
	with open('content.json', 'r', encoding='utf-8') as file:
		tree = json.load(file)
		file.close()
	return tree
	
def getNode(tree, buttonName = ''):
	if buttonName == '':
		return tree
	for node in tree['children']:
		if node['button_name'] == buttonName:
			return node
		if 'children' in node:
			result_node = getNode(node, buttonName)
			if result_node:
				return result_node 

def generateMarkup(node):
	if 'children' not in node:
		return None
	markup = InlineKeyboardMarkup()	
	for button in node['children']:
		markup.add(InlineKeyboardButton(button['button_name'], callback_data=button['button_name']))
	return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
	node = getNode(config, call.data)
	bot.send_message(call.message.chat.id, node['desc'], reply_markup=generateMarkup(node))

@bot.message_handler(func=lambda message: True)
def message_handler(message):
	bot.send_message(message.chat.id, config['desc'], reply_markup=generateMarkup(config))

config = loadConfig()

try:
	bot.infinity_polling()
except Exception as exception_error:
	logging.error(f"При обращении к Telegram API возникла ошибка: {exception_error}")
	bot.stop_polling()
	exit(1)