# VibeCoding_Hackathon
Hackathon Instructions, Project and Explanation. 
I am focussing on SDG 4 ( Quality Education) through a language app that translates, explains and gives more information on the langage of instruction. 
Language of instruction is the most important part of the learning process. Leveraging on increase in cellurar coverage in the contry, more children will have the chance to practise and have in depth explanation in a fun, creative way in understanding the instruction language which in Africa, is more oftern not the first language. 
We'll have a simple interface with:
  - A way to select language (English, Swahili, Spanish)
  - An input for the user to ask a question
  - A button to submit the question
  - A display for the answer
 We'll also have a section for monetization (Intrasend) that might show a paywall or prompt for payment to access full functionality.
 For the backend, we'll set up a Flask server that:
  - Serves the frontend
  - Has an endpoint to handle questions (which will use the Hugging Face API)
  - Integrates with MySQL to store user questions and answers (or other data)
  - Integrates with Intrasend to check if the user has paid.
    
 1. index.html
 2. style.css
 3. script.js
 4. app.py (Flask backend)
 5. database schema for MySQL
