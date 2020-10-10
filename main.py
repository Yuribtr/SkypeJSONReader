import json
import re
import html
from datetime import datetime


class PrintColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def strip_symbols(word: str):
    """
    Only for debugging purposes to clean special symbols.
    Not used in this script.
    """
    forbidden_chars = ('~`!@#$%^&*()+-*/_={}[]:;"\'<>?,.\|')
    return word.strip(forbidden_chars)


def get_message_types(filename):
    """
    Only for debugging purposes - which message types are presents in JSON export file.
    Not used in this script.
    """
    result = set()
    with open(filename, encoding='utf-8') as file:
        file = json.load(file)
        conversations = file['conversations']
        for conversation in conversations:
            for message in conversation['MessageList']:
                result.add(message['messagetype'])
    return result


def remove_prefixes(login: str):
    return re.sub("^[\d]+:", "", login)


def get_login_names(filename):
    """
    Only for debugging purposes - which login names are presents in JSON export file.
    Not used in this script.
    """
    result = set()
    with open(filename, encoding='utf-8') as file:
        file = json.load(file)
        conversations = file['conversations']
        for conversation in conversations:
            result.add(f'{remove_prefixes(conversation["id"])}'
                       f'{"" if conversation["displayName"] is None else " [" + conversation["displayName"] + "]"}'
                       f' - {len(conversation["MessageList"])}')
    return result


def get_dialog_by_name(filename, person: str):
    """
    Function will extract a conversation between your account and your interlocutor using specified login in
    chronological order with highlighting. Usually Skype export file keeps conversation history for last 2 years.

    :param filename: JSON export file downloaded from https://go.skype.com/export
    :param person:  Skype login of your interlocutor
    :param prefix:  magic prefix that appeared in JSON export files
    :return:    list of formatted conversations
    """
    result = ['Login name was not found!\n']
    last_msg_date = None
    with open(filename, 'r', encoding='utf-8') as file:
        file = json.load(file)
        items = file['conversations']
        for item in items:
            if remove_prefixes(item['id']) == person:
                result = []
                for message in item['MessageList']:
                    if not message['messagetype'] in ['RichText', 'Text']:
                        continue
                    msg_date = datetime.fromtimestamp(int(message['id']) / 1000).strftime('%Y-%m-%d')
                    if last_msg_date != msg_date:
                        result += [f'\n---{last_msg_date}---']
                        last_msg_date = msg_date
                    if message['from'] == person:
                        result += [f'{PrintColors.OKGREEN}↓  '
                                   f'{html.unescape(re.sub("<[^<]+?>", "", message["content"]))}{PrintColors.ENDC}']
                    else:
                        result += [f'{PrintColors.OKBLUE}↑  '
                                   f'{html.unescape(re.sub("<[^<]+?>", "", message["content"]))}{PrintColors.ENDC}']
                result += [f'\n---{last_msg_date}---']
                result.reverse()
                result = result[:-1]
                break
    return result


while True:
    print('\n1. Get chat history by login\n2. List all logins')
    choice = input('Pls select your choice or print "q", and hit "Enter": ')
    if choice == '1':
        person = input('Please enter Skype login to get conversation list: ')
        print(*get_dialog_by_name('messages.json', person=person), sep='\n')
    if choice == '2':
        print(*get_login_names('messages.json'), sep='\n')
    if choice == 'q':
        break
