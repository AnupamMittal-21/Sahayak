from dotenv import load_dotenv
import os
import requests
import json

from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

# text = """API Documentation
# API Documentation is very essential and it helps in effective interaction. Here, we are using NewsAPI that provides us the information regarding various news of various countries and celebrities. To get news updates from NewsAPI, we need a special key called an API key. Think of it as a digital passcode that lets us access their news database. We’ve stored this key in a place called API_KEY.
#
# Next, we’ve built a specific web address (or URL) that tells NewsAPI exactly what kind of news we want – in this case, top business headlines from the United States. It’s like telling a librarian you’re interested in the business section of a newspaper from a particular city.
#
# After setting up this request, our code then sends a message to NewsAPI using this URL. It’s similar to clicking on a link to see a webpage. Once we send this message, NewsAPI replies with a status update. This status tells us if our request was successful or if there was any problem. We then simply print out this status to see if everything worked as expected.
#
# import requests
# # Replace 'API_KEY' with your actual API key from NewsAPI
# API_KEY = '3805f6bbabcb42b3a0c08a489baf603d'
# url = f"https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey={API_KEY}"
# response = requests.get(url)
# print(response.status_code)
# Output
#
# 200
#
# A successful request yields a ‘200’ status code, signifying success. The documentation also mentions that the API response comes in JSON format. Now, we will use response.json() method to get complete output in next section (Using API with Query).
#
# Working with JSON Data
# While working with APIs, it is very essential to know how to work with JSON data. Json universally works as the language of APIs that helps in providing a way to encode the data structures in a format that is easily interpreted by machines. Imagine browsing a news website. The data we see there—headlines, descriptions, images—is often structured in a format called JSON. It’s like the universal language that APIs speak.
#
# Now, to make sense of this digital jigsaw puzzle, we’ve written a Python script. This script acts like a digital news curator: it reaches out to NewsAPI using a library called requests and fetches the latest business headlines from the US. Once it has this data, Python steps in, sorting and presenting it in a neat list. Think of it as a friendly librarian picking out the top three articles for us from a vast collection. This whole process not only gives us a glimpse into how APIs and JSON work hand in hand but also underscores the magic Python brings to the table in managing such tasks effortlessly.
#
# """
# print(len(text))
# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size=1000,
#     chunk_overlap=200,
#     length_function=len
# )
# chunks = text_splitter.split_text(text=text)
#
# print(type(chunks))
# print(chunks)
# print(len(chunks))
#
# for i in chunks:
#     print(len(i))
#     print(i)



def get_embeddings(text):

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

# def get_response_from_llm(user_query, sentiment, previous_queries, previous_responses, service_database_answers):
#
# #
# a = get_embeddings("how can i achieve scaling in EC2 in aws?")
# print(a)
