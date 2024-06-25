from loguru import logger
from openai import OpenAI

from chat import Chat


class RomanticChat(Chat):
    def __init__(self, client: OpenAI, own_name: str, partner_name: str, model: str = "gpt-3.5-turbo") -> None:
        super().__init__(client=client, system_message=f"Du heißt {own_name} und hast eine romantische Beziehung zu {partner_name}.", model=model)
        self.own_name = own_name
        self.partner_name = partner_name
        self.total_tokens_used = 0
