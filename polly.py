from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import io
import sys


def get_speech(text, polly, voice_id):
    try:
        response = polly.synthesize_speech(Text=text, OutputFormat="mp3", VoiceId=voice_id)
    except (BotoCoreError, ClientError) as error:
        print(error)
        sys.exit(-1)

    if "AudioStream" in response:
        with closing(response["AudioStream"]) as stream:
            try:
                audio_stream = io.BytesIO()
                audio_stream.write(stream.read())
                audio_stream.seek(0)
                return audio_stream
            except IOError as error:
                print(error)
                sys.exit(-1)
    else:
        print("Could not stream audio")
        sys.exit(-1)
