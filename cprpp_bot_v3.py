import logging
import hashlib
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

# Глобальная переменная для хранения дерева
tree = None

# Функция для чтения content.txt и обработки его
def process_content_file():
    with open('content.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    tree = {'children': {}}  # Убедитесь, что корень имеет ключ 'children'
    stack = [tree]
    for line in lines:
        depth = line.count('\t')
        text = line.strip()
        
        if text.startswith("(") and text.endswith(")"):
            # Случай с выводом текста
            if stack:
                if 'text' not in stack[-1]:
                    stack[-1]['text'] = []
                stack[-1]['text'].append(text)
        else:
            # Создаем новую запись в иерархии
            node = {'text': [], 'children': {}}
            if depth < len(stack):
                stack = stack[:depth + 1]
            stack[-1]['children'][text] = node
            stack.append(node)
    
    return tree

# Создаем первый уровень KeyboardButtons
def create_main_keyboard():
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    if tree and 'children' in tree:
        for key in tree['children'].keys():
            markup.add(KeyboardButton(key))
    return markup

# Создаем уникальные данные для callback_data
def create_callback_data(text):
    return hashlib.sha1(text.encode()).hexdigest()

# Создаем InlineKeyboardMarkup для следующего уровня
def create_inline_markup(node):
    markup = InlineKeyboardMarkup(row_width=1)
    if node and 'children' in node:
        for key in node['children'].keys():
            callback_data = create_callback_data(key)
            markup.add(InlineKeyboardButton(key, callback_data=callback_data))
    return markup

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    global tree
    tree = process_content_file()  # Загружаем дерево из файла
    bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=create_main_keyboard())

# Обработчик сообщений для первого уровня кнопок
@bot.message_handler(func=lambda message: tree and 'children' in tree and message.text in tree['children'])
def send_submenu(message):
    node = tree['children'][message.text]
    if 'children' in node and node['children']:
        # Если у узла есть дочерние элементы, создаем InlineKeyboardMarkup
        bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=create_inline_markup(node))
    elif node['text']:
        # Если у узла есть текст, выводим все строки в чат
        for text in node['text']:
            bot.send_message(message.chat.id, text, parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, "Больше опций нет.", reply_markup=None)

# Обработчик callback-запросов для InlineKeyboardButtons
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    node = find_node_by_callback(tree, call.data)
    
    if node:
        if 'children' in node and node['children']:
            bot.send_message(call.message.chat.id, "Выберите опцию:", reply_markup=create_inline_markup(node))
        elif node['text']:
            for text in node['text']:
                bot.send_message(call.message.chat.id, text, parse_mode='Markdown')
        else:
            bot.send_message(call.message.chat.id, "Больше опций нет.", reply_markup=None)

def find_node_by_callback(current_node, callback_data):
    for key, child in current_node['children'].items():
        if create_callback_data(key) == callback_data:
            return child
        result = find_node_by_callback(child, callback_data)
        if result:
            return result
    return None

# Запуск бота
bot.polling()