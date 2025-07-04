from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os
from dotenv import load_dotenv
import markdown  # ✅ Import markdown converter

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure Gemini API key
genai.configure(api_key=os.getenv("gemini"))

# Load the Gemini 1.5 Flash model
model = genai.GenerativeModel("models/gemini-1.5-flash")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "").strip()

    if not user_input:
        return jsonify({"reply": "Please enter a message."})

    try:
        # Prompt Elara to respond in structured Markdown
        prompt = (
            "You are Elara, a helpful and intelligent AI assistant. "
            "Respond in clear, structured Markdown format using bullet points, bold text, and line breaks where appropriate.\n\n"
            f"User: {user_input}\nElara:"
        )

        response = model.generate_content([prompt])
        raw_reply = response.text.strip()

        # ✅ Convert Markdown to HTML
        html_reply = markdown.markdown(raw_reply)

        return jsonify({"reply": html_reply})

    except Exception as e:
        print("Error:", e)
        return jsonify({"reply": "⚠️ Error processing request."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
