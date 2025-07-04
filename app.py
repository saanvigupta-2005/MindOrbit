import os
from flask import Flask, request, jsonify, render_template_string
import google.generativeai as genai

app = Flask(__name__)
genai.configure(api_key=os.environ.get("gemini"))
model = genai.GenerativeModel("gemini-pro")

# HTML template for chatbot UI
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Elara - AI Chatbot</title>
    <style>
        body { font-family: Arial; padding: 20px; background: #f4f4f4; }
        #chatbox { width: 100%; height: 400px; overflow-y: scroll; border: 1px solid #ccc; padding: 10px; background: white; }
        #userInput { width: 80%; padding: 10px; }
        #sendBtn { padding: 10px; }
    </style>
</head>
<body>
    <h2>Elara - Your AI Companion</h2>
    <div id="chatbox"></div>
    <input type="text" id="userInput" placeholder="Type your message..." />
    <button id="sendBtn">Send</button>

    <script>
        const chatbox = document.getElementById("chatbox");
        const input = document.getElementById("userInput");
        const sendBtn = document.getElementById("sendBtn");

        function appendMessage(sender, text) {
            const msg = document.createElement("div");
            msg.innerHTML = `<strong>${sender}:</strong> ${text}`;
            chatbox.appendChild(msg);
            chatbox.scrollTop = chatbox.scrollHeight;
        }

        sendBtn.onclick = async () => {
            const message = input.value.trim();
            if (!message) return;
            appendMessage("You", message);
            input.value = "";

            const res = await fetch("/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message })
            });
            const data = await res.json();
            appendMessage("Elara", data.response);
        };
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(html_template)

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    try:
        response = model.generate_content(user_input)
        reply = response.text.strip()
    except Exception as e:
        reply = f"Error: {str(e)}"
    return jsonify({"response": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
