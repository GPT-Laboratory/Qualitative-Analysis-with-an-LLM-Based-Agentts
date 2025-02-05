from flask import Flask, request, send_file, jsonify, render_template
import os
from flask_socketio import SocketIO
import speech_recognition as sr
from pydub import AudioSegment
from github_discussion_new.Content_pattern import main as content_pattern
from github_discussion_new.Content_themes import main as content_themes
from github_discussion_new.Ground_Theory import main as ground_theory
from github_discussion_new.Discourse_themes import main as discourse_themes
from github_discussion_new.Discourse_pattern import main as discourse_pattern
from github_discussion_new.Narrative_analysis import main as narrative_analysis
from github_discussion_new.Thematic_cause import main as thematic_cause
from github_discussion_new.Thematic_issue import main as thematic_issue
from github_discussion_new.Thematic_solution import main as thematic_solution
from github_discussion_new.Thematic_pattern import main as thematic_pattern
from github_discussion_new.Thematic_themes import main as thematic_themes
import pandas as pd
import json
import requests

app = Flask(__name__)
socketio = SocketIO(app)
# Assuming CSV files will be stored in a directory named 'csv_files'
CSV_FOLDER = ''

@app.route('/')
def index():
    # Render a template that includes the UI elements you described
    return render_template('index.html')

@app.route('/submit_links', methods=['POST'])
def submit_links():
    # Extract links from the request
    links = request.form.get('links')
    options_list = request.form.getlist("selectedButtonsLinks[]")
    chatGPT_input = request.form.get('chatGPT')
    # Placeholder: Process the links and generate a CSV file
    # (You would replace this with a call to your API or processing function)
    csv_filename = process_links_and_generate_csv(links, options_list, chatGPT_input)

    # Return the name of the generated CSV file
    return jsonify({'csv_filename': csv_filename})

@app.route('/download_csv/<filename>', methods=['GET'])
def download_csv(filename):
    # Send the CSV file to the user
    return send_file(os.path.join(CSV_FOLDER, filename), as_attachment=True)

@app.route('/submit_prompt', methods=['POST'])
def submit_prompt():
    # Extract prompt from the request
    prompt = request.form.get('prompt')
    options_list = request.form.getlist("selectedButtonsPrompts[]")
    chatGPT_input = request.form.get('chatGPT')
    chatgpt_response = process_prompt_and_get_chatgpt_response(prompt, options_list, chatGPT_input)
    # Return the response from ChatGPT
    return jsonify({'response': chatgpt_response})


def call_chat_gpt_api( conversation_history):
    url = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Authorization': 'Bearer ' +  "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",
        'Content-Type': 'application/json',
    }

    payload = {
        'model': 'gpt-3.5-turbo-16k',
        'messages': conversation_history,
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=150)

    return response.json()


def process_prompt_and_get_chatgpt_response(project, selected_options, chatGPT_input):
    if selected_options: 
        main_option = selected_options[0]

    chatGPT_response = ""

    if chatGPT_input != "":
        user_input = {"role":"user", "content": f"here's a project description: {project} and here's a what you need to do f{main_option} f{chatGPT_input}"}
        system_message ={ "role": "system" ,"content":"You will be provided with project description and then queries like provide thematic coding or thematic solutions and so on. please return the output in a systematic way for example Response: \n Identified cause: \nThematic coding for identified cause: \n Sub category for thematic coding of identified cause: \nCategory for sub category of identified cause:"}
        conversation_history = [ system_message, user_input]
        response = call_chat_gpt_api(conversation_history)
        chatGPT_response = response['choices'][0]['message']['content']
    else:
        for option in selected_options[1:]:
            if main_option == "Thematic" and option == "Cause":
                chatGPT_response += "\n"+ thematic_cause(project).run()
            elif main_option == "Thematic" and option == "Issue":
                chatGPT_response += "\n"+ thematic_issue(project).run()
            elif main_option == "Thematic" and option == "Solution":
                chatGPT_response += "\n"+ thematic_solution(project).run()
            elif main_option == "Thematic" and option == "Pattern":
                chatGPT_response += "\n"+ thematic_pattern(project).run()
            elif main_option == "Thematic" and option == "Themes":
                chatGPT_response += "\n"+ thematic_themes(project).run()
            elif main_option == "Content" and option == "Pattern":
                chatGPT_response += "\n"+ content_pattern(project).run()
            elif main_option == "Content" and option == "Themes":
                chatGPT_response += "\n"+ content_themes(project).run()
            elif main_option == "Ground" and option == "Theory":
                chatGPT_response += "\n"+ ground_theory(project).run()
            elif main_option == "Discourse" and option == "Themes":
                chatGPT_response += "\n"+ discourse_themes(project).run()
            elif main_option == "Discourse" and option == "Pattern":
                chatGPT_response += "\n"+ discourse_pattern(project).run()
            elif main_option == "Narrative" and option == "Analysis":
                chatGPT_response += "\n"+ narrative_analysis(project).run()
            chatGPT_response += "\n\n---------------------------------------------------------------------------------------------------"
        
    
    return chatGPT_response


