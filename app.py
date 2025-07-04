import os
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

app = Flask(__name__)

# Configure Gemini API key
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Initialize the Gemini model
model = genai.GenerativeModel("gemini-pro")

@app.route("/")
def home():
    return render_template("index.html")  # Make sure this file is in the 'templates' folder

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")

    if not user_input:
        return jsonify({"response": "Please enter a message."}), 400

    try:
        # Add a system-style prompt to guide Elara's behavior
        prompt = f"You are Elara, a friendly and intelligent AI assistant. Respond helpfully and clearly.\nUser: {user_input}"

        response = model.generate_content(prompt)
        reply = response.text.strip()

        # Fallback if Gemini returns an empty or vague response
        if not reply or "I'm not sure" in reply:
            reply = "I'm still learning! Could you try rephrasing that?"

    except Exception as e:
        reply = f"Oops! Something went wrong: {str(e)}"

    return jsonify({"response": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
