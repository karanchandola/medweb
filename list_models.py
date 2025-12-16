import google.generativeai as genai
import os

api_key = 'AIzaSyDbXM921PliKZ-U0d1Jf-e1wWPT5TgOq5c'
genai.configure(api_key=api_key)

print("Listing available models...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
except Exception as e:
    print(f"Error: {e}")
