from pinecone.grpc import PineconeGRPC as Pinecone
from dotenv import load_dotenv
import os
from openAi import get_embeddings
import uuid


def delete_rule(index, vector_id):
    index.delete(ids=[vector_id], namespace='aws')


def initialise_pinecone():
    load_dotenv()
    pinecone_api_key = os.environ.get('PINECONE_API_KEY')
    pc = Pinecone(api_key=pinecone_api_key)

    index_name = os.environ.get('PINECONE_INDEX_NAME')
    index_ = pc.Index(index_name)
    return index_


def insert_data(index_, queries, responses, namespace_pine):
    vectors_to_insert = [
        {
            "id": str(uuid.uuid4()),  # Generate a unique ID for each vector
            "values": get_embeddings(queries[i]),
            "metadata": {"queries": queries[i], "response": responses[i]}
        }
        for i in range(len(queries))
    ]
    index_.upsert(namespace=namespace_pine, vectors=vectors_to_insert)

    print(index_.describe_index_stats())


def query_pinecone(index_, user_query, namespace_pine):
    query_vector = get_embeddings(user_query)

    query_results = index_.query(
        namespace=namespace_pine,
        vector=query_vector,
        top_k=4,
        include_values=False,
        include_distance=True,
        include_metadata=True,
    )

    queries = []
    responses = []

    matches = query_results['matches']
    for match in matches:
        if match['score'] > 0.7:
            responses.append(match['metadata']['response'])
            queries.append(match['metadata']['queries'])
    return queries, responses


# index = initialise_pinecone()
# insert_data(index, prime_queries, prime_responses, 'prime')

# query = "tell me about ec2 auto scaling and how it works?"
# queries_, response = query_pinecone(index, query, 'aws')
# print(queries_, response)
# vector_id = 'aa7fe3a5-e0b4-4e39-812f-dac1a6c62939'
# 6e0d4ac6-799f-4c58-9967-a16817e5e9c9
# delete_rule(index, vector_id)
