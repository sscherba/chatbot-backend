from flask import Flask, request, jsonify
from flask_cors import CORS

import openai
import os

app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": "https://sscherba.github.io"}})

openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to read the config.txt file
def load_config():
    config = {}
    with open("config.txt", "r") as file:
        for line in file:
            if "=" in line:
                key, value = line.strip().split("=", 1)
                config[key] = value
     print("Config Loaded Successfully:", config) 
    except Exception as e:
        print("❌ Error Loading Config:", str(e))
    return config

# Load chatbot parameters
config = load_config()

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "")

    # Use parameters from config.txt
    persona = f"""
    {config.get("DEFAULT_RESPONSE", "I can help with DBT skills.")}
    
    Character Name: {config.get("Character Name", "Nikki")}
    Description: {config.get("Description", "A student learning DBT")}
    
    Conversation starters:
    - {config.get("1", "Hi Nikki, you seem upset. Are you okay?")}
    - {config.get("2", "Hi Nikki, I heard you were dropping out of school!")}
    - {config.get("3", "Would you like help with the DBT Pros and Cons skill?")}

    User: {user_input}
    Nikki:
    """

    # Call OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": persona}]
    )

    return jsonify({"reply": response['choices'][0]['message']['content']})

if __name__ == "__main__":
    app.run(debug=True)
