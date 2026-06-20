import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

models = []

for m in genai.list_models():
    models.append(m.name)

for model_name in models:
    try:
        model = genai.GenerativeModel(model_name)

        response = model.generate_content(
            "Reply with OK"
        )

        print(f"{model_name}: AVAILABLE")

    except ResourceExhausted:
        print(f"{model_name}: QUOTA EXCEEDED")

    except Exception as e:
        print(f"{model_name}: ERROR -> {e}")