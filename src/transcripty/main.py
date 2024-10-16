import json
import os
import flet as ft
from transcripty.audio_recorder import AudioRecorder
from transcripty.whisper_client import WhisperClient


class VoiceRecorderApp:
    """Voice Recorder Application that allows recording audio and transcribing it."""

    def __init__(self) -> None:
        # Initialize theme data
        self.theme_data: tuple[bool, ft.ThemeMode] | None = None

        # Create an instance of AudioRecorder
        self.audio_recorder = AudioRecorder()

        # Label for recording status
        self.record_label = ft.Text("Tap to Record", size=18, color=ft.colors.WHITE)
        self.page: ft.Page

        # Theme toggle switch
        self.theme_toggle = ft.Switch(
            label="Toggle Light/Dark Mode",
            value=self.load_theme_state()[0],
            data=self.load_theme_state()[1],  # Load theme state from file
            on_change=self.toggle_theme,
        )

        # Initialize WhisperClient for audio transcription
        self.model = WhisperClient(model_name="turbo")
        self.devices_dropdown: ft.Dropdown

        # Text field for showing recognized text
        self.recognized_text_box = ft.Text(
            expand=True, style=ft.TextStyle(size=20), weight=ft.FontWeight.W_400
        )

        # Progress indicator for loading animation
        self.loading_indicator = ft.Column(
            [
                ft.ProgressRing(),
                ft.Text("Transcribing ...", size=24),
            ],
            visible=False,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def set_recorder(self, e: ft.ControlEvent) -> None:
        """Set the recorder device from dropdown selection."""
        device_index = int(e.data)
        self.audio_recorder.set_device(device_index)

    def handle_start_recording(self, e: ft.ControlEvent) -> None:
        """Start recording audio and update UI components."""
        self.record_label.value = "Recording..."
        self.record_label.update()
        # Disable copy button when there isn't transcribed text
        self.copy_button.disabled = True
        self.copy_button.update()
        self.devices_dropdown.disabled = (
            True  # Disable device selection during recording
        )
        self.devices_dropdown.update()
        self.audio_recorder.start_recording()

        # Change the background color of the recording container
        self.record_container.bgcolor = ft.colors.RED_ACCENT  # type: ignore
        self.record_container.update()

    def handle_stop_recording(self, e: ft.ControlEvent) -> None:
        """Stop recording, save the audio, and prepare for transcription."""
        self.audio_recorder.stop_recording()
        self.audio_file = self.audio_recorder.save_audio()
        self.record_label.value = "Tap to Record"
        self.record_label.update()

        # Reset the background color of the recording container
        self.record_container.bgcolor = ft.colors.BLUE_ACCENT  # type: ignore
        self.record_container.update()

        # Re-enable device selection
        self.devices_dropdown.disabled = False
        self.devices_dropdown.update()

        self.recognize_audio()  # Start audio transcription

    def handle_click(self, e: ft.ControlEvent) -> None:
        """Toggle recording state on click."""
        if self.audio_recorder.is_recording:
            self.handle_stop_recording(e)  # Stop recording if currently recording
        else:
            self.handle_start_recording(e)  # Start recording otherwise

    def toggle_theme(self, e: ft.ControlEvent) -> None:
        """Toggle between light and dark themes."""
        new_theme = (
            ft.ThemeMode.DARK
            if self.page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        self.page.theme_mode = new_theme
        self.page.update()  # type: ignore
        self.save_theme_state(self.page.theme_mode)  # Save the new theme state

    def load_theme_state(self) -> tuple[bool, ft.ThemeMode]:
        """Load the theme state from a JSON file."""
        if self.theme_data:
            return self.theme_data

        try:
            if os.path.exists("theme_state.json"):
                with open("theme_state.json", "r") as f:
                    data = json.load(f)
                    cond = data.get("theme_mode", "ThemeMode.LIGHT") == "ThemeMode.DARK"
                    return cond, ft.ThemeMode.DARK if cond else ft.ThemeMode.LIGHT
        except:  # noqa: E722
            pass
        return False, ft.ThemeMode.LIGHT

    def save_theme_state(self, theme_mode: ft.ThemeMode) -> None:
        """Save the theme state to a JSON file."""
        with open("theme_state.json", "w") as f:
            json.dump({"theme_mode": str(theme_mode)}, f)

    async def build_ui(self, page: ft.Page) -> None:
        """Build the Flet UI for the voice recorder app."""
        self.page = page
        page.title = "Transcripty"
        page.theme_mode = self.theme_toggle.data  # type: ignore

        # Dropdown for device selection
        self.devices_dropdown = ft.Dropdown(
            label=str(self.audio_recorder.devices[0][1] or "Select Device"),
            options=[
                ft.dropdown.Option(text=device[1], key=str(device[0]))
                for device in self.audio_recorder.devices
            ],
            on_change=self.set_recorder,
            disabled=False,
        )

        # Container for recording controls
        self.record_container = ft.Container(
            content=self.record_label,
            padding=10,
            bgcolor=ft.colors.BLUE_ACCENT,
            alignment=ft.alignment.center,
            on_click=self.handle_click,
        )

        # Copy button to copy recognized text
        self.copy_button = ft.ElevatedButton(
            text="Copy Text",
            on_click=self.copy_text,
            disabled=True,
        )

        # Add all components to the page
        page.add(
            ft.Column(
                [
                    ft.Row(
                        [self.devices_dropdown, self.theme_toggle],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Text("Voice Recorder", size=24),
                    self.record_container,
                    self.loading_indicator,
                    ft.Container(
                        content=self.copy_button,
                        alignment=ft.Alignment(1.0, 0.0),
                    ),
                    ft.Stack(
                        [
                            ft.Container(
                                content=self.recognized_text_box,  # Add recognized text box
                                border=ft.border.all(1, ft.colors.GREY),
                                border_radius=ft.border_radius.all(5),
                                expand=True,
                                alignment=ft.alignment.top_center,
                            ),
                        ],
                        expand=True,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            )
        )

    def copy_text(self, e: ft.ControlEvent) -> None:
        """Copy the transcribed text to the clipboard."""
        if self.recognized_text_box.value:
            self.page.set_clipboard(self.recognized_text_box.value)
            self.page.show_snack_bar(ft.SnackBar(ft.Text("Text copied to clipboard!")))

    def recognize_audio(self) -> None:
        """Recognize audio from the recorded file."""
        self.loading_indicator.visible = True
        self.loading_indicator.update()
        self.record_container.disabled = True  # Disable recording during transcription
        self.record_container.bgcolor = ft.colors.GREY
        self.record_container.update()

        if not self.model.is_model_loaded:
            # Update loading status while model is loading
            self.loading_indicator.controls[1].value = "Loading model..."
            self.loading_indicator.controls[1].update()
            self.model.load_model_thread.join()
            self.loading_indicator.controls[1].value = "Transcribing..."
            self.loading_indicator.controls[1].update()

        # Transcribe the audio file
        self.recognized_text_box.value = self.model.transcribe(self.audio_file)
        self.recognized_text_box.update()

        self.loading_indicator.visible = False
        self.loading_indicator.update()

        # Re-enable recording after transcription
        self.record_container.disabled = False
        self.record_container.bgcolor = ft.colors.BLUE_ACCENT
        self.record_container.update()

        # Enable copy button when there is transcribed text
        self.copy_button.disabled = False
        self.copy_button.update()


def main() -> None:
    """Main entry point for the application."""
    app_instance = VoiceRecorderApp()
    ft.app(app_instance.build_ui)  # type: ignore
