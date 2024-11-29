# SOEN321-Project
Enhancing Privacy Rights and Consumer Protection Through AI-Driven Consent Management in Digital Services 

## Summary
This project aims to develop an AI-based framework to empower online consumers to make informed decisions about their data privacy. By leveraging AI to interpret complex privacy policies, the system would flag risks and help users customize their consent preferences. The project will involve fine-tuning a machine learning model (or using a suitable existing one) for privacy policy interpretation, building a prototype consent tool, and assessing its effectiveness. 

### Solution 
1. Use AI to analyze and simplify privacy policies.
2. Highlight potential risks and let users set personalized consent preferences.
3. Build an interactive tool where users can explore these options and tailor their consent settings.

### Goals
1. Train or adapt a machine learning model to interpret privacy policies.
2. Develop a web-based tool using Python and Flask.
3. Provide visual feedback and customization options to users.

### First Commit Project Structure
The first commit sets up the project structure for the front-end, JS (AJAX), and back-end. Here's a small recap of how the project functions:

	1. The user navigates to a webpage and wants to check it's privacy policy score.
	2. The user clicks the pop-up (Chrome extension) and which will then start the "Analysis" process.
	3. The front-end button is linked to the JS script which takes the webpage's URL and creates an AJAX request sending that information to the back-end.
	4. The back-end gets the requests and queries ChatGPT (make sure to use the specific GPT we were given) API. The response from GPT is then sanitized and sent back to AJAX in a JSON format.
	5. The information is then presented cleanly to the user. 

### Dependencies
1. Flask: Backend framework - _pip install Flask Flask-CORS_
2. OpenAI API: For privacy policy analysis - _pip install openai==0.28 python-dotenv_
3. Summarize extract Text - _pip install sumy_ , _pip install nltk_
4. Python package used for making HTTP requests- _pip install requests_
5. Add API Key: Create .env file - _touch .env_
6. Add the _**secret key**_
7. Run: _python app.py_

### Chrome Extension
1. Go to chrome://extensions/
2. Enable Developer mode
3. Load unpacked project folder > static
4. Click Update
5. Add Extension to task bar

**Once all dependencies are installed and the extension is set up, you can begin analyzing privacy policies by clicking the extension icon and then "Analyze TOS".**
