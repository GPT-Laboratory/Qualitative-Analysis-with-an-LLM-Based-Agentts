import tkinter as tk
from tkinter import simpledialog, messagebox
import requests
import json

# GUI functions
def get_user_input():
    root = tk.Tk()
    root.withdraw()
    user_input = simpledialog.askstring(title="PekkaGPT", prompt="Please enter your message:")
    return user_input

def display_output(output):
    messagebox.showinfo("Response", output)

class main:
    def __init__(self,project_description):
        self.open_ai_api_key = "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"
        self.bot_1 = open("github_discussion_new/agent_001.txt", "r").read()
        self.bot_2 = open("github_discussion_new/agent_002.txt", "r").read()
        self.bot_3 = open("github_discussion_new/agent_003.txt", "r").read()
        self.bot_4 = open("github_discussion_new/agent_004.txt", "r").read()
        
        self.project_descrption = get_user_input()
        if not self.project_descrption:
            exit()

        self.bot_1 = self.bot_1.replace("PROJECT_DESCRIPTION", self.project_descrption)
        self.bot_2 = self.bot_2.replace("PROJECT_DESCRIPTION", self.project_descrption)
        self.bot_3 = self.bot_3.replace("PROJECT_DESCRIPTION", self.project_descrption)
        self.bot_4 = self.bot_4.replace("PROJECT_DESCRIPTION", self.project_descrption)

        self.conversation_history_bot_1 = [{'role': 'system', 'content': self.bot_1}]
        self.conversation_history_bot_2 = [{'role': 'system', 'content': self.bot_2}]
        self.conversation_history_bot_3 = [{'role': 'system', 'content': self.bot_3}]
        self.conversation_history_bot_4 = [{'role': 'system', 'content': self.bot_4}]

    def call_chat_gpt_api(self, conversation_history):
        url = 'https://api.openai.com/v1/chat/completions'
        headers = {
            'Authorization': 'Bearer ' + self.open_ai_api_key,
            'Content-Type': 'application/json',
        }

        payload = {
            'model': 'gpt-3.5-turbo-16k',
            'messages': conversation_history,
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=150)

        return response.json()

    def process_response(self, response):
        if isinstance(response, str) and response.startswith("FALLBACK"):
            assistant_response = response
        elif response['choices'][0]['message']['content']:
            assistant_response = response['choices'][0]['message']['content']
        elif response['choices'][0]['message']['function_call']:
            assistant_response = response['choices'][0]['message']['function_call']
        else:
            assistant_response = "Unknown response"
        
        return assistant_response

    def run(self,):
        total_rounds = 0
        final_response = ""

        while total_rounds != 1:
            for conversation_history in [self.conversation_history_bot_1, self.conversation_history_bot_2, self.conversation_history_bot_3, self.conversation_history_bot_4]:
                response = self.call_chat_gpt_api(conversation_history)
                assistant_response = self.process_response(response)
                final_response += "Bot {}: {}\n".format(total_rounds + 1, assistant_response)
                conversation_history.append({'role': 'user', 'content': assistant_response})

            total_rounds += 1

        display_output(final_response)

if __name__ == "__main__":
    main().run()
