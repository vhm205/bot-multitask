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
            'command': 'stock',
            'description': 'Finance stock data',
        },
        {
            'command': 'food',
            'description': 'Random food',
        },
        {
            'command': 'search',
            'description': 'Search with google',
        },
        {
            'command': 'os',
            'description': 'Control OS',
        },
    ]
    return menu

def set_commands():
    response = requests.get('%s/%s/%s' % (telegram_api, telegram_bot, 'setMyCommands'),
        params={'commands': json.dumps(get_commands()),
    })

    content = json.loads(response.content)
    return content
