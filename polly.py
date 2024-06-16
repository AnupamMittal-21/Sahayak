from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import io
import sys

# polly = boto3.client("polly")
# s3_client = boto3.client('s3')
# bucket_name = 'hackon'
# s3_key = 'path/in/bucket/speech2.mp3'


def get_speech(text, polly):

    try:
        # Request speech synthesis
        response = polly.synthesize_speech(Text= text, OutputFormat="mp3", VoiceId="Joanna")
    except (BotoCoreError, ClientError) as error:
        # The service returned an error, exit gracefully
        print(error)
        sys.exit(-1)

    # Access the audio stream from the response
    if "AudioStream" in response:
        # Note: Closing the stream is important because the service throttles on the
        # number of parallel connections. Here we are using contextlib.closing to
        # ensure the close method of the stream object will be called automatically
        # at the end of the with statement's scope.
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

# get_speech("Welcome! To record your query, click the Start button. When you're finished, click Stop, and then click Send to receive a response. If you face any issues, click Restart to record your query again.", polly=boto3.client("polly"), s3_client=boto3.client('s3'), bucket_name='hackon', s3_key = 'path/in/bucket/Intro2.mp3')

# URL: https://hackon.s3.amazonaws.com/path/in/bucket/speech.mp3