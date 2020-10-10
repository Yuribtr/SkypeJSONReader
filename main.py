import json
import re
from time import perf_counter
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
    with open(filename, encoding='utf-8') as file:
        file = json.load(file)
        items = file['conversations']
        text = set()
        for item in items:
            for message in item['MessageList']:
                text.add(message['messagetype'])
    return text


def get_dialog_by_name(filename, person: str, prefix='8:'):
    """
    Function will extract a conversation between your account and your interlocutor using specified login in
    chronological order with highlighting. Usually Skype export file keeps conversation history for last 2 years.

    :param filename: JSON export file downloaded from https://go.skype.com/export
    :param person:  Skype login of your interlocutor
    :param prefix:  magic prefix that appeared in JSON export files
    :return:    list of formatted conversations
    """
    result = ['Login name was not found!\n']
    person = prefix + person
    last_msg_date = None
    with open(filename, 'r', encoding='utf-8') as file:
        file = json.load(file)
        items = file['conversations']
        for item in items:
            if item['id'] == person:
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
    person = input('Please enter Skype login to get conversation list: ')
    if person != '':
        break
start_time = perf_counter()
print(*get_dialog_by_name('messages.json', person=person), sep='\n')
end_time = perf_counter()
print(f"Time taken: {(end_time - start_time) * 1000000} mkS")
