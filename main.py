"""
This module is responsible for managing bot's core functionality.
"""

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


def get_action(action_name):
    """
    Retrieve the action associated with a command from the scheme dictionary.
    """
    for action in scheme['actions']:
        if action['name'] == action_name:
            return action
    return None

def replace_placeholders(message_content, placeholders):
    """
    Replace placeholders in the message content with their corresponding values.
    """
    for placeholder, value in placeholders.items():
        message_content = message_content.replace(placeholder, value)
    return message_content

def process_message(action, message):
    """
    Process the message based on the action's content.
    """
    if action['proccess']['type'] == 'message':
        message_content = action['proccess']['message']
        placeholders = {
            '{{username}}': message.from_user.username,
            # Add more placeholders and their corresponding values here
        }
        response_message = replace_placeholders(message_content, placeholders)
        bot.send_message(message.chat.id, response_message)

def register_handler(command):
    """
    Register a handler for a specific command.
    """
    command_aliases = command['aliases']
    command_action = command['action']

    @bot.message_handler(commands=command_aliases)
    def handler(message):
        action = get_action(command_action)
        if action:
            process_message(action, message)

def register_handlers():
    """
    Register handlers for commands defined in the scheme dictionary.
    """
    for command in scheme['commands']:
        register_handler(command)

register_handlers()
bot.polling()
