import tkinter as tk
import sounddevice as sd
import speech_recognition as sr
import threading
import queue

# Global variables
is_recording = False
audio_queue = queue.Queue()

# Function to continuously record audio
def continuous_record(sample_rate=16000, chunk_size=1024):
    global is_recording
    with sd.InputStream(samplerate=sample_rate, channels=1, callback=audio_callback):
        while is_recording:
            sd.sleep(1000)

# Audio callback function for sounddevice
def audio_callback(indata, frames, time, status):
    audio_queue.put(indata.copy())

# Function to recognize speech from audio chunks
def recognize_speech_from_audio():
    recognizer = sr.Recognizer()
    while is_recording:
        try:
            audio_chunk = audio_queue.get()
            if audio_chunk is not None:
                with sr.AudioData(audio_chunk, 16000, 2) as source:
                    try:
                        text = recognizer.recognize_google(source, show_all=False)
                        update_text_area(text + '\n')
                    except sr.UnknownValueError:
                        pass  # Do nothing if the chunk is not understood
        except queue.Empty:
            pass

# Function to update the text area
def update_text_area(text):
    text_area.configure(state='normal')
    text_area.insert(tk.END, text)
    text_area.configure(state='disabled')
    text_area.see(tk.END)

# Function to start recording
def start_recording():
    global is_recording
    is_recording = True
    threading.Thread(target=continuous_record).start()
    threading.Thread(target=recognize_speech_from_audio).start()

# Function to stop recording
def stop_recording():
    global is_recording
    is_recording = False

# Create the GUI
root = tk.Tk()
root.title("Voice Recorder and Transcriber")

start_button = tk.Button(root, text="Start Recording", command=start_recording)
start_button.pack()

stop_button = tk.Button(root, text="Stop Recording", command=stop_recording)
stop_button.pack()

text_area = tk.Text(root, height=10, width=50, state='disabled')
text_area.pack()

root.mainloop()
