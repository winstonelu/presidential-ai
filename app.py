# app.py
import os
from flask import Flask, request, jsonify, render_template
from openai import OpenAI
from dotenv import load_dotenv

# ✅ load .env
load_dotenv()

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

system_prompt_base = """You are a friendly and educated budgeting assistant.

You take the user's income, expenses, and savings goal, then produce a simple and casual budget plan.
Do NOT ask follow-up questions.
Give a clear plan in at most two short paragraphs.

Format:
Start with money status (extra money or deficit) and goal.
Mention biggest spending category.
List 5 clear ways to save or reduce unnecessary spending.

Audience includes children, young adults, and elderly users.
No bullet symbols like *.
"""

chat_history = [{"role": "system", "content": system_prompt_base}]


@app.route("/")
def index():
    return render_template("index.html", chat=None)


@app.route("/start", methods=["POST"])
def start():
    global chat_history
    chat_history = [{"role": "system", "content": system_prompt_base}]
    return jsonify({"ok": True})


@app.route("/chat")
def chat():
    return render_template("index.html", chat=chat_history)


@app.route("/message", methods=["POST"])
def message():
    global chat_history

    user_prompt = request.json.get("message")

    if user_prompt == "STOP":
        return jsonify({"response": "Session ended. Refresh to start again."})

    chat_history.append({"role": "user", "content": user_prompt})

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=chat_history
    )

    assistant_response = response.choices[0].message.content
    chat_history.append({"role": "assistant", "content": assistant_response})

    return jsonify({"response": assistant_response})


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
