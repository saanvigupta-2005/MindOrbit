from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Set your OpenAI API key from environment variable
openai.api_key = os.environ.get("gemini")

@app.route("/")
def home():
    return "Elara is live and ready to chat!"

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")

    if not user_input:
        return jsonify({"response": "Please send a message."}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use "gpt-4" if you have access
            messages=[
                {"role": "system", "content": "You are Elara, a helpful, friendly, and intelligent AI assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        reply = response['choices'][0]['message']['content'].strip()
        return jsonify({"response": reply})

    except Exception as e:
        return jsonify({"response": f"Oops! Something went wrong: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
