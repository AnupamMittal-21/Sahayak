import streamlit as st
from dotenv import load_dotenv
import pickle
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback
import os

load_dotenv()

st.title("Ask Questions from PDF 📃")
def main():
    df = st.file_uploader("Upload your PDF", type='pdf')

    if df is not None:
        pdf_reader = PdfReader(df)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(text=text)

        store_name = df.name[:-4]
        st.write(f'{store_name}')

        if os.path.exists(f"{store_name}.index"):
            VectorStore = FAISS.load_local(store_name)
            st.write('Embeddings Loaded from Disk')
        else:
            embeddings = OpenAIEmbeddings()
            print(type(embeddings))
            print(embeddings)
            VectorStore = FAISS.from_texts(chunks, embedding=embeddings)
            VectorStore.save_local(store_name)

        # query = st.text_input("Ask questions about your PDF file:")
        #
        # if query:
        #     docs = VectorStore.similarity_search(query=query, k=3)
        #
        #     llm = OpenAI()
        #     chain = load_qa_chain(llm=llm, chain_type="stuff")
        #     with get_openai_callback() as cb:
        #         response = chain.run(input_documents=docs, question=query)
        #         print(cb)
        #     st.write(response)

if __name__ == "__main__":
    main()