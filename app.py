# app.py
from flask import Flask, request, jsonify, render_template
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(api_key="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")

system_prompt_base = """
You are a friendly budgeting assistant.
You give calm, simple financial guidance for beginners.
Never ask follow-up questions.
Keep answers short, practical, and reassuring.
"""

chat_history = [{"role": "system", "content": system_prompt_base}]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start():
    global chat_history
    chat_history = [{"role": "system", "content": system_prompt_base}]
    choice = request.json.get("choice")

    if choice == 1:
        chat_history[0]["content"] += "\nUser wants a step-by-step budget."
    elif choice == 2:
        chat_history[0]["content"] += "\nUser wants saving suggestions."

    return jsonify({"session_id": "ok"})

@app.route("/chat")
def chat():
    return render_template("index.html", chat=chat_history)

@app.route("/message", methods=["POST"])
def message():
    global chat_history
    user_msg = request.json.get("message")

    if user_msg == "STOP":
        return jsonify({"response": "Conversation ended. You did great today."})

    chat_history.append({"role":"user","content":user_msg})

    res = client.chat.completions.create(
        model="gpt-4o",
        messages=chat_history
    )

    reply = res.choices[0].message.content
    chat_history.append({"role":"assistant","content":reply})

    return jsonify({"response": reply})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
