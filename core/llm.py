import os
from langchain_google_genai import ChatGoogleGenerativeAI

def create_llm(temperature: float = 0.1, model: str = "gemini-1.5-flash") -> ChatGoogleGenerativeAI:
    """Create a configured Gemini LLM instance"""
    google_api_key = os.getenv("GOOGLE_API_KEY")
    return ChatGoogleGenerativeAI(
        model=model,
        temperature=temperature,
        google_api_key=google_api_key
    ) 