from openai import OpenAI
import os
from dotenv import load_dotenv

class QAAssistant:  # Feed data with the system role in the prompt, for conversations cache the responses in a list and feed it in through the system role
    _instance = None # Think about putting code through the system role instead of a prompt

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(QAAssistant, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            load_dotenv()
            self.client = OpenAI(api_key=os.getenv("OPEN_API_KEY"))
            # Think about how to add the creation of the chat here eventually so we can send messages to the chat instead of making a new chat each time (or putting previous answers back into each answer)
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
    
    def TestingCases(self, fileContent : str):
        prompt = (
            "I have the following code: \n\n"
            f"{fileContent}\n\n"
            "List me off some testing cases for this program, list only the test cases"
        )

        response = self.chat = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a knowledgeable coding quality assurance test case generator"},
                    {"role": "user", "content": prompt}
                ]
            )
        
        stringResponse = response.choices[0].message.content.strip()

        print(f"\nTokens used: {response.usage.total_tokens}\n\n")

        test_cases = stringResponse.splitlines()

        html_response = "<ul>"

        for case in test_cases:
            html_response += f"<li>{case}<li>"
        html_response += "<ul>"

        return html_response

    def FailingCases(self, fileContent : str):
        prompt = (
            "I have the following code: \n\n"
            f"{fileContent}\n\n"
            "Give me cases where this program is going to fail"
        )

        response = self.chat = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a knowledgeable coding quality assurance assistant"},
                    {"role": "user", "content": prompt}
                ]
            )
        
        stringResponse = response.choices[0].message.content.strip()

        print(f"\nTokens used: {response.usage.total_tokens}\n\n")

        return stringResponse
    
    def EdgeCases(self, fileContent : str):
        prompt = (
            "I have the following code: \n\n"
            f"{fileContent}\n\n"
            "Give me the edge cases for this program"
        )

        response = self.chat = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a knowledgeable coding quality assurance assistant"},
                    {"role": "user", "content": prompt}
                ]
            )
        
        stringResponse = response.choices[0].message.content.strip()

        print(f"\nTokens used: {response.usage.total_tokens}\n\n")

        return stringResponse
    
    def Testing(self : str, message : str, cache : list = None):
        conversation = [
            "Alice: Hey, Bob! How’s it going?",
            "Bob: Hi Alice! I’m doing well, thanks. How about you?",
            "Alice: I’m good too. Got any plans for the weekend?",
            "Bob: Actually, yes. I’m thinking of going hiking. How about you?",
            "Alice: That sounds fun! I’m planning to visit a museum.",
            "Bob: Nice! Which museum are you thinking of?",
            "Alice: The art museum downtown. I’ve heard they have a new exhibition.",
            "Bob: That’s exciting! What’s the exhibition about?",
            "Alice: It’s a collection of modern art. I’m really looking forward to it.",
            "Bob: Sounds interesting. I’ve always enjoyed modern art.",
            "Alice: Me too! It’s so vibrant and expressive.",
            "Bob: Absolutely. Do you like hiking as well?",
            "Alice: I do, but I haven’t been in a while. I should try to get back into it.",
            "Bob: You should! It’s a great way to unwind and enjoy nature.",
            "Alice: I agree. Maybe I’ll join you next time.",
            "Bob: That would be awesome! We could plan a hike together.",
            "Alice: Definitely. Let’s make it happen.",
            "Bob: Perfect! I’ll look up some good trails for us.",
            "Alice: Great. I’ll check out the museum’s schedule for their tours.",
            "Bob: Sounds like a plan. Have a great time at the museum!",
            "Alice: Thanks, Bob! Enjoy your hike and stay safe."
        ]

        prompt = (
            f"{message}"
        )

        response = self.chat = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"{conversation}"},
                    {"role": "system", "content": f"Your Previous response: \n\n{cache}"},
                    {"role": "user", "content": prompt}
                ]
            )
        
        stringResponse = response.choices[0].message.content.strip()

        print(f"\nTokens used: {response.usage.total_tokens}\n\n")

        return stringResponse
