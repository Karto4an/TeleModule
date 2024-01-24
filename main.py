import os
import json
import dotenv
import telebot

dotenv.load_dotenv()
bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))

# Open scheme.json file and load it into a dictionary
with open('scheme.json', 'r', encoding='utf-8') as f:
    scheme = json.load(f)


# Dynamically register handler for a command from json file
# Json file uses the following format:
# {'commands': [{'name': 'start', 'description': 'Start command', 'aliases': ['start'], 'action': 'start_message_action'}], 'actions': [{'name': 'start_message_action', 'description': 'Start message action', 'proccess': {'type': 'message', 'message': 'Hello, {{username}}!'}}]}


def register_handlers():
    for command in scheme['commands']:
        @bot.message_handler(commands=command['aliases'])
        def handler(message):
            action = command['action']
            for action in scheme['actions']:
                if action['name'] == command['action']:
                    if action['proccess']['type'] == 'message':
                        bot.send_message(message.chat.id, action['proccess']['message'].replace('{{username}}', message.from_user.username))


register_handlers()
bot.polling()
