from openai import OpenAI
import os
import textwrap
from ChatClasses.QAAssistant import QAAssistant

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
    print("\nResponse Content:\n")
    print("\n\n".join(wrapper.wrap(response_content)))

    print("\n" + "-"*80 + "\n")


def main(): 
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filePath = os.path.join(script_dir, 'Testing.py')
    fileContent : str = ReadFile(filePath)

    Assistant = QAAssistant()

    response = Assistant.EdgeCases(fileContent)
    
    print(response)

main()