def process_links_and_generate_csv(links, selected_options, chatGPT_input):
    links = links.split(",")
    if selected_options:
        main_option = selected_options[0]

    if chatGPT_input != "":
        responses = {}
        for link in links:
            user_input = {"role":"user", "content": f"here's a link: {link} and here's a what you need to do {main_option} {chatGPT_input}"}
            system_message ={ "role": "system" ,"content":"You will be provided with github discussions link and then queries like provide thematic coding or thematic solutions and so on. please return the output in a systematic way for example Response: \n Identified cause: \nThematic coding for identified cause: \n Sub category for thematic coding of identified cause: \nCategory for sub category of identified cause:"}
            conversation_history = [ system_message, user_input]
            response = call_chat_gpt_api(conversation_history)
            chatGPT_response = response['choices'][0]['message']['content']
            responses[link] = chatGPT_response

        # Save the results to a CSV file
        csv_filename = 'results.csv'
        results_df = pd.DataFrame.from_dict(responses, orient='index', columns=['Response'])
        results_df.to_csv(os.path.join(CSV_FOLDER, csv_filename), index=True)
        return csv_filename
    else:

        columns = ['Link'] + selected_options[1:]
        results_df = pd.DataFrame(columns=columns)


        for link in links:
            # Initialize a dictionary to hold the results for this link
            link_result = {'Link': link}
            for option in selected_options[1:]:
                if main_option == "Thematic" and option == "Cause":
                    link_result[option] = thematic_cause(link).run()
                elif main_option == "Thematic" and option == "Issue":
                    link_result[option] = thematic_issue(link).run()
                elif main_option == "Thematic" and option == "Solution":
                    link_result[option] = thematic_solution(link).run()
                elif main_option == "Thematic" and option == "Pattern":
                    link_result[option] = thematic_pattern(link).run()
                elif main_option == "Thematic" and option == "Themes":
                    link_result[option] = thematic_themes(link).run()
                elif main_option == "Content" and option == "Pattern":
                    link_result[option] = content_pattern(link).run()
                elif main_option == "Content" and option == "Themes":
                    link_result[option] = content_themes(link).run()
                elif main_option == "Ground" and option == "Theory":
                    link_result[option] = ground_theory(link).run()
                elif main_option == "Discourse" and option == "Themes":
                    link_result[option] = discourse_themes(link).run()
                elif main_option == "Discourse" and option == "Pattern":
                    link_result[option] = discourse_pattern(link).run()
                elif main_option == "Narrative" and option == "Analysis":
                    link_result[option] = narrative_analysis(link).run()
            
            results_df = pd.concat([results_df, pd.DataFrame(link_result, index=[0])], ignore_index=True)

        # Save the results to a CSV file
        csv_filename = 'results.csv'
        results_df.to_csv(os.path.join(CSV_FOLDER, csv_filename), index=False)

        return csv_filename

# @socketio.on('audio_chunk')
# def handle_audio_chunk(data):
#     # Assuming data is a blob of audio in WAV format
#     print(data[:10]) 
#     audio_blob = bytes(data)  # Convert list of integers back to bytes
#     audio_stream = BytesIO(audio_blob)
#     audio_segment = AudioSegment.from_file(audio_stream, format="wav")
    
#     # Convert to a format suitable for speech_recognition library
#     audio_stream = BytesIO()
#     audio_segment.export(audio_stream, format="wav")
#     audio_stream.seek(0)
    
#     recognizer = sr.Recognizer()
#     with sr.AudioFile(audio_stream) as source:
#         audio_data = recognizer.record(source)
#         try:
#             text = recognizer.recognize_amazon(audio_data)
#             socketio.emit('transcription', text)
#         except sr.UnknownValueError:
#             socketio.emit('transcription', "Speech recognition could not understand audio")
#         except sr.RequestError as e:
#             socketio.emit('transcription', f"Could not request results from speech recognition service; {e}")

@app.route("/upload_audio", methods=['POST'])
def upload_audio():
    if 'audio_data' not in request.files:
        return 'No audio data!', 400

    audio_file = request.files['audio_data']
    audio_file_path = 'received_audio.webm' 
    audio_file.save(audio_file_path) # Saving the file to the server

    # Convert from WebM to WAV using pydub
    audio_segment = AudioSegment.from_file(audio_file_path, format="webm")
    wav_path = 'converted_audio.wav'
    audio_segment.export(wav_path, format="wav")

    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            return "Speech recognition could not understand audio"
        except sr.RequestError as e:
            return f"Could not request results from speech recognition service; {e}"
        
if __name__ == '__main__':
    app.run(debug=True, port=5003)
