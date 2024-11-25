from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import html
import validators
import time
import os
import openai
import requests

app = Flask(__name__)
CORS(app)

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

load_dotenv()
openai.api_key = os.getenv("bananaSecretKey")

def extract_text_from_url(url):
    if not validators.url(url):
        raise ValueError("Invalid URL")
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.get_text()

def analyzePolicywithAI(policy_text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a privacy and consent management assistant. "
                        "Your job is to help users understand how their data is being used, highlight any potential privacy risks, "
                        "and offer suggestions on how they can adjust their consent preferences to protect their data. "
                        "Provide your responses in clear and concise bullet points, including recommendations where relevant."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        "Analyze the following privacy policy, summarize how the user's data will be collected and used, "
                        "highlight any privacy risks, and suggest ways the user can adjust their consent preferences:\n"
                        f"{policy_text}"
                    )
                }
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return "An error occurred while analyzing the privacy policy."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
@limiter.limit("10 per minute")
def analyze():
    try:
        data = request.get_json()
        if not data or 'type' not in data or 'data' not in data:
            return jsonify({"error": "Invalid input"}), 400
            
        input_type = data['type']
        input_data = html.escape(data['data'].strip())
        
        if not input_data:
            return jsonify({"error": "Empty input"}), 400
            
        if input_type == "url":
            try:
                policy_text = extract_text_from_url(input_data)
            except Exception as e:
                return jsonify({"error": f"URL error: {str(e)}"}), 400
        elif input_type == "text":
            policy_text = input_data
        else:
            return jsonify({"error": "Invalid input type"}), 400
            
        analysis = analyzePolicywithAI(policy_text)
        return jsonify({"analysis": analysis})
        
    except Exception as e:
        app.logger.error(f"Analysis error: {str(e)}")
        return jsonify({"error": "Server error"}), 500

@app.route('/hello', methods=['POST'])
def hello():
    return jsonify(message="Hello World")

if __name__ == '__main__':
    app.run(debug=True)