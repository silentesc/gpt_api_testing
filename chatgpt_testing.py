import json
from openai import OpenAI

from romantic_chat import RomanticChat


SECRETS = json.load(open("secrets.json"))
client = OpenAI(api_key = SECRETS.get("TOKEN"))

chat = RomanticChat(client=client, own_name="Bottoni", partner_name="Bottina")

print(chat.make_request("Hallo, wie gehts?"))
