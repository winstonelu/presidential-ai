# app.py
import os
from flask import Flask, request, jsonify, render_template
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

#test
app = Flask(__name__)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

system_prompt_base = """
You are a really educated bot that take in the users income and saving goals, in order to use those informations you will ask the user their plan and goals.With the income and the users goal budget/what they will be saving up for you will make a plan for user preferences, even with the customized plan you should ask the user additional information. 

The format of this plan should be casual so you dont freak out the user, it should start with the dept/+money and the goal and then it should list the biggest income in the spending then you will list the top 5 alternative ways to save money or to lower the spedning on stuff that is not needed. It should provide detailed ways to save up for the budget and the thing the user desires,. it should included guide on how to save up. It should stay in context, please provide short answer at most two paragraph and 5 options for the return format. Please don't add '*' for the section.

the people who will be interacting with the ai will be people who need to keep track of their money and need to be smart in their budget and dont know how to use money wiseley. these people would include children elderly and young adults.
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
