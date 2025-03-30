from .Audio_Adaptor import Audio_Adaptor

class Audio:
    def __init__(self, adaptor: Audio_Adaptor):
        self.adaptor = adaptor
    
    def stream_audio_transcript_and_play(self, text) -> None:
        pass

    def audio_transcript_and_play(self, text) -> None:
        pass
    
    def audio_transcript_return_file(self, text) -> None:
        pass
