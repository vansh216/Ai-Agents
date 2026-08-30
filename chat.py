import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.getenv("GAMINI_API")
if not api_key:
    raise RuntimeError("GAMINI_API is missing. Add it to your .env file as: GAMINI_API=your_key")

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model='gemini-3.6-flash',
    contents=[
        types.Content(
            role='user',
            parts=[types.Part.from_text(text='is my friend is good')],
        )
    ],
    config=types.GenerateContentConfig(
        system_instruction=(
            "you are a strict math assistance. "
            "do not reply to other messages that are not related to math and its operations. "
            "show the calculation step by step. "
            "example: {{msg: what is 3*5 answer: it is a mathematical operation of multiplication}} "
            "example: {{msg: is sky blue answer: I am only a math operations assistant}}"
        ),
        temperature=0,
        top_p=0.95,
        top_k=20,
    ),
)
print(response.text)