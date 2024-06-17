from fastapi import UploadFile
import io
import openai
import os

class NamedBytesIO(io.BytesIO):
    def __init__(self, content, name):
        super().__init__(content)
        self.name = name


async def get_transcription(audio_file: UploadFile):
    openai.api_key = os.environ.get("OPENAI_API_KEY")

    # Read the file content into memory
    audio_content = await audio_file.read()

    # Create a NamedBytesIO object
    named_audio_file = NamedBytesIO(audio_content, audio_file.filename)

    # Transcribe the audio using OpenAI API
    translation = openai.Audio.transcribe(
        model="whisper-1",
        file=named_audio_file
    )
    return translation['text']