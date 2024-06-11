from pymongo import MongoClient
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import MongoDBAtlasVectorSearch
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader, DirectoryLoader
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
import gradio as gr
from gradio.themes.base import Base 
import key_param


client = MongoClient(key_param.MONGO_URI)
dbName = "langchain_demo"
collectionName = "collection_of_text_blobs"
collection = client[dbName][collectionName]

# loader = DirectoryLoader("./sample_files", glob="./*.txt", show_progress=True)
# data = loader.load()

embeddings = OpenAIEmbeddings(openai_api_key=key_param.openai_api_key)

vectorStore = MongoDBAtlasVectorSearch.from_documents(data, embeddings, collection=collection)


def query_dat(query):
    docs = vectorStore.similarity_search(query, K=1)
    as_ouput = doc[0].page_content

    llm = OpenAI(openai_api_key=key_param.openai_api_key, temperature =0)
    retriever = vectorStore.as_retriever()
    qa = RetrievalQA.from_chain_type(llm, chain_type="stuff", retriever=retriever)
    retriever_output = qa.run(query)

    return as_ouput, retriever_output
    