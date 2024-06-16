import boto3
def transcribe_audio(audio_stream, job_name, language_code='en-US'):
    transcribe = boto3.client('transcribe')

    try:
        # Start transcription job
        response = transcribe.start_transcription_job(
            TranscriptionJobName=job_name,
            LanguageCode=language_code,
            MediaFormat='mp3',
            Media={
                'MediaByteStream': audio_stream
            }
        )
        print(f"Transcription job {job_name} started successfully.")
        return response
    except Exception as e:
        print(f"Error starting transcription job: {str(e)}")
        return None