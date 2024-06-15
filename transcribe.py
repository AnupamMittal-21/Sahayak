import time
import urllib
import json

# For checking the transcribe function
# import boto3
# transcribe_client = boto3.client('transcribe')


def transcribe_file(job_name, file_uri, transcribe_client):
    try:
        # The below try-Except block is to handle the case of same file name.
        transcript = None
        try:
            transcribe_client.start_transcription_job(
                TranscriptionJobName=job_name,
                IdentifyLanguage=True,
                IdentifyMultipleLanguages=True,
                Media={'MediaFileUri': file_uri},
                MediaFormat='mp3',
            )
        except Exception as e:
            print(f"Error in transcribe_file function : {e}")

        max_tries = 10
        while max_tries > 0:
            max_tries -= 1
            job = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
            job_status = job['TranscriptionJob']['TranscriptionJobStatus']
            if job_status in ['COMPLETED', 'FAILED']:
                if job_status == 'COMPLETED':
                    response = urllib.request.urlopen(job['TranscriptionJob']['Transcript']['TranscriptFileUri'])
                    data = json.loads(response.read())
                    transcript = data['results']['transcripts'][0]['transcript']
                break
            else:
                print(f"Waiting for {job_name}. Current Status is {job_status}")
                transcript = ""
                time.sleep(6)
        print(f"Transcript Successful Retrieved : {transcript}")
        return transcript
    except Exception as e:
        print(f"Error in transcribe_file function : {e}")
        return ""

# For Checking Purpose Only.
# file_uri = 'https://hackon.s3.amazonaws.com/english_trial.mp3'
# file_uri = 'https://hackon.s3.amazonaws.com/hindi_english.mp3'
# file_uri = 'https://hackon.s3.amazonaws.com/path/in/bucket/speech2.mp3'
# transcribe_file('2378', file_uri, transcribe_client)

