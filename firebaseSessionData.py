import logging

# Configure logging
logging.basicConfig(level=logging.ERROR)  # Set the logging level according to your needs


def get_current_element_list(doc_ref, path):
    try:
        doc_snapshot = doc_ref.get()
        if doc_snapshot.exists:
            data = doc_snapshot.to_dict()
            if path in data:
                return data[path]
            else:
                logging.error(f"Path '{path}' not found in document {doc_ref.id}")
        else:
            logging.error(f"Document '{doc_ref.id}' does not exist")

        return None  # Return None when document doesn't exist or path is not found

    except Exception as e:
        logging.error(f"Error in reading query document on Firestore: {e}")
        return None


def get_previous_query_and_response(doc_ref):
    try:
        previous_queries = get_current_element_list(doc_ref=doc_ref, path='questions')
        previous_responses = get_current_element_list(doc_ref=doc_ref, path='answers')
        return previous_queries, previous_responses

    except ValueError as ve:
        print(f'ValueError in get_previous_query_data: {ve}')
        return [], []

    except IndexError as ie:
        print(f'IndexError in get_previous_query_data: {ie}')
        return [], []

    except Exception as e:
        # Catch any other unexpected exceptions
        print(f'Error in get_previous_query_data: {e}')
        return [], []
