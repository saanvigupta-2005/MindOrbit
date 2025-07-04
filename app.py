import os
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

app = Flask(__name__)

# Configure Gemini API key
genai.configure(api_key=os.environ.get("gemini"))

# Load the Gemini model
model = genai.GenerativeModel("gemini-pro")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")

    if not user_input:
        return jsonify({"response": "Please enter a message."}), 400

    try:
        # Gemini expects a list of parts, not just a string
        response = model.generate_content([user_input])
        reply = response.text.strip()

        if not reply or "I'm not sure" in reply:
            reply = "I'm still learning! Could you try rephrasing that?"

    except Exception as e:
        reply = f"Oops! Something went wrong: {str(e)}"

    return jsonify({"response": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
