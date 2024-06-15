# import boto3
import time
import urllib
import json

# transcribe_client = boto3.client('transcribe')


def transcribe_file(job_name, file_uri, transcribe_client):
    transcript = None
    transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        IdentifyLanguage=True,
        IdentifyMultipleLanguages=True,
        Media={'MediaFileUri': file_uri},
        MediaFormat='mp3',
    )

    max_tries =  10
    while max_tries > 0:
        max_tries -= 1
        job = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        job_status = job['TranscriptionJob']['TranscriptionJobStatus']
        if job_status in ['COMPLETED', 'FAILED']:
            if job_status == 'COMPLETED':
                response = urllib.request.urlopen(job['TranscriptionJob']['Transcript']['TranscriptFileUri'])
                data = json.loads(response.read())
                text = data['results']['transcripts'][0]['transcript']
                transcript = text
                print(f"Transcript Succesfull : {transcript}")
            break
        else:
            print(f"Waiting for {job_name}. Current Status is {job_status}")
            transcript = "Sorry, can you please repeat that?"
            time.sleep(6)

    print(f"Transcript inside the function is : {transcript}")
    return transcript


# def main():
#
#     # file_uri = 'https://hackon.s3.amazonaws.com/english_trial.mp3'
#     # file_uri = 'https://hackon.s3.amazonaws.com/hindi_english.mp3'
#     file_uri = 'https://hackon.s3.amazonaws.com/path/in/bucket/speech2.mp3'
#     transcribe_file('Example-Job_4', file_uri, transcribe_client)
#
# if __name__ == "__main__":
#     main()


