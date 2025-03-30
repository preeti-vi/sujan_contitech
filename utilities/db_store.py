from langchain_openai import OpenAIEmbeddings


__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import sqlite3
from langchain_chroma import Chroma

def get_vector_store():
    # Store in vector DB
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    vector_store = Chroma(
        collection_name="example_collection",
        embedding_function=embeddings,
        persist_directory="./chroma_langchain_db",  # Where to save data locally, remove if not necessary
    )

    return vector_store


def store_in_db(chunks):
    vector_store = get_vector_store()
    vector_store.add_texts(chunks)


def query_db(user_query):
    vector_store = get_vector_store()
    retriever = vector_store.as_retriever(
        search_type="similarity", search_kwargs={"k": 2}
    )
    response = retriever.invoke(user_query)

    for i, doc in enumerate(response):
        print(f"\nDoc : {i + 1}\n")
        print(doc.page_content)

    return response