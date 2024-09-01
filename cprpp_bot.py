#pyTelegramBotAPI
#~/bots/cprpp_bot.py

import logging
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

logging.basicConfig(filename='errors.log', level=logging.ERROR, format='%(asctime)s--%(levelname)s--%(message)s', encoding='utf-8')

try:
    with open('token.txt', 'r', encoding='utf-8') as file:
        my_token = file.read().strip()
except FileNotFoundError:
    logging.error("Файл token.txt не найден")
    exit(1)
except Exception as Err:
    logging.error(f"При чтении файла token.txt возникла ошибка: {Err}")
    exit(1)

bot = telebot.TeleBot(my_token)

def create_markup(buttons):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(*[KeyboardButton(btn) for btn in buttons])
    return markup

def screen_1():
    buttons = [
        "🏫 Освітній процес",
        "Контакти",
        "🎨 Позаурочна діяльність",
        "Проєктна діяльність",
        "💡 Підвищення кваліфікації",
        ">>>>>"
    ]
    return create_markup(buttons)

def screen_2():
    buttons = [
        "🗂️ Учнівська документація",
        "Корисні посилання",
        "🔍 Звіти",
        "📝 Заяви",
        "Психологична служба",
        "Бібліотека",
        "<<<<<"
    ]
    return create_markup(buttons)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    text = ("Привіт! Я твій чат-бот.\n"
            "Відвідайте наш [сайт](https://www.avdiivkacprpp.pp.ua) для отримання додаткової інформації.\n"
            "Приєднуйтесь до нашого [Telegram-каналу](https://t.me/+oj9EtMrcl38wZWEy/)\n"
            "Приєднуйтесь до нашого [YouTube-каналу](https://www.youtube.com/@avdiivkacprpp/playlists/)")
    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=screen_1())

@bot.message_handler(commands=['mailme'])
def send_welcome(message):
    text = ("Скористайтеся можливістю дати [Зворотний зв'язок](https://forms.gle/7ovuJqqyxmFRv7Vq5/)")
    bot.send_message(message.chat.id, text, parse_mode='Markdown')


@bot.message_handler(func=lambda message: message.text == ">>>>>")
def next_screen(message):
    if message.text == ">>>>>":
        current_screen = screen_2()
    elif message.text == "<<<<<":
        current_screen = screen_1()
    bot.send_message(message.chat.id, "Оберіть одну з опцій нижче:", reply_markup=current_screen)

