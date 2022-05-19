import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup

bot = telebot.TeleBot('5280932131:AAELkJM_n0-ndTQ-bvmrlCThjDsgcGdYG7A')


@bot.message_handler(commands=["start"])
def start(message, res=False):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Главное меню")
    btn2 = types.KeyboardButton("Помощь")
    markup.add(btn1, btn2)

    bot.send_message(chat_id,
                     text="Привет, {0.first_name}! Я ПайТон. Я могу помочь тебе с выбором книг для чтения.".format(
                         message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    chat_id = message.chat.id
    ms_text = message.text

    if ms_text == "Главное меню" or ms_text == "🔙" or ms_text == "Вернуться в главное меню":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Случайная книга")
        btn2 = types.KeyboardButton("Поиск по названию")
        btn3 = types.KeyboardButton("Поиск по автору")
        btn4 = types.KeyboardButton("Помощь")
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(chat_id, text="Вы в главном меню", reply_markup=markup)

    elif ms_text == "Случайная книга":
        bot.send_message(chat_id, get_book())

    elif ms_text == "Поиск по названию":
        bot.send_message(chat_id, 'Отправь мне название книги. Я попробую ее найти.')
        bot.register_next_step_handler(message, search_book)

    elif ms_text == "Поиск по автору":
        bot.send_message(chat_id, 'Отправь мне имя автора. Я попробую его найти.')
        bot.register_next_step_handler(message, search_author)

    elif ms_text == "/help" or ms_text == "Помощь":
        bot.send_message(chat_id, "Автор: Белоцерковец Алина")
        key1 = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text="Напиши автору", url="https://t.me/Litareae")
        key1.add(btn1)
        img = open('1MV4_Belotserkovets_Alina.jpg', 'rb')
        bot.send_photo(chat_id, img, reply_markup=key1)
    else:
        bot.send_message(chat_id, 'Не понимаю... Если хочешь что-нибудь найти, нажми соответствующую кнопку!')


def get_book():
    array_books = []
    req_book = requests.get('https://readly.ru/books/i_am_lucky/?show=1')
    soup = BeautifulSoup(req_book.content, "html.parser")
    result_find = soup.select("a > img")
    result_find2 = soup.select('.blvi__title, .blvi__book_info')
    for img in result_find:
        img_url = img.attrs.get("src")
    book_image = f"https://readly.ru/{img_url}"
    for result in result_find2:
        array_books.append(result.getText())
    return book_image + array_books[0] + array_books[1]


def search_author(message):
    chat_id = message.chat.id
    ms_text1 = message.text
    try:
        array_authors = []
        url = f"https://readly.ru/search/?q={ms_text1}"
        book_href = requests.get(url)
        soup = BeautifulSoup(book_href.content, "html.parser")
        for a in soup.select("figure > a"):
            array_authors.append(a.get('href'))
        searchQuery = array_authors[0]
        author_href = f"https://readly.ru/{searchQuery}"
        bot.send_message(chat_id, text="Похоже вы искали этого автора" + '\n' + author_href)
    except Exception:
        bot.send_message(chat_id, text="Такой автор не найден")


def search_book(message):
    chat_id = message.chat.id
    ms_text = message.text
    try:
        array_books = []
        url = f"https://readly.ru/search/?q={ms_text}"
        books_href = requests.get(url)
        soup = BeautifulSoup(books_href.content, "html.parser")
        for a in soup.select("figure > div > a", rel="nofollow"):
            array_books.append(a.get('href'))
        searchQuery = array_books[0]
        book_href = f"https://readly.ru/{searchQuery}"
        bot.send_message(chat_id, text="Похоже вы искали эту книгу" + '\n' + book_href)
    except Exception:
        bot.send_message(chat_id, text="Такая книга не найдена")


bot.polling(none_stop=True, interval=0)

print()
