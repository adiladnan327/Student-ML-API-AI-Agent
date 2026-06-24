import os
import json
import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# ====================== CONFIG ======================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in environment variables!")

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "llama-3.3-70b-versatile")  # or llama-3.1-8b-instant, mixtral-8x7b-32768 etc.
PREDICT_API_URL = os.getenv("PREDICT_API_URL", "http://127.0.0.1:8000/predict")

# Initialize client for Groq (OpenAI-compatible)
client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)
# ===================================================

def predict_student_score(hours: float) -> dict:
    """Tool that calls your FastAPI ML model."""
    try:
        response = requests.get(
            PREDICT_API_URL,
            params={"hours": hours},
            timeout=10
        )

        if response.status_code != 200:
            return {
                "success": False,
                "error": response.text
            }

        return {
            "success": True,
            "result": response.json()
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


tools = [
    {
        "type": "function",
        "function": {
            "name": "predict_student_score",
            "description": (
                "Predict a student's exam score based on study hours. "
                "Use this tool whenever the user asks about expected score, marks, "
                "performance, pass/fail chance, or study outcome based on study hours."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "hours": {
                        "type": "number",
                        "description": "Number of hours the student studied."
                    }
                },
                "required": ["hours"],
                "additionalProperties": False
            }
        }
    }
]


def ask_llm_agent(user_question: str) -> str:
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful student advisor agent. "
                "You can call the predict_student_score tool when needed. "
                "Explain the result in very simple, friendly language. "
                "Do not invent predictions yourself — always use the tool."
            )
        },
        {
            "role": "user",
            "content": user_question
        }
    ]

    print("\n🔄 LLM Agent Step 1: Sending question to Groq...")

    first_response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    assistant_message = first_response.choices[0].message
    messages.append(assistant_message)

    if not assistant_message.tool_calls:
        print("✅ LLM answered directly (no tool needed).")
        return assistant_message.content

    print("🛠️ LLM decided to call the ML prediction tool.")

    for tool_call in assistant_message.tool_calls:
        tool_name = tool_call.function.name
        tool_arguments = json.loads(tool_call.function.arguments)

        print(f"   Tool: {tool_name} | Hours: {tool_arguments.get('hours')}")

        if tool_name == "predict_student_score":
            tool_result = predict_student_score(hours=tool_arguments["hours"])
        else:
            tool_result = {"success": False, "error": f"Unknown tool: {tool_name}"}

        print(f"   API Result: {tool_result}")

        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(tool_result)
        })

    print("🔄 LLM Agent Step 2: Sending tool result back for final answer...")

    final_response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=messages
    )

    return final_response.choices[0].message.content


if __name__ == "__main__":
    print("🚀 Groq Student Advisor Agent (using Groq API)")
    print("-----------------------------------------------")
    print("Make sure:")
    print("1. Your FastAPI is running: uvicorn model_api:app --reload")
    print("2. GROQ_API_KEY is set in your .env file")
    print()
    print("Example question: 'My son studied 5 hours. What score can he expect?'")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("You: ")
        if question.lower() in ["exit", "quit", "bye"]:
            print("Agent: Goodbye! 👋")
            break

        try:
            answer = ask_llm_agent(question)
            print(f"\nAgent: {answer}\n")
        except Exception as ex:
            print(f"\n❌ Error: {ex}\n")
