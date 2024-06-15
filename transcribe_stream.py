import boto3
import time
import threading
import asyncio
from pydub import AudioSegment
from amazon_transcribe.client import TranscribeStreamingClient
from amazon_transcribe.handlers import TranscriptResultStreamHandler
from amazon_transcribe.model import TranscriptEvent

class MyEventHandler(TranscriptResultStreamHandler):
    def __init__(self, transcript_result_stream):
        super().__init__(transcript_result_stream)

    async def handle_transcript_event(self, transcript_event: TranscriptEvent):
        results = transcript_event.transcript.results
        for result in results:
            for alt in result.alternatives:
                print(f'Transcript: {alt.transcript}')

async def transcribe_audio(pcm_audio_path):
    client = TranscribeStreamingClient(region="us-east-1")
    stream = await client.start_stream_transcription(
        language_code="en-US",
        media_sample_rate_hz=16000,
        media_encoding="pcm",
    )

    handler = MyEventHandler(stream.output_stream)
    handler_task = asyncio.create_task(handler.handle_events())

    with open(pcm_audio_path, 'rb') as audio_file:
        while chunk := audio_file.read(1024):
            await stream.input_stream.send_audio_event(audio_chunk=chunk)

    await stream.input_stream.end_stream()
    await handler_task

def convert_mp3_to_pcm(mp3_file_path, pcm_file_path):
    audio = AudioSegment.from_mp3(mp3_file_path)
    audio = audio.set_frame_rate(16000).set_channels(1)
    audio.export(pcm_file_path, format="wav")

# if __name__ == "__main__":
#     mp3_file_path = "english_trial.mp3"
#     pcm_file_path = "audiofile.pcm"
#
#     convert_mp3_to_pcm(mp3_file_path, pcm_file_path)
#
#     asyncio.run(transcribe_audio(pcm_file_path))
