from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env (for local testing)
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure Gemini API key
genai.configure(api_key=os.getenv("gemini"))

# Load the Gemini 1.5 Flash model
model = genai.GenerativeModel("models/gemini-1.5-flash")

@app.route("/")
def index():
    return render_template("index.html")  # Ensure index.html is in the 'templates' folder

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "").strip()

    if not user_input:
        return jsonify({"reply": "Please enter a message."})

    try:
        # Prompt Elara to respond in a structured, readable format
        prompt = (
            "You are Elara, a helpful and intelligent AI assistant. "
            "When answering questions, respond in a clear, structured format using bullet points or numbered lists where appropriate. "
            "Use line breaks and formatting to make your response easy to read.\n\n"
            f"User: {user_input}\nElara:"
        )

        # Gemini expects a list of parts
        response = model.generate_content([prompt])
        reply = response.text.strip()

        # Fallback if Gemini returns a vague or empty response
        if not reply or "I'm not sure" in reply:
            reply = "I'm still learning! Could you try rephrasing that?"

        return jsonify({"reply": reply})

    except Exception as e:
        print("Error:", e)
        return jsonify({"reply": "⚠️ Error processing request."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
