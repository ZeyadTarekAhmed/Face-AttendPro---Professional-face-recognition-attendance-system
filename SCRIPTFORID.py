import requests
import json

bot_token = '7814258804:AAHiHBFbBPiYhEGHU3JigdpA3ezyd6yokdI'  # Replace with your bot's token
url = f"https://api.telegram.org/bot{bot_token}/getUpdates"

# Function to get chat ID from the latest message
def get_chat_id():
    response = requests.get(url)
    updates = response.json()

    # Check if we have any updates (messages) in the chat
    if 'result' in updates and len(updates['result']) > 0:
        # Get the last message sent to the bot
        last_message = updates['result'][-1]
        chat_id = last_message['message']['chat']['id']
        first_name = last_message['message']['from']['first_name']
        print(f"Chat ID: {chat_id} | Student Name: {first_name}")
        return chat_id

# Call the function to capture chat ID
get_chat_id()
