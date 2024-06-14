import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

uid = 'oGjjFFZj0IuCpSZmOT1Y'

cred = credentials.Certificate("vcs-hackon-firebase.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


category = 1


doc_ref = db.collection("Queries").document(uid)

def get_all_embeddings(uid, category):
    categories_list = ['generals', 'aws', 'order', 'prime', 'refund', 'retailer']
    embedding_list = []
    doc_ref = db.collection("Queries").document(uid)
    if category == 0:
        for i in categories_list:
            if doc_ref.get().exists:
                embedding_list += doc_ref.get().to_dict()[i]['embeddings']
            else:
                print("Document does not exist")
                embedding_list = []
            return embedding_list
    else:
        if doc_ref.get().exists:
            embedding_list = doc_ref.get().to_dict()[categories_list[category]]['embeddings']

        else:
            print("Document does not exist")
            embedding_list = []

    return embedding_list


def find_top_similar_vectors(query_vector, other_vectors, top_n=3):
    # Here i need to keep track of index at any cost.
    # Convert vectors to numpy arrays if not already
    query_vector = np.array(query_vector).reshape(1, -1)  # Reshape to row vector
    other_vectors = np.array(other_vectors)

    # Compute cosine similarities
    similarities = cosine_similarity(query_vector, other_vectors)

    # Get indices of top n similar vectors (excluding the query vector itself)
    top_indices = similarities.argsort()[0][-top_n - 1:-1][::-1]

    # Return the top n similar vectors and their cosine similarities
    top_vectors = other_vectors[top_indices]
    top_similarities = similarities[0][top_indices]

    return top_vectors, top_similarities


# Data to append
new_embeddings = ["e11", "e12"]
new_queries = ["5q", "6q"]
new_responses = ["r5", "r6"]
new_sentiments = ["s5", "s6"]


# Function to append data to an array field in Firestore
def update_query_document(doc_ref, field_path, new_embeddings):
    field_initial = field_path.split(".")[0]
    field_second = field_path.split(".")[1]
    if doc_ref.get().exists:
        l1 = doc_ref.get().to_dict()[field_initial][field_second]
        l1 = l1 + new_embeddings
        doc_ref.update({field_path: l1})
    else:
        print("Document does not exist")

def get_previous_query_data(uid, category, user_query_vector):
    previous_embeddings = get_all_embeddings(uid=uid, category=category)
    top_vectors, top_similarity = find_top_similar_vectors(query_vector=user_query_vector, other_vectors=previous_embeddings, top_n=3)
    # Create embeddings using the current and previous one, call the pooling layer code over here also.

    return top_vectors





update_query_document(doc_ref, "aws.embeddings", new_embeddings)
# append_data_to_array_field(doc_ref, "aws.embeddings", new_embeddings)
# append_data_to_array_field(doc_ref, "aws.queries", new_queries)
# append_data_to_array_field(doc_ref, "aws.responses", new_responses)
# append_data_to_array_field(doc_ref, "aws.sentiments", new_sentiments)
# print("Data appended successfully.")



# Write the data to firestore, by providing the correct path
# doc_ref = db.collection("Users").document("alovelace")
# doc_ref.set({"contactNumber": "9999998888", "country": "India", "email": "anupam@gmail.com", "firstName": "a", "lastName": "m", "password": "123456", "state": "up"})
#
# # Read the data from firestore, by providing the correct path
# users_ref = db.collection("Users")
# docs = users_ref.stream()
#
# for doc in docs:
#     print(f"{doc.id} => {doc.to_dict()}")
