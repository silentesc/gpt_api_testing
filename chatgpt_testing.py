import json
from openai import OpenAI

from chat import Chat


SECRETS = json.load(open("secrets.json"))
client = OpenAI(api_key = SECRETS.get("TOKEN"))

chat = Chat(client=client, own_name="Bottoni", partner_name="Bottina")

chat.send_message("Wie gehts dir?")
chat.send_message("Wie viele Äpfel hat ein Baum ohne Äpfel?")

chat.save_log()
