import wave
import struct
from pvrecorder import PvRecorder  # type: ignore
import threading
from datetime import datetime


class AudioRecorder:
    def __init__(self) -> None:
        # Initialize recording parameters
        self.frame_size: int = 512
        self.recording_data: list[int] = []
        self.is_recording: bool = False
        self.recorder: PvRecorder = PvRecorder(device_index=0, frame_length=512)
        # Retrieve available devices for the recorder
        self.devices: list[tuple[int, str]] = [
            (index, device)
            for index, device in enumerate(PvRecorder.get_available_devices())
        ]

    def set_device(self, device_index: int) -> None:
        """Set the audio recorder device."""
        self.recorder = PvRecorder(device_index=device_index, frame_length=512)

    def start_recording(self) -> None:
        """Start recording audio."""
        self.recorder.start()
        self.is_recording = True

        # Continuously read and store audio data while recording
        def read_audio():
            while self.is_recording:
                frame: list[int] = self.recorder.read()
                self.recording_data.extend(frame)

        threading.Thread(target=read_audio).start()

    def stop_recording(self) -> None:
        """Stop recording audio."""
        self.is_recording = False
        self.recorder.stop()

    def save_audio(self) -> str:
        """Save recorded audio to a WAV file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"rec_{timestamp}.wav"
        with wave.open(filename, "wb") as f:
            f.setparams((1, 2, 16000, 512, "NONE", "NONE"))
            f.writeframes(
                struct.pack("h" * len(self.recording_data), *self.recording_data)
            )
        self.recording_data.clear()  # Clear the recording data
        return filename
