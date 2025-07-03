import os
import markdown                     
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template

API_KEY = os.getenv("gemini")             
if not API_KEY:
    raise RuntimeError("Missing ‘gemini’ env‑var (your API key)")

genai.configure(api_key=API_KEY)

MODEL_NAME = "models/gemini-1.5-flash"          
model = genai.GenerativeModel(MODEL_NAME)
chat  = model.start_chat()                       
app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat_route():
    user_text = request.json.get("message", "").strip()
    if not user_text:
        return jsonify({"error": "Empty message"}), 400

    try:
        response   = chat.send_message(user_text)

        
        html_reply = markdown.markdown(
            response.text,
            extensions=["fenced_code", "nl2br"]  
        )

        return jsonify({"reply": html_reply})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
