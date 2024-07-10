from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings


def split_docs(documents, chunk_size=200, chunk_overlap=75):
    try:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        docs = text_splitter.split_text(documents)
        return docs
    except Exception as e:
        raise RuntimeError(f"Error in splitting documents: {e}")


def get_top_k_results(itemList, k, user_query):
    try:
        documents = ""
        for item in itemList:
            documents += item + ' \n '

        docs = split_docs(documents)
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        VectorStore = Chroma.from_texts(docs, embeddings)
        response_docs = VectorStore.similarity_search_with_score(query=user_query, k=k)

        filtered_documents = []
        for document, score in response_docs:
            if score > 0.7 and document.page_content not in filtered_documents:
                filtered_documents.append(document.page_content)

        return filtered_documents

    except Exception as e:
        raise RuntimeError(f"Error in getting top k results: {e}")
