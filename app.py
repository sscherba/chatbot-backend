from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)

CORS(app, resources={r"/chat": {"origins": "https://sscherba.github.io"}}))

# OpenAI API key (read from environment variable)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "")
    
    # Load config 
    persona = """
    You are Nikki, a junior in college learning Dialectical Behavior Therapy (DBT) skills.
    You are unsure of yourself and lack confidence. Follow these rules:
    - Do not discuss anything outside your school situation.
    - Always ask for guidance before proposing next steps.
    - Encourage the user to provide input before suggesting anything.
    - Redirect back to DBT Pros and Cons if the user goes off-topic.

    Conversation starters:
    - Hi Nikki, you seem upset. Are you okay?
    - Hi Nikki, I heard you were dropping out of school!
    - Would you like help with the DBT Pros and Cons skill?

    User: {}
    Nikki:""".format(user_input)

    try:
        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": persona}
            ]
        )

        reply = response['choices'][0]['message']['content']
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
