import google.generativeai as genai
from ..config.index import settings


def configure_gemini():
    genai.configure(api_key=settings.API_KEY)
    return genai
