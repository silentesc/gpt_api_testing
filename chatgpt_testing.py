import json
from openai import OpenAI

from chat import RomanticChat


SECRETS = json.load(open("secrets.json"))
client = OpenAI(api_key = SECRETS.get("TOKEN"))

chat = RomanticChat(client=client, own_name="Bottoni", partner_name="Bottina")
