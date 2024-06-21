import uvicorn
from polly import get_speech
from openAISentiment import sentiment_and_emotion_analysis
from firebaseSessionData import get_previous_query_and_response
from llmResponse import get_response_from_llm
from pinecone.grpc import PineconeGRPC as Pinecone
from pineconeDB import query_pinecone
from dotenv import load_dotenv
import boto3
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from transcriptionWhisper import get_transcription
from typing import Optional
from fastapi import FastAPI, File, UploadFile, Form
from chromaDB import get_top_k_results
from updateFirebase import update_session
from openAISentiment import get_emotion_and_sentiment
import os

app = FastAPI()
load_dotenv()

cred = credentials.Certificate("vcs-hackon-firebase.json")

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

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
        uid: Optional[str] = Form(None),
        language: Optional[str] = Form(None),
        sessionId: Optional[str] = Form(None),
):
    try:
        # handling any unknown exception.
        categories_list = ['aws', 'aws', 'retail', 'refund', 'buyer', 'prime']
        category = categories_list[category]
        print("Selected Category is : ", category)
        print("Session ID : ", sessionId)
        print("User ID : ", uid)
        print("Language : ", language)

        language_dict = {
            'English': 'Danielle',
            'Hindi': 'Aditi',
            'Spanish': 'Mia',
            'French': 'Mathieu',
            'German': 'Hans',
            'Chinese': 'Zhiyu',
            'Japanese': 'Mizuki',
            'Russian': 'Tatyana',
            'Portuguese': 'Christiano',
            'Italian': 'Bianca',
            'Korean': 'Seoyeon',
            'Arabic': 'Zeina',
            'Turkish': 'Filiz',
            'Dutch': 'Lotte',
            'Swedish': 'Astrid',
            'Polish': 'Ewa',
        }
        voice_id = 'Joanna'
        if language in language_dict:
            voice_id = language_dict[language]


#       ######################################## Transcription ###################################

        # Ensure the uploaded file is an MP3
        if file.content_type != 'audio/mpeg':
            return {"Error": "Invalid file format. Expected MPEG."}

        try:
            transcript = await get_transcription(file)
            if not transcript:
                return {"Error": "No transcription found"}
            print(f"Transcription: {transcript}")
        except Exception as e:
            print("Got some exception in transcription", e)
            return {"Error": "Some Error in transcription "}


#       ###################################### Sentiment Analysis ################################

        # Performing Sentiment analysis of the whole transcript using OpenAI.
        sentiment_text = sentiment_and_emotion_analysis(transcript)
        sentiment, emotions = get_emotion_and_sentiment(sentiment_text)
        print(f"Sentiment: {sentiment_text}")
        print(f"Emotions: {emotions}")


#       ########################################### Firebase ######################################

        try:
            db = firestore.client()
            doc_ref = db.collection("sessions").document(sessionId)
            print(f"Firebase of {sessionId} Exists")

        except Exception as e:
            print(f"Firebase of {sessionId} does not Exists, Exception is : {e}")
            return {"Error": "Error in initializing Firebase"}

        # Getting the previous query data and finding the top similar vectors.
        previous_queries, previous_responses = get_previous_query_and_response(doc_ref=doc_ref)
        # print(f"Previous Queries are : {len(previous_queries)}")
        # print(f"Previous Responses are : {len(previous_responses)}")


#       ####################### Get Top Previous Responses and Queries #############################

        top_queries = []
        top_responses = []
        if previous_queries and previous_responses:
            top_queries = get_top_k_results(itemList=previous_queries,
                                            k=4,
                                            user_query=transcript)
            top_responses = get_top_k_results(itemList=previous_responses,
                                              k=4,
                                              user_query=transcript)
        # print(f"Top Queries are : {len(top_queries)}")
        # print(f"Top Responses are : {len(top_responses)}")


#       ########################################### Service DB #####################################

        # Calculate the similarity between combined query and service database and get responses.
        pinecone_api_key = os.environ.get('PINECONE_API_KEY')
        pc = Pinecone(api_key=pinecone_api_key)

        index_name = os.environ.get('PINECONE_INDEX_NAME')
        index = pc.Index(index_name)
        service_queries, service_responses = query_pinecone(index_=index,
                                                            user_query=transcript,
                                                            namespace_pine=category)

        # print(f"Service Database Questions are : {len(service_queries)}")
        # print(f"Service Database Answers are : {len(service_responses)}")


#       ########################################### LLM (OpenAI) ####################################

        # Pass the previous query data, the sentiment, the user query and the service database answers to the OpenAI.
        response_llm = get_response_from_llm(user_query=transcript, sentiment=sentiment_text,
                                             emotions=emotions,
                                             previous_queries=top_queries,
                                             previous_responses=top_responses,
                                             service_database_questions=service_queries,
                                             service_database_answers=service_responses,
                                             language=language)

        if response_llm == "":
            return {"Error": "Error in getting response from LLM"}

        print(f"Response from LLM : {response_llm}")


#       ###################################### Update DataBase ######################################

        # Processing the audio link for saving the speech by Amazon polly.
        update_session(db=db,
                       sessionId=sessionId,
                       new_query=transcript,
                       new_response=response_llm,
                       new_sentiment=sentiment)

        print("Session Updated")


#       ########################################### Polly ############################################

        polly_obj = boto3.client(
            'polly',
            region_name='us-east-1',
            aws_access_key_id=os.environ.get("ACCESS_KEY"),
            aws_secret_access_key=os.environ.get("SECRET_ACCESS_KEY"),
        )

        try:
            audio_stream = get_speech(text=response_llm,
                                      polly=polly_obj,
                                      voice_id=voice_id)

        except:
            audio_stream = get_speech(text=response_llm,
                                      polly=polly_obj,
                                      voice_id='Joanna')

        return StreamingResponse(audio_stream, media_type="audio/mpeg",
                                 headers={"Content-Disposition": "attachment; filename=speech.mp3"})

    except Exception as e:
        return {"Error": f"Some Exception occurred, Details are : {e}"}


@app.get("/")
def read_root():
    return {"Info": "Enter '/get_response' to get correct response"}


if __name__ == "__main__":
        # print(f"Region is : {os.environ.get('REGION')}")
        # port = int(os.environ.get("PORT", 8000))
        # print(f"Starting server on port {port}")
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)