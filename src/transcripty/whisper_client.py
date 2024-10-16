import threading
import whisper  # type: ignore


class WhisperClient:
    def __init__(self, model_name: str) -> None:
        self.is_model_loaded: bool = False
        self.model_name: str = model_name
        self.load_model_thread = threading.Thread(target=self._load_model)
        self.load_model_thread.start()
        self.model: whisper.Whisper

    def _load_model(self) -> None:
        self.model = whisper.load_model(self.model_name)
        self.is_model_loaded = True

    def transcribe(self, audio_path: str) -> str:
        """Transcribe audio from the given path."""
        self.load_model_thread.join()  # Wait for the model to load
        assert self.is_model_loaded, "Model is not loaded yet"

        try:
            result = self.model.transcribe(audio_path)  # type: ignore
            return result["text"]  # type: ignore
        except Exception as e:
            print(f"Error during transcription: {e}")
            return "Transcription failed."
