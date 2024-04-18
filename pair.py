class AudioThumbnailPair:
    def __init__(self, image:str, audio:str):
        self.image = image
        self.audio = audio

    def __str__(self) -> str:
        return f"AudioThumbnailPair:(image={self.image}, audio={self.audio})"

    def ffmpeg_clip(self) -> str:
        pass