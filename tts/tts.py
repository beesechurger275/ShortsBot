from gtts import gTTS

class WrapperForTypeHintingBecauseOfStupidWSLBullshit(gTTS):
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class TextToSpeech:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __call__(self, text:str) -> WrapperForTypeHintingBecauseOfStupidWSLBullshit:
        obj = WrapperForTypeHintingBecauseOfStupidWSLBullshit(text=text, *self.args, **self.kwargs) # TODO options
        return obj
    