@bot.message_handler(func=lambda message: message.text == "<<<<<")
def prev_screen(message):
    if message.text == "<<<<<":
        current_screen = screen_1()
    elif message.text == ">>>>>":
        current_screen = screen_2()
    bot.send_message(message.chat.id, "Оберіть одну з опцій нижче:", reply_markup=current_screen)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == "🏫 Освітній процес":
        markup = InlineKeyboardMarkup(row_width=1)
        buttons = [
            InlineKeyboardButton("🧠 Навчальний", callback_data="Навчальний"),
            InlineKeyboardButton("🌱 Виховний", callback_data="Виховний")
         ]
        markup.add(*buttons)
        bot.send_message(message.chat.id, "Оберіть необхідне:", reply_markup=markup)

    elif message.text == "Контакти":
        markup = InlineKeyboardMarkup(row_width=1)
        buttons = [
            InlineKeyboardButton("ЦПРПП", callback_data="AddLnks"),
            InlineKeyboardButton("Відділ освіти", callback_data="AddLnks"),
            InlineKeyboardButton("Заклади освіти", callback_data="AddLnks"),
            InlineKeyboardButton("ІППО", callback_data="AddLnks")
         ]
        markup.add(*buttons)
        bot.send_message(message.chat.id, "Оберіть необхідне:", reply_markup=markup)

    elif message.text == "🎨 Позаурочна діяльність":
        markup = InlineKeyboardMarkup(row_width=1)
        buttons = [
            InlineKeyboardButton("Олімпіади", callback_data="AddLnks"),
            InlineKeyboardButton("🏆 Конкурси", callback_data="Конкурси"),
            InlineKeyboardButton("ЗНО, НМТ", callback_data="AddLnks"),
            InlineKeyboardButton("ДПА", callback_data="AddLnks")
        ]
        markup.add(*buttons)
        bot.send_message(message.chat.id, "Оберіть необхідне:", reply_markup=markup)

    elif message.text == "Проєктна діяльність":
        markup = InlineKeyboardMarkup(row_width=1)
        buttons = [
            InlineKeyboardButton("Освітні", callback_data="AddLnks"),
            InlineKeyboardButton("Учнівські", callback_data="AddLnks"),
            InlineKeyboardButton("Для вчителів", callback_data="AddLnks")
        ]
        markup.add(*buttons)
        bot.send_message(message.chat.id, "Оберіть необхідне:", reply_markup=markup)

    elif message.text == "💡 Підвищення кваліфікації":
        markup = InlineKeyboardMarkup(row_width=1)
        buttons = [
            InlineKeyboardButton("Положення", callback_data="AddLnks"),
            InlineKeyboardButton("ЦПРПП", callback_data="AddLnks"),
            InlineKeyboardButton("ІППО", callback_data="AddLnks"),
            InlineKeyboardButton("Інші ресурси ПК", callback_data="AddLnks"),
            InlineKeyboardButton("Вчитель року", callback_data="AddLnks"),
            InlineKeyboardButton("🏅 Сертифікація", callback_data="Сертифікація"),
            InlineKeyboardButton("Маршрут професійного розвитку педагога", callback_data="AddLnks")
        ]
        markup.add(*buttons)
        bot.send_message(message.chat.id, "Оберіть необхідне:", reply_markup=markup)

    elif message.text == "🗂️ Учнівська документація":
        markup = InlineKeyboardMarkup(row_width=1)
        buttons = [
            InlineKeyboardButton("🗃️ Особова справа (зразок)", url="https://docs.google.com/document/d/1Zsj6vH-vG18eQhyvfwsmH3EbQoB7pc69ZyfCoeJE-A0/edit?usp=sharing/"),
            InlineKeyboardButton("📑 Табель (зразок)", url="https://docs.google.com/document/d/18nP0iWG-5ovWa9EBgtpsh5e_9KKwNC0gX2C6z7OaaLA/edit?usp=sharing/"),
            InlineKeyboardButton("Соціальний паспорт (зразок)", callback_data="AddLnks"),
            InlineKeyboardButton("Свідоцтво досягнень учнів", callback_data="AddLnks"),
            InlineKeyboardButton("📋 Характеристика", url="https://docs.google.com/document/d/1ed8Zo00Jz8Khkc6PBFIL5ZpZHmMHPUC9DkaXiOTZqhs/edit?usp=sharing/")
        ]
        markup.add(*buttons)
        bot.send_message(message.chat.id, "Оберіть необхідне:", reply_markup=markup)


    elif message.text == "Корисні посилання":
        markup = InlineKeyboardMarkup(row_width=1)
        buttons = [
#############################################
            InlineKeyboardButton("?????", callback_data="AddLnks")
        ]
        markup.add(*buttons)
        bot.send_message(message.chat.id, "Оберіть необхідне:", reply_markup=markup)

    elif message.text == "🔍 Звіти":
        markup = InlineKeyboardMarkup(row_width=1)
        buttons = [
            InlineKeyboardButton("👨‍👩‍👧‍👦 Виховна робота", callback_data="Виховна робота"),
            InlineKeyboardButton("Навчальні досягнення учнів", callback_data="AddLnks"),
            InlineKeyboardButton("Вчителя-предметника", callback_data="AddLnks")
        ]
        markup.add(*buttons)
        bot.send_message(message.chat.id, "Оберіть необхідне:", reply_markup=markup)

    elif message.text == "📝 Заяви":
        markup = InlineKeyboardMarkup(row_width=1)
        buttons = [
            InlineKeyboardButton("📌 Доручення", url="https://docs.google.com/document/d/1ptR4x2GWApSMO_4GapmI1FgVI2len45V0BINdj_olog/edit?usp=sharing/"),
            InlineKeyboardButton("🖋️ Розписка", url="https://docs.google.com/document/d/1FtfMGr7ZmtTsE8StHRbpQzgjP9w0x8UA57tczxXFeQ8/edit?usp=sharing/"),
            InlineKeyboardButton("✍️ До 10-го класу", url="https://docs.google.com/document/d/1SDYp6TIkFzno_owMQS_AyD2Td7WT6Jzl2_FukKPR6zw/edit?usp=sharing/"),
            InlineKeyboardButton("✅ Довідка зі школи", url="https://docs.google.com/document/d/1z5iQLuGsY5VVspe5YdVexTIpmoLnmS0AD1XMdYymap0/edit?usp=sharing/"),
            InlineKeyboardButton("🏖️ Поділ основної відпустки", url="https://docs.google.com/document/d/159GB6Kr71kE3kzDpWwj5j5gkPTbN-897VnCquU6bf6o/edit?usp=sharing/"),
            InlineKeyboardButton("Відпустка", callback_data="AddLnks"),
            InlineKeyboardButton("Звільнення", callback_data="AddLnks"),
            InlineKeyboardButton("Сумісництво", callback_data="AddLnks"),
            InlineKeyboardButton("Прийняття на роботу", callback_data="AddLnks"),
            InlineKeyboardButton("Відпустка власним коштом", callback_data="AddLnks")
        ]
        markup.add(*buttons)
        bot.send_message(message.chat.id, "Оберіть необхідне:", reply_markup=markup)

    elif message.text == "Психологична служба":
        markup = InlineKeyboardMarkup(row_width=1)
        buttons = [
###############################################
            InlineKeyboardButton("?????", callback_data="AddLnks")
        ]
        markup.add(*buttons)
        bot.send_message(message.chat.id, "Оберіть необхідне:", reply_markup=markup)

    elif message.text == "Бібліотека":
        markup = InlineKeyboardMarkup(row_width=1)
        buttons = [
            InlineKeyboardButton("Підручники та методички", callback_data="Підручники та методички"),
            InlineKeyboardButton("Кіно", callback_data="AddLnks"),
            InlineKeyboardButton("Художня література", callback_data="AddLnks"),
            InlineKeyboardButton("Онлайн подорожі", callback_data="AddLnks")
        ]
        markup.add(*buttons)
        bot.send_message(message.chat.id, "Оберіть необхідне:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "Навчальний":
        markup = InlineKeyboardMarkup(row_width=1)
        buttons = [
            InlineKeyboardButton("📚 Модельні навчальні програми", callback_data="Модельні навчальні програми"),
            InlineKeyboardButton("📝 Освітні програми (орієнтовні)", callback_data="Освітні програми (орієнтовні)"),
            InlineKeyboardButton("📋 Календарне планування (орієнтовне)", callback_data="Календарне планування (орієнтовне)"),
            InlineKeyboardButton("💡Навчальні платформи (цікавинки)", callback_data="Навчальні платформи (цікавинки)"),
            InlineKeyboardButton("🎯 Критерії оцінювання", callback_data="Критерії оцінювання")
        ]
        markup.add(*buttons)
        bot.send_message(call.message.chat.id, "Оберіть необхідне:", reply_markup=markup)

    elif call.data == "Щорічні для учнів":
        markup = InlineKeyboardMarkup(row_width=1)
        buttons = [
            InlineKeyboardButton("📖 Мовно-літературна", callback_data="Мовно-літературна. Конкурси"),
            InlineKeyboardButton("🔢 Математична", url="https://www.kangaroo.com.ua/"),
            InlineKeyboardButton("Природнича", callback_data="AddLnks"),
            InlineKeyboardButton("Технологічна", callback_data="AddLnks"),
            InlineKeyboardButton("Інформатична", callback_data="AddLnks"),
            InlineKeyboardButton("Громадянська та історична", callback_data="AddLnks"),
            InlineKeyboardButton("Мистецька", callback_data="AddLnks"),
            InlineKeyboardButton("Соціальна і здоров'язбережувальна", callback_data="AddLnks"),
            InlineKeyboardButton("Фізична культура", callback_data="AddLnks"),
            InlineKeyboardButton("Міжгалузеві інтегровані курси", callback_data="AddLnks")
        ]
        markup.add(*buttons)
        bot.send_message(call.message.chat.id, "Оберіть галузь:", reply_markup=markup)

    elif call.data == "Календарне планування (орієнтовне)":
        markup = InlineKeyboardMarkup(row_width=1)
        buttons = [
            InlineKeyboardButton("📖 Мовно-літературна", callback_data="Мовно-літературна. Планування"),
            InlineKeyboardButton("🔢 Математична", url="https://www.schoollife.org.ua/zbirnyk-kalendarno-tematychnyh-planuvan-z-matematyky-algebry-ta-geometriyi-na-2024-2025-n-r/"),
            InlineKeyboardButton("Природнича", callback_data="AddLnks"),
            InlineKeyboardButton("Технологічна", callback_data="AddLnks"),
            InlineKeyboardButton("💻 Інформатична", url="https://www.schoollife.org.ua/zbirnyk-kalendarno-tematychnyh-planuvan-z-informatyky-na-2024-2025-n-r/"),
            InlineKeyboardButton("Громадянська та історична", callback_data="AddLnks"),
            InlineKeyboardButton("Мистецька", callback_data="AddLnks"),
            InlineKeyboardButton("Соціальна і здоров'язбережувальна", callback_data="AddLnks"),
            InlineKeyboardButton("Фізична культура", callback_data="AddLnks"),
            InlineKeyboardButton("Міжгалузеві інтегровані курси", callback_data="AddLnks")
        ]
        markup.add(*buttons)
        bot.send_message(call.message.chat.id, "Оберіть галузь:", reply_markup=markup)

    elif call.data == "Виховний":
        markup = InlineKeyboardMarkup(row_width=1)
        buttons = [
            InlineKeyboardButton("🕊️ Національно-патриотичне", callback_data="Національно-патриотичне"),
            InlineKeyboardButton("Правове", callback_data="AddLnks"),
            InlineKeyboardButton("Екологічне", callback_data="AddLnks"),
            InlineKeyboardButton("Профорієнтація", callback_data="AddLnks"),
            InlineKeyboardButton("Морально-етичне", callback_data="AddLnks"),
            InlineKeyboardButton("Бесіди, інструктажі", callback_data="AddLnks")
        ]
        markup.add(*buttons)
        bot.send_message(call.message.chat.id, "Оберіть необхідне:", reply_markup=markup)

    elif call.data == "Конкурси":
        markup = InlineKeyboardMarkup(row_width=1)
        buttons = [
            InlineKeyboardButton("Для вчителів", callback_data="AddLnks"),
            InlineKeyboardButton("📅 Щорічні для учнів", callback_data="Щорічні для учнів"),
            InlineKeyboardButton("Періодичні для учнів", callback_data="AddLnks")
        ]
        markup.add(*buttons)
        bot.send_message(call.message.chat.id, "Оберіть необхідне:", reply_markup=markup)

    elif call.data == "Виховна робота":
        markup = InlineKeyboardMarkup(row_width=1)
        buttons = [
            InlineKeyboardButton("📈 Звіт", url="https://docs.google.com/document/d/1lGpFpwq7mdilrUkbBriySwPRezugtqne0EV-hhDZdH4/edit?usp=sharing/"),
            InlineKeyboardButton("📊 Аналіз", url="https://docs.google.com/document/d/1N7lBkBQ4U2QBjujvC4vbA4zyuiphKGPRw158DfPZccU/edit?usp=sharing/")
        ]
        markup.add(*buttons)
        bot.send_message(call.message.chat.id, "Оберіть необхідне:", reply_markup=markup)

    elif call.data == "Підручники та методички":
        markup = InlineKeyboardMarkup(row_width=1)
        buttons = [
            InlineKeyboardButton("Підручники", callback_data="AddLnks"),
            InlineKeyboardButton("Додаткова література", callback_data="AddLnks")
        ]
        markup.add(*buttons)
        bot.send_message(call.message.chat.id, "Оберіть необхідне:", reply_markup=markup)

    elif call.data == "Модельні навчальні програми":
        bot.send_message(call.message.chat.id, f"{call.data}:")
        text = ("Модельні та навчальні програми. [Що спільного і чим відрізняються?](https://znayshov.com/News/Details/shcho_spilnoho_i_chym_vidrizniaiutsia_modelni_ta_navchalni_prohramy/)")
        bot.send_message(call.message.chat.id, text, parse_mode='Markdown')

    elif call.data == "Освітні програми (орієнтовні)":
        bot.send_message(call.message.chat.id, f"{call.data}:")
        text = ("Конструктор програм. [Відеопосібник](https://youtu.be/Z2uQYOasJgs?si=tzFDhUldNV7JdLke/) користувача")
        bot.send_message(call.message.chat.id, text, parse_mode='Markdown')
        text = ("Нові рекомендації [оцінювання](https://nus.org.ua/news/u-mon-rozrobyly-novi-rekomendatsiyi-otsinyuvannya-uchniv-5-9-klasiv/) учнів 5-9 класів")
        bot.send_message(call.message.chat.id, text, parse_mode='Markdown')

    elif call.data == "Навчальні платформи (цікавинки)":
        bot.send_message(call.message.chat.id, f"{call.data}:")
        text = ("Безплатні колекції [відео](https://ua.pistacja.tv/)")
        bot.send_message(call.message.chat.id, text, parse_mode='Markdown')

    elif call.data == "Критерії оцінювання":
        bot.send_message(call.message.chat.id, f"{call.data}:")
        text = ("Наказ МОН №1093 ['Про затвердження рекомендацій щодо оцінювання результатів навчання'](https://drive.google.com/file/d/12_-OmNV3f07uLyjPuLZb5y2hM5ShqgTk/view?usp=drive_link/)\n\n"
                "Методичні рекомендації ['Оцінювання навчальних досягнень учнів з ООП'](https://drive.google.com/file/d/1bD92UNuxi14tW6PJnccv-aLTN2f3TjIc/view?usp=drive_link/)")
        bot.send_message(call.message.chat.id, text, parse_mode='Markdown')
        text = ("[Критерії оцінювання на Освіта.UA](https://osvita.ua/school/estimation/)")
        bot.send_message(call.message.chat.id, text, parse_mode='Markdown')

    elif call.data == "Мовно-літературна. Планування":   
        bot.send_message(call.message.chat.id, f"{call.data}:")
        text = ("[Зарубіжна література](https://www.schoollife.org.ua/zbirnyk-kalendarno-tematychnyh-planuvan-zarubizhnoyi-literatury-na-2024-2025-n-r/)")
        bot.send_message(call.message.chat.id, text, parse_mode='Markdown')
        text = ("[Теми. 8 клас.](https://docs.google.com/document/d/102crJPqWe1Evx7FKHbdigw9V1b_xcCCIwprDNuxRtFc/edit?usp=sharing/)")
        bot.send_message(call.message.chat.id, text, parse_mode='Markdown')

    elif call.data == "Мовно-літературна. Конкурси":   
        bot.send_message(call.message.chat.id, f"{call.data}:")
        text = ("Конкурс ораторського мистецтва\n[«Заговори, щоб я тебе побачив»](https://viddilgum.wixsite.com/viddilgum/zagovori-shob-ya-tebe-pobachiv/)")
        bot.send_message(call.message.chat.id, text, parse_mode='Markdown')
        text = ("Конкурс літературно-мистецької та педагогічної медіатворчості\n[«Створи шедевр»](https://stvoryschedevr.wixsite.com/sajt/)")
        bot.send_message(call.message.chat.id, text, parse_mode='Markdown')
        text = ("Конкурс\n[«Я так бачу, чую, відчуваю»](https://viddilgum.wixsite.com/viddilgum/%D1%8F-%D1%82%D0%B0%D0%BA-%D0%B1%D0%B0%D1%87%D1%83-%D1%87%D1%83%D1%8E-%D0%B2%D1%96%D0%B4%D1%87%D1%83%D0%B2%D0%B0%D1%8E/)")
        bot.send_message(call.message.chat.id, text, parse_mode='Markdown')
        text = ("Фестиваль\n[«Тарас Шевченко: погляд крізь століття»](https://viddilgum.wixsite.com/viddilgum/%D1%82-%D1%88%D0%B5%D0%B2%D1%87%D0%B5%D0%BD%D0%BA%D0%BE-%D0%BF%D0%BE%D0%B3%D0%BB%D1%8F%D0%B4-%D0%BA%D1%80%D1%96%D0%B7%D1%8C-%D1%81%D1%82%D0%BE%D0%BB%D1%96%D1%82%D1%82%D1%8F/)")
        bot.send_message(call.message.chat.id, text, parse_mode='Markdown')
        text = ("Фестиваль етнічних та національних мов і культур\n[«Мови різні, душа одна»](https://viddilgum.wixsite.com/viddilgum/festival/)")
        bot.send_message(call.message.chat.id, text, parse_mode='Markdown')
        text = ("Конкурс з української мови імені [Петра Яцика»](https://mon.gov.ua/osvita-2/zagalna-serednya-osvita/olimpiadi-ta-konkursi/konkursi/uchnivski-konkursi-ta-turniri/mizhnarodniy-konkurs-z-ukrainskoi-movi-imeni-petra-yatsika/)")
        bot.send_message(call.message.chat.id, text, parse_mode='Markdown')
        text = ("Конкурс\n[«Репортер»](https://filter.mkip.gov.ua/reporter_/)")
        bot.send_message(call.message.chat.id, text, parse_mode='Markdown')
        text = ("Конкурс\n[«Ми любимо зарубіжну літературу»](https://svitfilologa.com.ua/uchnivskyi-konkurs-%C2%ABmi-lubimo-zarub%D1%96zhnu-l%D1%96teraturu-%E2%80%93-2024%C2%BB.html/)")
        bot.send_message(call.message.chat.id, text, parse_mode='Markdown')
        text = ("Конкурс\n[«Літературний всесвіт»](https://nniim.cdu.edu.ua/konkursy/literaturnyi-vsesvit-2024/)")
        bot.send_message(call.message.chat.id, text, parse_mode='Markdown')       
        text = ("Конкурс\n[«Я – журналіст!»](https://ij.ogo.ua/ya-zhurnalist/umovi-konkursu-ya-zhurnalist-2023-roku/)")
        bot.send_message(call.message.chat.id, text, parse_mode='Markdown')

    elif call.data == "Національно-патриотичне":
        bot.send_message(call.message.chat.id, f"{call.data}:")
        text = ("Сучасний україномовний контент, який може стати у нагоді як класному керівнику так і вчителю предметнику.\n"
                "https://vm.tiktok.com/ZMrsj27oa/\n\n"
                "https://vm.tiktok.com/ZMrsjSF1b/\n\n"
                "https://vm.tiktok.com/ZMrsjABnT/\n\n"
                "https://vm.tiktok.com/ZMrsj286E/\n\n"
                "https://vm.tiktok.com/ZMrsj5FhR/\n\n"
                "https://vm.tiktok.com/ZMrsjAyqL/\n\n"
                "https://vm.tiktok.com/ZMrsjjQoA/\n\n")
        bot.send_message(call.message.chat.id, text, parse_mode='Markdown')

    elif call.data == "Сертифікація":
        bot.send_message(call.message.chat.id, f"{call.data}:")
        text = ("Наказ [МОН](https://osvita.ua/legislation/Ser_osv/91137/)")
        bot.send_message(call.message.chat.id, text, parse_mode='Markdown')
        text = ("Сертифікація педагогічних працівників [на сайті УЦОЯО](https://testportal.gov.ua/sertifikaciya-pedagogichnix-pracivnikiv-testuvannya/)")
        bot.send_message(call.message.chat.id, text, parse_mode='Markdown')

    elif call.data == "AddLnks":
        text = ("Вибачте! Чат-бот все ще перебуває в активній розробці.\n"
                "[Прискорити процес!](https://forms.gle/KhorxMpJMGzXYbtQA/)")
        bot.send_message(call.message.chat.id, text, parse_mode='Markdown')

try:
    bot.polling(none_stop=True)
except Exception as Err:
    logging.error(f"При обращении к Telegram API возникла ошибка: {Err}")
    bot.stop_polling()
    exit(1)
    