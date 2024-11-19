# SOEN321-Project
Enhancing Privacy Rights and Consumer Protection Through AI-Driven Consent Management in Digital Services 

## Summary
This project aims to develop an AI-based framework to empower online consumers to make informed decisions about their data privacy. By leveraging AI to interpret complex privacy policies, the system would flag risks and help users customize their consent preferences. The project will involve fine-tuning a machine learning model (or using a suitable existing one) for privacy policy interpretation, building a prototype consent tool, and assessing its effectiveness. 


### First Commit project structure
The first commit sets up the project structure for the front-end, JS (AJAX), and back-end. Here's a small recap of how the project functions:

	1. The user navigates to a webpage and wants to check it's privacy policy score.
	2. The user opens the pop-up (Chrome extension) and clicks on the "Analyze" button.
	3. The front-end button is linked to the JS script which takes the webpage's URL and creates an AJAX request sending that information to the back-end.
	4. The back-end gets the requests and queries ChatGPT (make sure to use the specific GPT we were given) API. The response from GPT is then sanitized and sent back to AJAX in a JSON format.
	5. The information is then presented cleanly to the user. 
	This is just testing lol. .


### Dependencies
1. Flask: Backend framework - _pip install Flask Flask-CORS_
2. OpenAI API: For privacy policy analysis - _pip install openai==0.28 python-dotenv_
3. **New**:- Python package used for making HTTP requests- _pip install requests_
4. Add API Key: Create .env file - _touch .env_
5. Add the _**secret key**_
6. Run: _python app.py_
7. Access on browser: _http://127.0.0.1:5000/_
