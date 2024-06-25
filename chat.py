from abc import ABC
from openai import OpenAI
from loguru import logger


class Chat(ABC):
    def __init__(self, client: OpenAI, system_message: str = "You are a helpful assistant!", model: str = "gpt-3.5-turbo") -> None:
        self.client = client
        self.model = model
        self.total_tokens_used = 0
        self.messages = [
            {
                "role": "system",
                "content": system_message,
            }
        ]


    def make_request(self, promt: str) -> str:
        """ Makes a request to openai and returns the answer
        Args:
            promt (str): The promt to be sent.
        Returns:
            str: The response from openai.
        """
        # Add new message to history
        self.messages.append(
            {
                "role": "user",
                "content": promt
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

            # Save response to history
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


    def save_log(self) -> None:
        """ Appends the message history and the total tokens used to a log file. Creates the file if not exists.
        Args:
            None
        Returns:
            None
        """
        log_path = "log.txt"

        request_amount = int((len(self.messages) - 1) / 2)

        output_str = ""
        output_str += f"Chat between own_name '{self.own_name}' and partner_name '{self.partner_name}'\n"
        output_str += f"Used model: {self.model}\n"
        output_str += f"Amount of requests: {request_amount}\n"
        output_str += f"Total tokens used: {self.total_tokens_used}\n"

        with open(log_path, "w", encoding="utf-8") as file:
            file.write(output_str)
