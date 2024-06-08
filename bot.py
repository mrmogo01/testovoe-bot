import telebot
import logging
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Настройка логгера
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = '6327645099:AAGLZhWPySd_AwPf5KO5CUmr_i4HGZuOveE'
bot = telebot.TeleBot(BOT_TOKEN)

@bot.chat_join_request_handler()
def handle_join_request(chat_join_request):
    chat_id = chat_join_request.chat.id
    user_id = chat_join_request.from_user.id

    markup = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text="Присоединиться к каналу", callback_data=f"approve_{chat_id}_{user_id}")
    markup.add(button)

    bot.send_message(user_id, "Нажми на кнопку ниже, чтобы подтвердить запрос на вступление в канал.", reply_markup=markup)

    # Логирование
    logger.info(f"Join request received from user {user_id} in chat {chat_id}.")

@bot.callback_query_handler(func=lambda call: call.data.startswith('approve_'))
def handle_approval_callback(call):
    _, chat_id, user_id = call.data.split('_')
    chat_id = int(chat_id)
    user_id = int(user_id)

    bot.approve_chat_join_request(chat_id, user_id)
    bot.send_message(user_id, "Твой запрос на вступление в канал одобрен! Добро пожаловать.")
    bot.answer_callback_query(call.id)

    # Логирование
    logger.info(f"Join request approved for user {user_id} in chat {chat_id}.")

bot.polling()
