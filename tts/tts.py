from gtts import gTTS
import os

class TTS(gTTS):
    def save(self, filename, *args, **kwargs):
        super().save(f"audio_temp/bad_{filename}", *args, **kwargs)
        os.system("yes | touch audio_temp/concat.txt")
        os.system(f"echo \"file 'bad_{filename}'\nfile '../img_assets/sec_3.mp3'\" > audio_temp/concat.txt")
        os.system(f"yes | ffmpeg -safe 0 -f concat -i audio_temp/concat.txt -c copy audio_temp/{filename}")

class TextToSpeech:
    def __init__(self, *args, **kwargs):
        self.args = args 
        self.kwargs = kwargs

    def __call__(self, text:str) -> TTS:
        return TTS(text=text, *self.args, **self.kwargs)
    

