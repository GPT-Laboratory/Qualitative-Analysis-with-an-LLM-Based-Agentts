import requests
import json
import pandas as pd

class Main:
    def __init__(self):
        self.open_ai_api_key = "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"  # Replace with your key
        self.bot_1 = open("github_discussion_new/agent05.txt", "r").read()

        self.conversation_history_bot_1 = []
        #self.conversation_history_bot_2 = []
        #self.conversation_history_bot_3 = []
        #self.conversation_history_bot_4 = []

    def call_chat_gpt_api(self, conversation_history):
        url = 'https://api.openai.com/v1/chat/completions'
        headers = {
            'Authorization': 'Bearer ' + self.open_ai_api_key,
            'Content-Type': 'application/json',
        }
        payload = {
            'model': 'gpt-4',
            'messages': conversation_history,
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=150)
        return response.json()

    def process_response(self, response):
        if isinstance(response, str) and response.startswith("FALLBACK"):
            return response, response
        elif response['choices'][0]['message']['content']:
            return response['choices'][0]['message']['content'], response['choices'][0]['message']['content']
        elif response['choices'][0]['message']['function_call']:
            return response['choices'][0]['message']['function_call'], response['choices'][0]['message']['function_call']

    def process_csv(self, csv_path):
        df = pd.read_csv(csv_path)
        print("Columns in CSV:", df.columns)
        for index, row in df.iterrows():
            issue, cause, solution = row['issue'], row['cause'], row['solution']
            self.project_description = f"Issue: {issue}. Cause: {cause}. Solution: {solution}."
            
            # Re-initialize the conversation histories
            self.conversation_history_bot_1 = [{'role': 'system', 'content': self.bot_1.replace("PROJECT_DESCRIPTION", self.project_description)}]
            #self.conversation_history_bot_2 = [{'role': 'system', 'content': self.bot_2.replace("PROJECT_DESCRIPTION", self.project_description)}]
            #self.conversation_history_bot_3 = [{'role': 'system', 'content': self.bot_3.replace("PROJECT_DESCRIPTION", self.project_description)}]
            #self.conversation_history_bot_4 = [{'role': 'system', 'content': self.bot_4.replace("PROJECT_DESCRIPTION", self.project_description)}]

            self.run()

    def run(self):
            for bot_history in [self.conversation_history_bot_1]:
                               # self.conversation_history_bot_2, 
                                #self.conversation_history_bot_3, 
                                #self.conversation_history_bot_4]:
                
                response = self.call_chat_gpt_api(bot_history)
                assistant_response, _ = self.process_response(response)
                print(assistant_response)
                
                # Add the response to all bot histories
                for history in [self.conversation_history_bot_1]:
                                #self.conversation_history_bot_2, 
                                #self.conversation_history_bot_3, 
                                #self.conversation_history_bot_4]:
                    history.append({'role': 'user', 'content': assistant_response})

if __name__ == "__main__":
    agent = Main()
    agent.process_csv("C:/Users/ZRasheed/Desktop/Pekka Task/Waseem/github_discussion/Dataextractioncsv.csv")