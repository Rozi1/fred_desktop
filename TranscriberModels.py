import re
import openai
import whisper
import os
import torch
from keys import OPENAI_API_KEY
import traceback


openai.api_key = OPENAI_API_KEY

def get_model(use_api):
    if use_api:
        return APIWhisperTranscriber()
    else:
        return WhisperTranscriber()
    
def get_sentiment(text):
    prompt_text = """Classify the sentiment of the following earnings calls text as as positive, negative, or neutral. 
    text: {}
    sentiment: """.format(text)

    sentiment = openai.Completion.create(
                model="text-davinci-003",
                prompt = prompt_text,
                max_tokens= 15,
                temperature=0,
                )
    
    # remove special characters e.g n etc, from response
    sentiment = re.sub('W+','', sentiment['choices'][0]['text'])
    return sentiment
class WhisperTranscriber:
    def __init__(self):
        self.audio_model = whisper.load_model(os.path.join(os.getcwd(), 'tiny.en.pt'))
        print(f"[INFO] Whisper using GPU: " + str(torch.cuda.is_available()))
        
   

    def get_transcription(self, wav_file_path):
        try:
            result = self.audio_model.transcribe(wav_file_path, fp16=torch.cuda.is_available())
            sentiment=get_sentiment(result['text'].strip())

        except Exception as e:
            print(e)        
            return ''
        return result['text'].strip(), sentiment
    
class APIWhisperTranscriber:
    def get_transcription(self, wav_file_path):
        try:
            with open(wav_file_path, "rb") as audio_file:
                result = openai.Audio.transcribe("whisper-1", audio_file)
                sentiment=get_sentiment(result['text'].strip())
        except Exception as e:
            print(e)
            return ''
        return result['text'].strip(), sentiment