import os
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.core.config import settings


class SimpleRAGServices:

    def __init__(self):
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=settings.EMBEDDING_MODEL,
            google_api_key=settings.GOOGLE_API_KEY
        )

        self.llm = ChatGoogleGenerativeAI(
            model=settings.LLM_MODEL,
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0
        )

        self.vector_store = None
        self.retriever = None
        self.rag_chain = None

    def ingest_document(self, file_path: str):
        """Charger le document, le découper et l'enregistrer dans ChromaDB"""

        if file_path.endswith('.pdf'):
            loader = PyPDFLoader(file_path)
        else:
            loader = TextLoader(file_path, encoding="utf-8")

        docs = loader.load()

        # Découpage du texte en blocs (chunks)
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100
        )
        splits = text_splitter.split_documents(docs)

        # 1. FIX : On passe 'splits' et non 'docs' pour profiter du découpage
        self.vector_store = Chroma.from_documents(documents=splits, embedding=self.embeddings)
        self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})

        prompt_template = """Tu es un assistant strict. Réponds à la question en t'appuyant uniquement sur le contexte fourni ci-dessous.
Si la réponse ne se trouve pas dans le contexte, dis simplement : "Je ne trouve pas ces informations dans le document."

Contexte :
{context}

Question :
{question}

Réponse :"""

        prompt = ChatPromptTemplate.from_template(prompt_template)

        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        # 2. FIX : Utilisation de lambdas propres pour extraire la question du dictionnaire
        self.rag_chain = (
            {
                "context": (lambda x: x["question"]) | self.retriever | format_docs,
                "question": lambda x: x["question"]
            }
            | prompt
            | self.llm
            | StrOutputParser()
        )

    def ask(self, question: str) -> str:
        if not self.rag_chain:
            return "Aucun document n'a encore été chargé dans le système RAG"

        # 3. FIX : On passe un dictionnaire avec la clé "question"
        return self.rag_chain.invoke({"question": question})


rag_service = SimpleRAGServices()