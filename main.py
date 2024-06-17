import uvicorn
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
from firebase_admin import firestore
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from transcription_whisper import get_transcription
from typing import Optional
from fastapi import FastAPI, File, UploadFile, Form
import os

app = FastAPI()
load_dotenv()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,  # Allow cookies and HTTP authentication
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

session = boto3.Session(
    aws_access_key_id=os.environ.get("ACCESS_KEY"),
    aws_secret_access_key=os.environ.get("SECRET_ACCESS_KEY"),
    region_name=os.environ.get("REGION")
)


@app.post("/get_response")
async def get_response(
        file: UploadFile = File(...),
        category: int = Form(...),
        uid: Optional[str] = Form(None)
):
    try:
        # handling any unknown exception.

        # ############################################### Transcription #################################
        # Ensure the uploaded file is an MP3
        if file.content_type != 'audio/mpeg':
            return {"Error": "Invalid file format. Expected MPEG."}

        try:
            transcript = await get_transcription(file)
            print(transcript)
        except Exception as e:
            transcript = ""
            print("Got some exception in transcription")
            print(e)

        uid = 'oGjjFFZj0IuCpSZmOT1Y'
        category = 0

        categories_list = ['generals', 'aws', 'order', 'prime', 'refund', 'retailer']
        category = categories_list[category]
        print("Extracted audio link")
        print(transcript)


#       ######################################## OLD Transcription #################################

        # file_name = str(random.randint(1000, 9999))
        #
        # transcribe_client = boto3.client(
        #     'transcribe',
        #     region_name='us-east-1',
        #     aws_access_key_id=os.environ.get("ACCESS_KEY"),
        #     aws_secret_access_key=os.environ.get("SECRET_ACCESS_KEY"),
        # )
        #
        # transcript = transcribe_file(job_name=file_name, file_uri=audio_link, transcribe_client=transcribe_client)
        #
        # if transcript == "":
        #     return {"Error": "Error in Transcription"}
        #
        # transcript = "can you repeat the step you told me about the scaling in EC2 in AWS?"


#       ###################################### Sentiment Analysis ################################

        # Performing Sentiment analysis of the whole transcript using GoEmotion.
        # sentiment = "relaxed"
        sentiment = get_sentiment(transcript)
        print(f"Sentiment: {sentiment}")


#       ########################################## Embeddings #####################################

        # Creating Embeddings of the transcript using OpenAI.
        user_query_embeddings = get_embeddings(transcript)
        if not user_query_embeddings:
            return {"Error": "Error in getting transcription embeddings"}

        print(f"Embeddings = {user_query_embeddings[0:3]}")


#       ########################################### Firebase ######################################

        try:
            cred = credentials.Certificate("vcs-hackon-firebase.json")
            firebase_admin.initialize_app(cred)
            db = firestore.client()
            doc_ref = db.collection("Queries").document(uid)
            print(f"Firebase of {uid} Exists")

        except Exception as e:
            print(f"Firebase of {uid} does not Exists, Exception is : {e}")
            return {"Error": "Error in initializing firebase"}

        # Getting the previous query data and finding the top similar vectors.
        previous_similar_queries, previous_similar_response, previous_similar_sentiments, embeddings_query_and_previous = get_previous_query_data(
            doc_ref=doc_ref, uid=uid, category=category, user_query_vector=user_query_embeddings)

        print(f"Previous Queries + User Query : {embeddings_query_and_previous[0:3]}")


#       ########################################### Service DB #####################################

        # Calculate the similarity between combined query and service database and get responses.
        service_database_answers = get_services_response(embeddings_query_and_previous)


#       ########################################### LLM (OpenAI) ####################################

        # Pass the previous query data, the sentiment, the user query and the service database answers to the OpenAI.
        response_llm = get_response_from_llm(user_query=transcript, sentiment=sentiment,
                                             previous_queries=previous_similar_queries,
                                             previous_responses=previous_similar_response,
                                             previous_sentiments=previous_similar_sentiments,
                                             service_database_answers=service_database_answers)
        if response_llm == "":
            return {"Error": "Error in getting response from LLM"}

        print(f"Response from LLM : {response_llm[0:20]}")


#       ###################################### Update DataBase ######################################

        # Processing the audio link for saving the speech by Amazon polly.
        update_session(db=db, uid=uid, category=category, new_embedding=user_query_embeddings, new_query=transcript,
                       new_response=response_llm, new_sentiment=sentiment)
        print("Session Updated")


#       ########################################### Polly ############################################

        polly_obj = boto3.client(
            'polly',
            region_name='us-east-1',
            aws_access_key_id=os.environ.get("ACCESS_KEY"),
            aws_secret_access_key=os.environ.get("SECRET_ACCESS_KEY"),
        )

        audio_stream = get_speech(text=response_llm, polly=polly_obj)

        return StreamingResponse(audio_stream, media_type="audio/mpeg",
                                 headers={"Content-Disposition": "attachment; filename=speech.mp3"})

    except Exception as e:
        return {"Error": f"Some Exception occurred, Details are : {e}"}


@app.get("/")
def read_root():
    return {"Info": "Enter '/get_response' to get correct response"}


# if __name__ == "__main__":
    #     print(f"Region is : {os.environ.get('REGION')}")
    #     port = int(os.environ.get("PORT", 8000))
    #     print(f"Starting server on port {port}")
    # uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)
