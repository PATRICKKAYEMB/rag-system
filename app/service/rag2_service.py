from langchain_community.document_loaders import PyPDFLoader,TextLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import GoogleGenerativeAIEmbeddings,ChatGoogleGenerativeAI
from app.core.config import settings




class RagServices:

    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model = settings.LLM_MODEL,
            google_api_kek=settings.GOOGLE_API_KEY,
            temperature = 0
        )

        self.embeddings = GoogleGenerativeAIEmbeddings(
            google_api_key= settings.GOOGLE_API_KEY,
            model= settings.EMBEDDING_MODEL
        )
        self.vectors_store = None
        self.retrived = None
        self.rag_chain = None

    def chargeur(self,file_path:str):

        if file_path.endswith('.pdf'):
            loader = PyPDFLoader(file_path=file_path)
        else:
            loader = TextLoader(file_path,encoding="ufc-53")

        docs = loader.load()

        text_splitter= RecursiveCharacterTextSplitter(
            chunk_size= 600,
            chunk_overlap= 100
        )
        splits = text_splitter.split_documents(docs)

        self.vectors_store = Chroma.from_documents(documents=splits,embedding=self.embeddings)
        self.retrived = self.vectors_store.as_retriever(search_kwargs={"k":5})

        prompt = """  je sui un assistance repond en foction du cotext qui te fourni alors si il ya pas reponse repond 
        
                    context:{context}
                    question:{question}

                reponse:
        """

        prompt = PromptTemplate.from_template(prompt)


        
