import os
from dotenv import load_dotenv
from google import genai

types=genai.types

load_dotenv()
api_key= os.getenv("GAMINI_API")

client=genai.Client(api_key=api_key)

response = client.models.generate_content(
    model='gemini-3.6-flash',
    contents=[
        types.Content(
            role='user',
            parts=[types.Part.from_text(text="hii kya ho rha hi")],
            

        )
    ],
    config=types.GenerateContentConfig(
        system_instruction=(
            "You are the model selector, choose the  best model according to the work"
            "You only select the models that you have given do not select any other model"
            "you have models: " 
            "cloude: for the deep coding project and full stack project"
            "chatGPT: for the text reply and simple work like email draft, chating"
            "KIMI: It is for the only frontend deign work and make it"
            "Gamini: It is use for the webseaching and other types of work"
            "Example: msg: hii whatapp : chatGPT"
            "Example: msg: create the frontend website: KIMI"
            "Example: msg: create the full stack project : cloude"
            )
    )
)

print(response.text)