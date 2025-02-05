import requests
import json
import pandas as pd

class Main:
    def __init__(self):
        self.open_ai_api_key = "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"  # Replace with your key
        self.bot_template = open("github_discussion_new/agent05.txt", "r").read()
        self.conversation_history = []

    def call_chat_gpt_api(self, link):
        url = 'https://api.openai.com/v1/chat/completions'
        headers = {
            'Authorization': 'Bearer ' + self.open_ai_api_key,
            'Content-Type': 'application/json',
        }
        payload = {
            'model': 'gpt-4',
            'messages': [{'role': 'system', 'content': self.bot_template.replace("LINK", link)}],
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=150)
        return response.json()

    def process_response(self, response):
        # Assuming the response contains issue, cause, solution, etc.
        return response['choices'][0]['message']['content']

    def process_csv(self, csv_path, output_csv_path):
        df = pd.read_csv(csv_path)
        output_df = pd.DataFrame(columns=['Links', 'Issue', 'Cause', 'Solution', 'Thematic Coding of issue', 'Thematic Coding of cause', 'Thematic Coding of solution', 'Sub-Categories for issue', 'Sub-Categories for cause', 'Sub-Categories for solution','Categories for issue', 'Categories for cause', 'Categories for solution' ])
        
        for link in df['Links']:
            response = self.call_chat_gpt_api(link)
            processed_content = self.process_response(response)

            # Convert processed_content to a DataFrame if it's not already one
            if not isinstance(processed_content, pd.DataFrame):
                # Assuming processed_content is a dictionary
                processed_content = pd.DataFrame([processed_content])

            # Use concat instead of append
            output_df = pd.concat([output_df, processed_content], ignore_index=True)

        output_df.to_csv(output_csv_path, index=False)

if __name__ == "__main__":
    agent = Main()
    input_csv = "C:/Users/ZRasheed/Desktop/Pekka Task/Waseem/github_discussion/datalink123.csv"
    output_csv = "C:/Users/ZRasheed/Desktop/Pekka Task/Waseem/github_discussion/datalink1234.csv"
    agent.process_csv(input_csv, output_csv)
