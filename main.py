import tkinter
import threading
from AudioTranscriber import AudioTranscriber
from GPTResponder import GPTResponder
import customtkinter as ctk
import AudioRecorder 
import queue
import time
import torch
import sys
import TranscriberModels
import subprocess
import datetime

import openai
from keys import OPENAI_API_KEY
openai.api_key = OPENAI_API_KEY


import sounddevice as sd


stop_transcription_flag = threading.Event()
font_size=16
lines = []

def write_in_textbox(textbox, text):

    textbox.delete("0.0", "end")
    textbox.insert("0.0", text)
    textbox.see("end")

def update_transcript_UI(transcriber, textbox,stop_flag):
    
    if not stop_flag.is_set():
        transcript_string = transcriber.get_transcript()
        global lines;
        lines= transcript_string.split('\n')
        reversed_lines = lines[::-1]
        reversed_transcript = '\n'.join(reversed_lines)

        write_in_textbox(textbox, reversed_transcript)
        textbox.after(300, update_transcript_UI, transcriber, textbox,stop_flag)

def update_response_UI(responder, textbox, update_interval_slider_label, update_interval_slider, freeze_state):
    if not freeze_state[0]:
        response = responder.response

        textbox.configure(state="normal")
        write_in_textbox(textbox, response)
        textbox.configure(state="disabled")
        update_interval = int(update_interval_slider.get())
        responder.update_response_interval(update_interval)
        update_interval_slider_label.configure(text=f"Update interval: {update_interval} seconds")

    textbox.after(300, update_response_UI, responder, textbox, update_interval_slider_label, update_interval_slider, freeze_state)

def clear_context(transcriber, audio_queue):
    transcriber.clear_transcript_data()
    with audio_queue.mutex:
        audio_queue.queue.clear()  
        
def stop_transcription(stop_flag):
    stop_flag.set()
    print("stoping...")
    global lines;
    # print(lines)
    # # Format the list into a conversation
    # messages = []
    # for chat in lines:
    #     if chat:
    #         # Split the string into role, content, and emotion
    #         role, content = chat.split(': ')
    #         content, emotion = content.strip('[]').split(', ', 1)
    #         # Add to messages
    #         messages.append({"role": role, "content": content})

    # # Add a user message asking the model to summarize the conversation
    # messages.append({"role": "user", "content": "Can you summarize this conversation?"})

    # response = openai.ChatCompletion.create(
    # model="gpt-3.5-turbo",
    # messages=messages
    # )

    # print(response['choices'][0]['message']['content'])


def start_transcription(stop_flag):
    stop_flag.clear()
    print("starting...")
    



def create_ui_components(root):

    def update_ui(root):
        width = root.winfo_width()
        if width < 400:

            transcript_textbox.configure(font=("Arial", 14))  # Set font size to 10
            response_textbox.configure(font=("Arial", 14))  # Set font size to 10

            root.minsize(200, 700)  

            transcript_textbox.grid(row=0, column=0)
            clear_transcript_button.grid(row=1,column=0)
            start_transcript_button.grid(row=2,column=0)
            stop_transcript_button.grid(row=3, column=0)
            response_textbox.grid(row=4, column=0)
            freeze_button.grid(row=5, column=0)
            update_interval_slider_label.grid(row=6, column=0)
            update_interval_slider.grid(row=7, column=0)
            transcript_textbox.grid_propagate(False)  # Prevent the widget from changing its size
            transcript_textbox.grid_rowconfigure(0, minsize=500)
            
            response_textbox.grid_propagate(False)  # Prevent the widget from changing its size
            response_textbox.grid_rowconfigure(0, minsize=300)  # Set minimum height
        

       
        else:
            root.minsize(200, 600)
            transcript_textbox.configure(font=("Arial", 16))  # Set font size to 10
            response_textbox.configure(font=("Arial", 16)) 

            transcript_textbox.grid(row=0, column=0)
            clear_transcript_button.grid(row=1,column=0)
            start_transcript_button.grid(row=2,column=0)
            stop_transcript_button.grid(row=3, column=0)

            response_textbox.grid(row=0, column=1)
            freeze_button.grid(row=1, column=1)
            update_interval_slider_label.grid(row=2, column=1)
            update_interval_slider.grid(row=3, column=1)


    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("dark-blue")
    root.title("Fred Speech to Text")
    root.configure(bg='#252422')
    root.minsize(200, 600)  # Minimum size of the window
    root.maxsize(1000, 600)  # Maximum size of the window
    root.geometry("1000x600")
    root.grid_columnconfigure(0, minsize=200)

    root.bind('<Configure>', lambda event: update_ui(root))

    transcript_textbox = ctk.CTkTextbox(root, width=300, font=("Arial", font_size), text_color='#000000', wrap="word")
    transcript_textbox.grid(row=0, column=0, padx=10, pady=20, sticky="nsew")

    response_textbox = ctk.CTkTextbox(root, width=300, font=("Arial", font_size), text_color='#639cdc', wrap="word")
    response_textbox.grid(row=0, column=1, padx=10, pady=20, sticky="nsew")

    freeze_button = ctk.CTkButton(root, text="Freeze", command=None)
    freeze_button.grid(row=1, column=1, padx=10, pady=3, sticky="nsew")

    update_interval_slider_label = ctk.CTkLabel(root, text=f"", font=("Arial", 12), text_color="#000000")
    update_interval_slider_label.grid(row=2, column=1, padx=10, pady=3, sticky="nsew")

    update_interval_slider = ctk.CTkSlider(root, from_=1, to=10, width=300, height=20, number_of_steps=9)
    update_interval_slider.set(2)
    update_interval_slider.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")

         # Add the clear transcript button to the UI
    clear_transcript_button = ctk.CTkButton(root, text="Clear Transcript", command=None)
    clear_transcript_button.grid(row=1, column=0, padx=10, pady=3, sticky="nsew")

    stop_transcript_button = ctk.CTkButton(root, text="Stop Transcription", command=None)
    stop_transcript_button.grid(row=2, column=0, padx=10, pady=3, sticky="nsew")
    
    start_transcript_button = ctk.CTkButton(root, text="Start Transcription", command=None)
    start_transcript_button.grid(row=3, column=0, padx=10, pady=3, sticky="nsew")



    return transcript_textbox, response_textbox, update_interval_slider, update_interval_slider_label, freeze_button, clear_transcript_button, start_transcript_button, stop_transcript_button

