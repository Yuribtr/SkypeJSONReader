# Simple python script for parsing Skype chat history file in JSON format
Script will extract a chat conversation history between you and your interlocutor using specified login in chronological order with highlighting.

##Requirements:
1. JSON export file downloaded from https://go.skype.com/export.
2. Login name of your interlocutor.

##Instructions:
1. Please put decompressed file "messages.json" in script folder.
2. Run "main.py".
3. Enter login name of your interlocutor when prompted.
4. Result will be printed to the Python console.

##Notice:
- Please use login name instead of display name. Login name usually are unique and doesn't contain spaces.
- Usually Skype export file keeps conversation history for last 2 years.
- Additional info here: https://support.skype.com/en/faq/FA34894/how-do-i-export-my-skype-files-and-chat-history