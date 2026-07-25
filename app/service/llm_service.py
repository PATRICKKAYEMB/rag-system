from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import settings


class LLMServices:

    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model= settings.GEMINI_MODEL,
            google_api_key= settings.GOOGLE_API_KEY,
            temperature=0
        )

    async def generate_response(self,prompt:str)->str:
        response= await self.llm.ainvoke(prompt)
        return response.content

llm_service = LLMServices()