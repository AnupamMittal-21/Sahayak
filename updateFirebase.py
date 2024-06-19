import logging

# Configure logging
logging.basicConfig(level=logging.ERROR)  # Set the logging level according to your needs


def update_query_document(doc_ref, field_name, new_data):
    try:
        doc_snapshot = doc_ref.get()
        if doc_snapshot.exists:
            data = doc_snapshot.to_dict()
            if field_name in data:
                current_data = data[field_name]
                if current_data is not None and isinstance(current_data, list):
                    updated_data = current_data + [new_data]
                else:
                    updated_data = [new_data]
            else:
                updated_data = [new_data]

            doc_ref.update({field_name: updated_data})
        else:
            logging.error(f"Document '{doc_ref.id}' does not exist")
            raise RuntimeError(f"Document Snapshot does not exists")

    except Exception as e:
        raise RuntimeError(f"Error in updating query document on Firestore: {e}")


def update_session(db, sessionId, new_query, new_response, new_sentiment):
    try:
        doc_ref = db.collection("sessions").document(sessionId)
        update_query_document(doc_ref=doc_ref, field_name="questions", new_data=new_query)
        update_query_document(doc_ref=doc_ref, field_name="answers", new_data=new_response)
        update_query_document(doc_ref=doc_ref, field_name="embeddings", new_data=new_sentiment)

    except Exception as e:
        raise RuntimeError(f"Error in updating session on Firestore: {e}")
