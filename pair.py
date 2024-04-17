class AudioThumbnailPair:
    def __init__(self, image:str, audio:str):
        self.image = image
        self.audio = audio

    def ffmpeg_clip(self) -> str:
        pass