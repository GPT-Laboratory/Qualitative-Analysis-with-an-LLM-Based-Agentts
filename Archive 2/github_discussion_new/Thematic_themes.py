import requests
import json
class main:
    def __init__(self,project_description):
        self.open_ai_api_key = "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"
        self.bot_1 = open("github_discussion_new/T-themes.txt", "r").read()

        
        self.project_descrption = f"Identify themes from {project_description}" # WRITE ANY PROJECT DESCRIPTION HERE
        self.bot_1 = self.bot_1.replace("PROJECT_DESCRIPTION", self.project_descrption)

        self.conversation_history_bot_1 = []
        self.conversation_history_bot_1.append({'role': 'system', 'content': self.bot_1})

    
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