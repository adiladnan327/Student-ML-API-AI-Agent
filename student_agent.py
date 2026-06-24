import re
import requests

API_URL = "http://127.0.0.1:8000/predict"

def extract_hours(user_message: str):
    patterns = [
        r"(\d+(\.\d+)?)\s*(hours|hour|hrs|hr)",
        r"studied\s+(\d+(\.\d+)?)"
    ]

    for pattern in patterns:
        match = re.search(pattern, user_message.lower())
        if match:
            return float(match.group(1))

    return None

def call_prediction_api(hours: float):
    response = requests.get(API_URL, params={"hours": hours}, timeout=10)

    if response.status_code != 200:
        return {
            "success": False,
            "error": response.json()
        }

    return {
        "success": True,
        "data": response.json()
    }

def explain_prediction(hours: float, predicted_score: float):
    if predicted_score >= 80:
        advice = "This looks strong. The student is likely doing well."
    elif predicted_score >= 60:
        advice = "This is a decent score, but there is room to improve."
    elif predicted_score >= 40:
        advice = "The student may need more preparation and practice."
    else:
        advice = "The student is at risk and should increase study time."

    return (
        f"Based on {hours} study hours, the ML model predicts a score of "
        f"around {predicted_score}.\n\n"
        f"Recommendation: {advice}"
    )

def agent_response(user_message: str):
    print("\nScripted Agent thinking...")
    print("1. Reading your question")

    hours = extract_hours(user_message)

    if hours is None:
        return (
            "I could not find study hours in your question.\n"
            "Please ask something like: My son studied 5 hours. What score can he get?"
        )

    print(f"2. Extracted study hours: {hours}")
    print("3. Calling the ML prediction API")

    api_result = call_prediction_api(hours)

    if not api_result["success"]:
        return f"The API returned an error: {api_result['error']}"

    prediction_data = api_result["data"]
    predicted_score = prediction_data["predicted_score"]

    print("4. Received prediction from API")
    print("5. Preparing human-friendly answer")

    return explain_prediction(hours, predicted_score)

if __name__ == "__main__":
    print("Scripted Student Advisor Agent")
    print("Type: My son studied 5 hours. How much score can he get?")
    print("Type 'exit' to stop.\n")

    while True:
        user_message = input("You: ")

        if user_message.lower() in ["exit", "quit"]:
            print("Agent: Goodbye!")
            break

        answer = agent_response(user_message)
        print(f"\nAgent: {answer}\n")
