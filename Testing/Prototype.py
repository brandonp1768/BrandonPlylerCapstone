from openai import OpenAI
import os
from dotenv import load_dotenv
import textwrap

load_dotenv()

def ReadFile(filePath : str):
    with open(filePath, 'r') as file:
        return file.read()

def FormatPrompt(fileContent : str):
    prompt = (
        "I have the following Python code: \n\n"
        f"{fileContent}\n\n"
        "What is this code doing?"
    )
    
    return prompt

'''
Strictly just a formatter for the terminal
'''
def PrintResponse(response_content: str):
    wrapper = textwrap.TextWrapper(width=80)  
    print("\nResponse Content:")
    print("\n".join(wrapper.wrap(response_content)))

    print("\n" + "-"*80 + "\n")


def main(): 
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    script_dir = os.path.dirname(os.path.abspath(__file__))
    filePath = os.path.join(script_dir, 'Testing.py')

    fileContent : str = ReadFile(filePath)

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a knowledgeable coding assistant",
            },
            {
                "role": "user",
                "content": FormatPrompt(fileContent)
            }
        ],
    ) 

    PrintResponse(response.choices[0].message.content.strip())

    totalTokens = response.usage.total_tokens
    print(f"\nTokens used: {totalTokens}")

main()