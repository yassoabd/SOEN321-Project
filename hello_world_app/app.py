from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import time 
#to hide the key 
from dotenv import load_dotenv
#extract, and open ai API
import time
import os
import openai
import requests

# .env file with secret key 
load_dotenv()

# Get OpenAI API key from the environment
openai.api_key = os.getenv("bananaSecretKey")

# Check if the key is loaded correctly (debugging only)
print(f"Loaded API key: {os.getenv('bananaSecretKey')}")

#Please do not share the key with anyone, thank you!! 

# Function to analyze a privacy policy with openai API
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
            # 1 token = 4 character 
            max_tokens=500  
        )
        summary = response['choices'][0]['message']['content'].strip()
        return summary
    
    # Ensure that we dont exeed number of request or else bug 
    except openai.error.RateLimitError:
        print("Rate limit exceeded. Will retry after 5 seconds...")
        # delay for 5 seconds 
        time.sleep(5)  
        return analyzePolicywithAI(policy_text)
    
    # Open AI error set up
    except openai.error.OpenAIError as e:
        print(f"OpenAI API error: {e}")
        return "An error occurred while analyzing the privacy policy."

# Example of google term (will have to extract it from page with json)
policy_text = "We use data to build better services We use the information we collect from all our services for the following purposes: Provide our services We use your information to deliver our services, like processing the terms you search for in order to return results or helping you share content by suggesting recipients from your contacts. Maintain & improve our services We also use your information to ensure our services are working as intended, such as tracking outages or troubleshooting issues that you report to us. And we use your information to make improvements to our services — for example, understanding which search terms are most frequently misspelled helps us improve spell-check features used across our services.Develop new services"

summary = analyzePolicywithAI(policy_text)
print(summary)
    
app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    # Render the front-end HTML file
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Unified route to analyze a privacy policy based on user input (text or URL).
    """
    data = request.json
    input_type = data.get("type")  # "text" or "url"
    input_data = data.get("data")

    if not input_type or not input_data:
        return jsonify({"error": "Invalid input. Please specify 'type' and 'data'."}), 400

    if input_type == "url":
        try:
            # Fetch the policy text from the URL
            response = requests.get(input_data)
            if response.status_code == 200:
                policy_text = response.text
            else:
                return jsonify({"error": "Failed to fetch policy from the URL."}), 500
        except Exception as e:
            return jsonify({"error": f"Error fetching policy from URL: {str(e)}"}), 500
    elif input_type == "text":
        policy_text = input_data
    else:
        return jsonify({"error": "Invalid input type. Use 'text' or 'url'."}), 400

    # Analyze the policy text
    analysis = analyzePolicywithAI(policy_text)
    return jsonify({"analysis": analysis})

@app.route('/hello', methods=['POST'])
def hello():
    # Respond with a JSON message
    return jsonify(message="Hello World")

if __name__ == '__main__':
    app.run(debug=True)