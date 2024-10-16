# Transcripty

Transcripty is a voice recorder application that allows users to record audio and transcribe it into text. Built with Python using the Flet framework, it provides a simple and user-friendly interface for audio recording and transcription.

## Features

- Record audio from selected devices
- Transcribe recorded audio using Whisper
- Toggle between light and dark themes
- Save recordings as WAV files

## Requirements

- Python 3.11.10 or higher
- Internet connection for model downloading

## Installation

### Clone the repository

```bash
git clone https://github.com/Abdulkhale-1/transcripty.git
cd transcripty
```

### Install dependencies

You can use `uv` to install the required dependencies. Make sure to create a virtual environment for better package management.

```bash
pip install uv
uv venv .venv
uv sync
```


### Run the application

To start the Transcripty application, use the following command:

```bash
uv run main
```

## Usage

1. **Select an audio recording device** from the dropdown menu.
2. **Click on the "Tap to Record" button** to start recording. The button label will change to "Recording...".
3. **Click the button again** to stop the recording. The audio will be saved automatically.
4. The application will automatically transcribe the recorded audio, and the result will be displayed on the screen.
5. Use the theme toggle switch to switch between light and dark modes.

## Contributing

If you would like to contribute to the Transcripty project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with descriptive messages.
4. Push your branch to your fork.
5. Create a pull request explaining your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgements

- [Flet](https://flet.dev/) - A framework for building interactive web apps in Python
- [OpenAI Whisper](https://github.com/openai/whisper) - A speech recognition model
- [PvRecorder](https://github.com/Picovoice/pvrecorder) - A simple audio recorder for Python

## Contact

For any questions or inquiries, please contact me at [abdulkhalek.muhammad.work@gmail.com](mailto:abdulkhalek.muhammad.work@gmail.com).