from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

print("API KEY FOUND:", api_key is not None)

genai.configure(api_key=api_key)

for m in genai.list_models():
    print(m.name)