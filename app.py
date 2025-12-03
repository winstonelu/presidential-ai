from flask import Flask, request, jsonify, render_template
from openai import OpenAI

app = Flask(__name__)

client = OpenAI()

system_prompt_base = """You are a really educated bot that take in the users income and saving goals, in order to use those informations you will ask the user their plan and goals.With the income and the users goal budget/what they will be saving up for you will make a plan for user preferences, even with the customized plan you should ask the user additional information. 

The format of this plan should be casual so you dont freak out the user, it should start with the dept/+money and the goal and then it should list the biggest income in the spending then you will list the top 5 alternative ways to save money or to lower the spedning on stuff that is not needed. It should provide detailed ways to save up for the budget and the thing the user desires,. it should included guide on how to save up. It should stay in context, please provide short answer at most two paragraph and 5 options for the return format. Please don't add '*' for the section.

the people who will be interacting with the ai will be people who need to keep track of their money and need to be smart in their budget and dont know how to use money wiseley. these people would include children elderly and young adults.
"""

# Store sessions in memory (temporary)
sessions = {}

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/start", methods=["POST"])
def start():
    user_choice = request.json.get("choice")

    # Create session
    session_id = str(len(sessions) + 1)

    # Copy base prompt
    system_prompt = system_prompt_base

    # Apply user choice (same logic as original code)
    if user_choice == 1:
        system_prompt += "\n The user wants a budget. Please provide step by step with an actual plan."
    elif user_choice == 2:
        system_prompt += "\n The user just want suggestions"

    chat_history = [
        {"role": "system", "content": system_prompt}
    ]

    sessions[session_id] = chat_history
    return jsonify({"session_id": session_id})


@app.route("/message", methods=["POST"])
def message():
    session_id = request.json.get("session_id")
    user_prompt = request.json.get("message")

    if session_id not in sessions:
        return jsonify({"error": "Invalid session"}), 400

    chat_history = sessions[session_id]

    # Stop condition (same logic as original code)
    if user_prompt == "STOP":
        return jsonify({"history": chat_history})

    chat_history.append({"role": "user", "content": user_prompt})

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=chat_history
    )

    assistant_response = response.choices[0].message.content

    chat_history.append({"role": "assistant", "content": assistant_response})

    return jsonify({"response": assistant_response})


if __name__ == "__main__":
    app.run(debug=True)
