from gtts import gTTS
import os

class WrapperForTypeHintingBecauseOfStupidWSLBullshit(gTTS):
    def save(self, filename, *args, **kwargs):
        super().save(f"audio_temp/bad_{filename}", *args, **kwargs)
        os.system(f"ffmpeg -i 'concat:audio_temp/bad_{filename}|img_assets/sec_3.mp3' audio_temp/{filename}")

class TextToSpeech:
    def __init__(self, *args, **kwargs):
        self.args = args 
        self.kwargs = kwargs

    def __call__(self, text:str) -> WrapperForTypeHintingBecauseOfStupidWSLBullshit:
        obj = WrapperForTypeHintingBecauseOfStupidWSLBullshit(text=text, *self.args, **self.kwargs) # TODO options
        return obj
    

