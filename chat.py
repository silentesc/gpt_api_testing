import os
import json
from loguru import logger
from openai import OpenAI


class Chat:
    def __init__(self, client: OpenAI, own_name: str, partner_name: str, model: str = "gpt-3.5-turbo") -> None:
        self.client = client
        self.model = model
        self.own_name = own_name
        self.partner_name = partner_name
        self.total_tokens_used = 0
        self.messages = [
            {
                "role": "system",
                "content": f"Du heißt {own_name} und hast eine romantische Beziehung zu {partner_name}.",
            }
        ]
    
    def send_message(self, message: str) -> str:
        """ Sends a message to the partner
        Args:
            message (str): The message to be sent to the partner.
        
        Returns:
            str: The response from the partner.
        """
        # Add new message to history
        self.messages.append(
            {
                "role": "user",
                "content": message
            }
        )

        try:
            # Make request
            chat_completion = self.client.chat.completions.create(
                messages = self.messages,
                model = self.model,
            )
            self.total_tokens_used += chat_completion.usage.total_tokens
            response = chat_completion.choices[0].message.content

            # Save response to chat
            self.messages.append(
                {
                    "role": "assistant",
                    "content": response
                }
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            logger.error("Request to openai failed due to:\n" + str(e))
            return "An error has been occured while making an openai request!"

    # TODO The log is not valid json, please don't use it for automated things
    def save_log(self) -> None:
        """ Appends the message history and the total tokens used to a json file. Creates the file if not exists.
        Args:
            None

        Returns:
            None
        """
        log_path = "log.json"

        # Create file if not exists
        if not os.path.exists(log_path):
            with open(log_path, "w", encoding="utf-8") as file:
                file.write("")
        
        # Append log file with new data
        with open(log_path, "a", encoding="utf-8") as file:
            if not file.writable():
                logger.error("Logging file is not writable!")
                return
            
            log_dict = {
                "messages": self.messages,
                "total_tokens_used": self.total_tokens_used
            }
            file.write(json.dumps(log_dict, ensure_ascii=False) + "\n")
