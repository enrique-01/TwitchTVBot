from config import NAME
from re import search
import chatscrub
import config

PREFIX = "@deeplearningbot69"

def process(bot, user, message):
    if message.startswith(PREFIX):
        respond_to_user(bot, user, message)

def respond_to_user(bot, user, message):
    bot.send_message({user['name']} + chatscrub.return_message(message))

