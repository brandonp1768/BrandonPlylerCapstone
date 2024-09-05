from openai import OpenAI
import os
from dotenv import load_dotenv

class QAAssistant:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(QAAssistant, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            load_dotenv()
            self.client = OpenAI(api_key=os.getenv("OPEN_API_KEY"))
            # Think about how to add the creation of the chat here eventually
            self.initialized = True
    
    def FormatPrompt(fileContent : str):
        prompt = (
            "I have the following Python code: \n\n"
            f"{fileContent}\n\n"
            "What is this code doing?"
        )
        
        return prompt

    def CodeExplanation(self, fileContent : str):
        
        prompt = (
            "I have the following code: \n\n"
            f"{fileContent}\n\n"
            "Explain what this code is doing?"
        )

        response = self.chat = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a knowledgeable coding assistant"},
                    {"role": "user", "content": prompt}
                ]
            )
        
        stringResponse = response.choices[0].message.content.strip()

        print(f"\nTokens used: {response.usage.total_tokens}\n\n")

        return stringResponse
