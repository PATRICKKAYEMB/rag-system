from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import GoogleGenerativeAIEmbeddings,ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.chat_history import InMemoryChatMessageHistory
from app.core.config import settings




class SimpleRagSevices:

    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model = settings.LLM_MODEL,
            google_api_key= settings.GOOGLE_API_KEY,
            temperature=0
        )

        self.embedding = GoogleGenerativeAIEmbeddings(
            model= settings.EMBEDDING_MODEL,
            google_api_key= settings.GOOGLE_API_KEY
        )
        self.persistence_directory="./chroma"
        self.vector_store= Chroma.from_documents(
            persist_directory=self.persistence_directory,
            embedding_function= self.embedding
        )
        self.retriver= self.vector_store.as_retriever(search_kwargs={"k":3})



    def ingestion_document(self,file_path:str):
        if file_path.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        else:
            return "format non prise en charge"

        docs= loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100
        )

        splits = splitter.split_documents(docs)

        self.vector_store = Chroma.from_documents(
            embedding=self.embedding,
            persist_directory=self.persistence_directory,
            documents=splits
        )
        self.retriver = self.vector_store.as_retriever(search_kwargs={"k":3})

        