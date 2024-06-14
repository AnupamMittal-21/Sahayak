from fastapi import FastAPI
from pydantic import BaseModel
from transcribe import transcribe_file
from polly import get_speech
from GoEmotion import get_sentiment
from openAi import get_embeddings
from firebase import get_previous_query_data
import boto3

# import datetime
# timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

app = FastAPI()


class RequestModel(BaseModel):
    audio_link: str
    category: int
    uid: str


class ResponseModel(BaseModel):
    response_audio_link: str


@app.post("/get_response", response_model=ResponseModel)
def get_response(request: RequestModel):

    # Extract the strings from the request
    audio_link = request.audio_link
    category = request.category
    uid = request.uid

    file_name = audio_link.split('request/')[1]

    # Creating object of Amazon Transcribe and calling the function with required parameters
    transcribe_client = boto3.client('transcribe')
    transcript = transcribe_file(job_name=file_name, file_uri=audio_link, transcribe_client=transcribe_client)

    # Performing Sentiment analysis of the whole transcript using GoEmotion.
    sentiment = get_sentiment(transcript)

    # Creating Embeddings of the transcript using OpenAI.
    user_query_embeddings = get_embeddings(transcript)

    # Getting the previous query data and finding the top similar vectors.
    previous_and_current_embeddings = get_previous_query_data(uid=uid, category=category, user_query_vector=user_query_embeddings)

    # Pass the joint embeddings to service data base for similarity search.
    # Get the top 3 similar vectors and their cosine similarities.
    # Pass the the data to OpenAI Model.

    # Processing the audio link for saving the speech by Amazon polly.
    response_audio_link = audio_link
    response_audio_link = str.replace(response_audio_link, "request", "response")
    response_audio_s3_key = response_audio_link.split("s3.amazonaws.com/")[1]

    get_speech(text=transcript, polly=boto3.client("polly"), s3_client=boto3.client('s3'), bucket_name='hackon', s3_key = response_audio_s3_key)
    response1 = response_audio_link
    response1 += "?category=" + str(category)
    response1 += "&uid=" + str(uid)
    response1 += "&sentiment=" + str(sentiment)

    # Return the response model
    return ResponseModel(response_audio_link=response1)

# Default root endpoint
@app.get("/")
def read_root():
    return {"Info": "Enter '/get_response' to get correct response"}