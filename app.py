import os
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

app = Flask(__name__)

# Configure Gemini API key
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Initialize the Gemini model
model = genai.GenerativeModel("gemini-pro")

# Start a persistent chat session with a system prompt
chat_session = model.start_chat(history=[
    {"role": "user", "parts": ["You are Elara, a helpful and intelligent AI assistant. Answer clearly, kindly, and accurately."]}
])

@app.route("/")
def home():
    return render_template("index.html")  # Make sure index.html is in the 'templates' folder

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")

    if not user_input:
        return jsonify({"response": "Please enter a message."}), 400

    try:
        response = chat_session.send_message(user_input)
        reply = response.text.strip()

        # Fallback if Gemini returns a vague or empty response
        if not reply or "I'm not sure" in reply:
            reply = "I'm still learning! Could you try rephrasing that?"

    except Exception as e:
        reply = f"Oops! Something went wrong: {str(e)}"

    return jsonify({"response": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
