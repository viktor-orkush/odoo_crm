import pickle
import telebot
import config


bot = telebot.TeleBot(config.TOKEN)


def save_chat_info(chat_id):
    chats_id = get_all_chats_id()
    if chat_id not in chats_id:
        chats_id.append(chat_id)
        with open('chat_info.pkl', 'wb+') as file:
            pickle.dump(chats_id, file)


def get_all_chats_id():
    with open('chat_info.pkl', 'rb') as file:
        try:
            chats_id = pickle.load(file)
        except EOFError:
            chats_id = []
    return list(chats_id)


@bot.message_handler(commands=['start', 'help'])
def start(message):
    save_chat_info(message.chat.id)
    bot.send_message(message.chat.id, "Этот бот служит для уведомления о завершении сделки, сюда будут приходить "
                                      "уведомления об успешно завершенных сделках с ее название и датой")


@bot.message_handler(content_types=['text'])
def send_text(message):
        bot.send_message(message.chat.id, "")


def send_message(message):
    chats_id = get_all_chats_id()
    for item in chats_id:
        bot.send_message(chat_id=item, text=message)


if __name__ == "__main__":
    bot.polling()
