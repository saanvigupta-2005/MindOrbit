import os
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Configure Gemini API key from environment variable
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Load the Gemini model
model = genai.GenerativeModel("gemini-pro")

@app.route("/")
def home():
    return "Elara is live!"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message")

    if not user_input:
        return jsonify({"response": "Please send a message."}), 400

    try:
        response = model.generate_content(user_input)
        reply = response.text.strip()
    except Exception as e:
        reply = f"Oops! Something went wrong: {str(e)}"

    return jsonify({"response": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
