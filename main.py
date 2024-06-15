import os

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from transcribe import transcribe_file
from polly import get_speech
from GoEmotion import get_sentiment
from openAi import get_embeddings
from firebase import get_previous_query_data
from llm_response import get_response_from_llm
from service_db import get_services_response
from firebase import update_session
import boto3
import firebase_admin
from firebase_admin import credentials

app = FastAPI()

session = boto3.Session(
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    region_name=os.environ.get("AWS_REGION")  # Optional
)


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

    # One of the exception in transcribe is of same file name, this can be effectively handled by saving the file name by timestamp.
    file_name = audio_link.split('request/')[1]+"217"

    # Creating object of Amazon Transcribe and calling the function with required parameters
    transcribe_client = boto3.client('transcribe')
    transcript = transcribe_file(job_name=file_name, file_uri=audio_link, transcribe_client=transcribe_client)

    # Performing Sentiment analysis of the whole transcript using GoEmotion.
    sentiment = get_sentiment(transcript)

    # Creating Embeddings of the transcript using OpenAI.
    user_query_embeddings = get_embeddings(transcript)

    cred = credentials.Certificate("vcs-hackon-firebase.json")
    firebase_admin.initialize_app(cred)
    # Getting the previous query data and finding the top similar vectors.
    previous_similar_queries, previous_similar_response, previous_similar_sentiments, embeddings_query_and_previous = get_previous_query_data(uid=uid, category=category, user_query_vector=user_query_embeddings)

    # Calculate the similarity between combined query and service database and get responses.
    service_database_answers = get_services_response(embeddings_query_and_previous)
    # Pass the previous query data, the sentiment, the user query and the service database answers to the OpenAI model.
    response_llm = get_response_from_llm(user_query=transcript, sentiment=sentiment, previous_queries=previous_similar_queries, previous_responses=previous_similar_response, previous_sentiments=previous_similar_sentiments, service_database_answers=service_database_answers)
    # Processing the audio link for saving the speech by Amazon polly.

    update_session(uid=uid,category=category, new_embedding=user_query_embeddings, new_query=transcript, new_response=response_llm, new_sentiment=sentiment)

    response_audio_link = audio_link
    response_audio_link = str.replace(response_audio_link, "request", "response")
    response_audio_s3_key = response_audio_link.split("s3.amazonaws.com/")[1]

    get_speech(text=response_llm, polly=boto3.client('polly', region_name='us-west-2'), s3_client = boto3.client('s3', region_name='us-west-2'), bucket_name='hackon', s3_key = response_audio_s3_key)
    response1 = response_audio_link

    # Return the response model
    return ResponseModel(response_audio_link=response1)

# Default root endpoint
@app.get("/")
def read_root():
    return {"Info": "Enter '/get_response' to get correct response"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)

# uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)