def main():
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        print("ERROR: The ffmpeg library is not installed. Please install ffmpeg and try again.")
        return

    root = ctk.CTk()
    transcript_textbox, response_textbox, update_interval_slider, update_interval_slider_label, freeze_button, clear_transcript_button, start_transcript_button, stop_transcript_button = create_ui_components(root)

    audio_queue = queue.Queue()

    user_audio_recorder = AudioRecorder.DefaultMicRecorder()
    user_audio_recorder.record_into_queue(audio_queue,stop_transcription_flag)

    time.sleep(2)

    speaker_audio_recorder = AudioRecorder.DefaultSpeakerRecorder()
    speaker_audio_recorder.record_into_queue(audio_queue,stop_transcription_flag)
    
  

    model = TranscriberModels.get_model('--api' in sys.argv)

    with audio_queue.mutex:
        audio_queue.queue.clear()
    transcriber = AudioTranscriber(user_audio_recorder.source, speaker_audio_recorder.source, model)
    transcribe = threading.Thread(target=transcriber.transcribe_audio_queue, args=(audio_queue,stop_transcription_flag))
    transcribe.daemon = True
    transcribe.start()

    responder = GPTResponder()
    respond = threading.Thread(target=responder.respond_to_transcriber, args=(transcriber,stop_transcription_flag))
    respond.daemon = True
    respond.start()

    print("READY")

    root.grid_rowconfigure(0, weight=100)
    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=1)
    root.grid_rowconfigure(3, weight=1)
    root.grid_columnconfigure(0, weight=2)
    root.grid_columnconfigure(1, weight=1)
    

    freeze_state = [False]  # Using list to be able to change its content inside inner functions
    def freeze_unfreeze():
        freeze_state[0] = not freeze_state[0]  # Invert the freeze state
        freeze_button.configure(text="Unfreeze" if freeze_state[0] else "Freeze")

    freeze_button.configure(command=freeze_unfreeze)
    
    def toggle_transcription(stop_transcription_flag):
            stop_transcription(stop_transcription_flag)
 
    def start_transcript(stop_transcription_flag):
        
            start_transcription(stop_transcription_flag)
            update_transcript_UI(transcriber, transcript_textbox, stop_transcription_flag)
            update_response_UI(responder, response_textbox, update_interval_slider_label, update_interval_slider, freeze_state)
 
    
    clear_transcript_button.configure( command=lambda: clear_context(transcriber, audio_queue, ))
    stop_transcript_button.configure(command=lambda: toggle_transcription(stop_transcription_flag))
    start_transcript_button.configure(command=lambda: start_transcript(stop_transcription_flag))



    update_interval_slider_label.configure(text=f"Update interval: {update_interval_slider.get()} seconds")

    update_transcript_UI(transcriber, transcript_textbox, stop_transcription_flag)
    update_response_UI(responder, response_textbox, update_interval_slider_label, update_interval_slider, freeze_state)
 
    root.mainloop()

if __name__ == "__main__":
    main()