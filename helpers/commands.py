import requests
import json
import os

BOT_TOKEN = os.environ.get('BOT_TOKEN')

telegram_api = 'https://api.telegram.org'
telegram_bot = f'bot{BOT_TOKEN}'

def get_commands():
    menu = [
        {
            'command': 'start',
            'description': 'Start the bot',
        },
        {
            'command': 'info',
            'description': 'Get the bot info',
        },
        {
            'command': 'os',
            'description': 'Control OS',
        },
        {
            'command': 'food',
            'description': 'Random food',
        },
        {
            'command': 'find',
            'description': 'Search with google',
        },
        {
            'command': 'finance',
            'description': 'Finance stock data',
        }
    ]
    return menu

def set_commands():
    response = requests.get('%s/%s/%s' % (telegram_api, telegram_bot, 'setMyCommands'),
        params={'commands': json.dumps(get_commands()),
    })

    content = json.loads(response.content)
    return content
