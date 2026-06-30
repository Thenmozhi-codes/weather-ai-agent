import os
import json
from groq import Groq
from tools import get_coordinates, get_weather, get_forecast
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

conversation_history = []

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_coordinates",
            "description": "Convert a city name to latitude and longitude coordinates",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "Name of the city e.g. Chennai, Tokyo"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather using latitude and longitude",
            "parameters": {
                "type": "object",
                "properties": {
                    "latitude": {"type": "number"},
                    "longitude": {"type": "number"}
                },
                "required": ["latitude", "longitude"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_forecast",
            "description": "Get 5-day weather forecast using latitude and longitude",
            "parameters": {
                "type": "object",
                "properties": {
                    "latitude": {"type": "number"},
                    "longitude": {"type": "number"}
                },
                "required": ["latitude", "longitude"]
            }
        }
    }
]

tool_map = {
    "get_coordinates": lambda args: get_coordinates(**args),
    "get_weather": lambda args: get_weather(**args),
    "get_forecast": lambda args: get_forecast(**args)
}

def run_agent(user_query: str) -> str:
    conversation_history.append({
        "role": "user",
        "content": user_query
    })

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful weather assistant. "
                "You have access to exactly THREE tools only: "
                "1. get_coordinates - convert any city name to coordinates. "
                "2. get_weather - get current weather using lat/lon. "
                "3. get_forecast - get 5-day forecast using lat/lon. "
                "NEVER use any other tool like brave_search. "
                "Always call get_coordinates first to get lat/lon, "
                "then call get_weather or get_forecast based on the query. "
                "If the user asks about current weather, use get_weather. "
                "If the user asks about forecast, week, or upcoming days, use get_forecast. "
                "Always mention any alerts from the response."
            )
        }
    ] + conversation_history

    while True:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            tools=tools,
            tool_choice="auto",
            max_tokens=1024
        )

        message = response.choices[0].message
        finish_reason = response.choices[0].finish_reason

        if finish_reason == "tool_calls" and message.tool_calls:
            messages.append(message)

            for tool_call in message.tool_calls:
                name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)

                print(f"  → Calling tool: {name}({args})")
                result = tool_map[name](args)
                print(f"  ← Result: {result}")

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })

        elif finish_reason == "stop":
            final_reply = message.content

            conversation_history.append({
                "role": "assistant",
                "content": final_reply
            })

            return final_reply

        else:
            return "Something went wrong."


if __name__ == "__main__":
    print("🌤️  Weather Agent (with Memory + Forecast + Alerts)")
    print("Ask me anything about the weather!")
    print("Type 'clear' to reset memory, 'quit' to exit\n")

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() in ["quit", "exit", "bye"]:
            print("Agent: Goodbye! Stay weather-aware! 👋")
            break

        if user_input.lower() in ["clear", "reset", "new chat"]:
            conversation_history.clear()
            print("Agent: Memory cleared! Starting fresh. 🧹\n")
            continue

        try:
            result = run_agent(user_input)
            print(f"\nAgent: {result}\n")
        except Exception as e:
            print(f"\nAgent: Sorry, couldn't process that. Try a specific city!\n")

        print("-" * 50)