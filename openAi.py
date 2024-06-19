from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()


def get_embeddings(text):
    try:
        url = 'https://api.openai.com/v1/embeddings'

        headers = {
            'Authorization': f'Bearer {os.environ.get("OPENAI_API_KEY")}',
            'Content-Type': 'application/json',
        }

        data = {
            'input': text,
            'model': 'text-embedding-ada-002'
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        response = response.json()
        embeddings = response['data'][0]['embedding']
        return embeddings

    except Exception as e:
        print(f"Error in getting embeddings of user_query(Transcription) : {e}")
        return []
