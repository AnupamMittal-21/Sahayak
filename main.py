import os
import random
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
from dotenv import load_dotenv
import boto3
import firebase_admin
from firebase_admin import credentials

app = FastAPI()
load_dotenv()

session = boto3.Session(
    aws_access_key_id=os.environ.get("ACCESS_KEY"),
    aws_secret_access_key=os.environ.get("SECRET_ACCESS_KEY"),
    region_name=os.environ.get("REGION")  # Optional
)


class RequestModel(BaseModel):
    audio_link: str
    category: int
    uid: str

#
# class ResponseModel(BaseModel):
#     response_audio_link: str


@app.post("/get_response")
def get_response(request: RequestModel):

    try:
        # Extract the strings from the request
        audio_link = request.audio_link
        category = request.category
        uid = request.uid
        print("Extracted audio link")


#       ########################################## Transcription #################################

        file_name = str(random.randint(1000, 9999))

        transcribe_client = boto3.client(
            'transcribe',
            region_name='us-east-1',
            aws_access_key_id=os.environ.get("ACCESS_KEY"),
            aws_secret_access_key=os.environ.get("SECRET_ACCESS_KEY"),
        )

        transcript = transcribe_file(job_name=file_name, file_uri=audio_link, transcribe_client=transcribe_client)

        if transcript == "":
            return {"Error": "Error in Transcription"}

        print(f"Transcript : {transcript}")


#       ###################################### Sentiment Analysis ################################

        # There is some problem with the sentiment analysis, so we are using a static value for now.
        # Performing Sentiment analysis of the whole transcript using GoEmotion.
        # sentiment = get_sentiment(transcript)
        sentiment = "frustrated"
        print(f"Sentiment: {sentiment}")


#       ########################################## Embeddings #####################################

        # Creating Embeddings of the transcript using OpenAI.
        user_query_embeddings = get_embeddings(transcript)
        if not user_query_embeddings:
            return {"Error": "Error in getting transcription embeddings"}

        print(f"Embeddings = {user_query_embeddings}")


#       ########################################### Firebase ######################################

        try:
            cred = credentials.Certificate("vcs-hackon-firebase.json")
            firebase_admin.initialize_app(cred)
        except Exception as e:
            print(f"Error in initializing firebase : {e}")
            return {"Error": "Error in initializing firebase"}

        print("Firebase Initialized")
        categories_list = ['generals', 'aws', 'order', 'prime', 'refund', 'retailer']
        # Getting the previous query data and finding the top similar vectors.
        previous_similar_queries, previous_similar_response, previous_similar_sentiments, embeddings_query_and_previous = get_previous_query_data(uid=uid, category=categories_list[category], user_query_vector=user_query_embeddings)

        print(f"Previous Queries + User Query : {embeddings_query_and_previous}")


#       ########################################### Service DB #####################################

        # Calculate the similarity between combined query and service database and get responses.
        service_database_answers = get_services_response(embeddings_query_and_previous)


#       ########################################### LLM (OpenAI) ####################################

        # Pass the previous query data, the sentiment, the user query and the service database answers to the OpenAI.
        response_llm = get_response_from_llm(user_query=transcript, sentiment=sentiment, previous_queries=previous_similar_queries, previous_responses=previous_similar_response, previous_sentiments=previous_similar_sentiments, service_database_answers=service_database_answers)
        if response_llm == "":
            return {"Error": "Error in getting response from LLM"}

        print(f"Response from LLM : {response_llm}")


#       ###################################### Update DataBase ######################################

        # Processing the audio link for saving the speech by Amazon polly.
        update_session(uid=uid,category=category, new_embedding=user_query_embeddings, new_query=transcript, new_response=response_llm, new_sentiment=sentiment)
        print("Session Updated")

#       ########################################### Polly ############################################

        response_audio_link = audio_link
        response_audio_link = str.replace(response_audio_link, "request", "response")
        response_audio_s3_key = response_audio_link.split("s3.amazonaws.com/")[1]

        polly_obj = boto3.client(
            'polly',
            region_name='us-east-1',
            aws_access_key_id=os.environ.get("ACCESS_KEY"),
            aws_secret_access_key=os.environ.get("SECRET_ACCESS_KEY"),
        )

        s3_obj = boto3.client(
            's3',
            region_name='us-east-1',
            aws_access_key_id=os.environ.get("ACCESS_KEY"),
            aws_secret_access_key=os.environ.get("SECRET_ACCESS_KEY"),
        )

        get_speech(text=response_llm, polly=polly_obj, s3_client=s3_obj, bucket_name='hackon', s3_key = response_audio_s3_key)
        response1 = response_audio_link

        return {"response_audio_link": response1}

    except Exception as e:
        return {"Error": f"Some Exception occurred, Details are : {e}"}

@app.get("/")
def read_root():
    return {"Info": "Enter '/get_response' to get correct response"}

# if __name__ == "__main__":
#     print(f"Region is : {os.environ.get('REGION')}")
#     port = int(os.environ.get("PORT", 8000))
#     print(f"Starting server on port {port}")
#     uvicorn.run('main:app', host="0.0.0.0", port=port, reload= True)