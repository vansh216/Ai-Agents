import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.getenv("GAMINI_API")
if not api_key:
    raise RuntimeError("GAMINI_API is missing. Add it to your .env file as: GAMINI_API=your_key")

def get_weather(city: str) -> str:
    # Replace this with a real API call (e.g. OpenWeatherMap)
    fake_data = {"delhi": "32 degree cel", "pune": "27 degree cel"}
    return fake_data.get(city.lower(), "Weather data not available")

available_tools = {
    "get_weather": get_weather
}

client = genai.Client(api_key=api_key)

system_inst = """
You are a helpful AI assistant who specializes in resolving the user's query.
You work in start, plan, action, observe, output steps.

Rules:
- Follow the Output JSON Format strictly.
- Always perform ONE step at a time and wait for the next input.
- Carefully analyze the user query before planning.
- Respond with a single valid JSON object per turn only. No extra text outside the JSON.

Output JSON format:
{"step": "plan" | "action" | "observe" | "output", "content": "string", "function": "string (only if step is action)", "input": "string (only if step is action)"}

Available tools:
- get_weather(city: str): returns the current weather for a given city name

Example:
User Query: What is the weather of Delhi?
Output: {"step": "plan", "content": "The user wants to know the weather of Delhi"}
Output: {"step": "plan", "content": "I will call get_weather to fetch this"}
Output: {"step": "action", "function": "get_weather", "input": "delhi"}
Output: {"step": "observe", "content": "12 degree cel"}
Output: {"step": "output", "content": "The weather of Delhi is 12 degree celsius"}
"""

# THIS is the line that was missing in every version you pasted
chat = client.chats.create(
    model='gemini-3.6-flash',   # verify the real/current model id in Google's docs
    config=types.GenerateContentConfig(
        system_instruction=system_inst,
        temperature=0,
    ),
)

user_query = input("You: ")
message_to_send = user_query

max_iterations = 10
iteration = 0

while iteration < max_iterations:
    iteration += 1
    response = chat.send_message(message_to_send)
    raw_text = response.text.strip()

    try:
        parsed = json.loads(raw_text)
    except json.JSONDecodeError:
        print("Model did not return valid JSON:", raw_text)
        break

    step = parsed.get("step")

    if step == "plan":
        print(f"🧠 Plan: {parsed['content']}")
        message_to_send = "continue"

    elif step == "action":
        func_name = parsed.get("function")
        func_input = parsed.get("input")
        print(f"⚙️  Action: calling {func_name}({func_input})")

        if func_name in available_tools:
            result = available_tools[func_name](func_input)
        else:
            result = f"Error: unknown tool {func_name}"

        observation = json.dumps({"step": "observe", "content": result})
        message_to_send = observation

    elif step == "observe":
        print(f"👀 Observed: {parsed['content']}")
        message_to_send = "continue"

    elif step == "output":
        print(f"✅ Final Answer: {parsed['content']}")
        break

    else:
        print("Unknown step:", parsed)
        break
else:
    print("⚠️ Max iterations reached without a final output.")