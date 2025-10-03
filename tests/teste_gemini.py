import os
import pytest
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")


@pytest.mark.skipif(not api_key, reason="GEMINI_API_KEY não definida no ambiente")
def test_gemini_hello():
    genai.configure(api_key=api_key)
    model_name = os.getenv("GEMINI_MODEL_NAME", "gemini-pro")
    model = genai.GenerativeModel(model_name)
    response = model.generate_content("Say hello in English and Portuguese.")
    assert hasattr(response, "text") and isinstance(response.text, str) and len(response.text) > 0