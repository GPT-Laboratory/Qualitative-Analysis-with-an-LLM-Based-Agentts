import requests
import json
class main:
    def __init__(self,project_description):
        self.open_ai_api_key = "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"
        self.bot_1 = open("github_discussion_new/agent_001.txt", "r").read()
        self.bot_2 = open("github_discussion_new/agent_002.txt", "r").read()
        self.bot_3 = open("github_discussion_new/agent_003.txt", "r").read()
        self.bot_4 = open("github_discussion_new/agent_004.txt", "r").read()
        
        self.project_descrption = f"Identify issue, cause and their solution from {project_description}" # WRITE ANY PROJECT DESCRIPTION HERE
        self.bot_1 = self.bot_1.replace("PROJECT_DESCRIPTION", self.project_descrption)
        self.bot_2 = self.bot_2.replace("PROJECT_DESCRIPTION", self.project_descrption)
        self.bot_3 = self.bot_3.replace("PROJECT_DESCRIPTION", self.project_descrption)
        self.bot_4 = self.bot_4.replace("PROJECT_DESCRIPTION", self.project_descrption)
        self.conversation_history_bot_1 = []
        self.conversation_history_bot_1.append({'role': 'system', 'content': self.bot_1})
        self.conversation_history_bot_2 = []
        self.conversation_history_bot_2.append({'role': 'system', 'content': self.bot_2})
        self.conversation_history_bot_3 = []
        self.conversation_history_bot_3.append({'role': 'system', 'content': self.bot_3})
        self.conversation_history_bot_4 = []
        self.conversation_history_bot_4.append({'role': 'system', 'content': self.bot_4})
    
    def call_chat_gpt_api(self, conversation_history, openai_api_key):
        url = 'https://api.openai.com/v1/chat/completions'
        headers = {
            'Authorization': 'Bearer ' + openai_api_key,
            'Content-Type': 'application/json',
        }

        payload = {
            'model': 'gpt-3.5-turbo-16k',
            'messages': conversation_history,
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=200)

        return response.json()


    def process_response(self, response):
        if isinstance(response, str) and response.startswith("FALLBACK"):
            assistant_response = response
            previousResponse = assistant_response
        elif response['choices'][0]['message']['content']:
            assistant_response = response['choices'][0]['message']['content']
            previousResponse = assistant_response
        elif response['choices'][0]['message']['function_call']:
            assistant_response = response['choices'][0]['message']['function_call']
            previousResponse = assistant_response

        return assistant_response, previousResponse
    
    def run(self,):

            
        response = self.call_chat_gpt_api(self.conversation_history_bot_1, self.open_ai_api_key)
        assistant_response, self.previous_response = self.process_response(response)
        return assistant_response
        
    
if __name__ == "__main__":
    main().run()