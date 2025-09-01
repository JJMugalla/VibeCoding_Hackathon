from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import mysql.connector
import requests
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

app = Flask(__name__)
CORS(app)

# Database configuration
db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'polyglotpals')
}

# Supabase configuration
supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(supabase_url, supabase_key)

# Hugging Face configuration
HF_API_TOKEN = os.getenv('HF_API_TOKEN')
HF_API_URL = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"

headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.json
    language = data.get('language')
    question = data.get('question')
    
    if not language or not question:
        return jsonify({'error': 'Language and question are required'}), 400
    
    # Get context based on language (in a real app, this would come from your database)
    context = get_context_for_language(language)
    
    # Query Hugging Face API
    payload = {
        "inputs": {
            "question": question,
            "context": context
        }
    }
    
    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload)
        result = response.json()
        
        if 'error' in result:
            return jsonify({'error': result['error']}), 500
        
        answer = result.get('answer', 'Sorry, I could not find an answer to your question.')
        
        # Store question and answer in MySQL
        store_qa_in_mysql(language, question, answer)
        
        # Also store in Supabase for real-time features
        store_qa_in_supabase(language, question, answer)
        
        return jsonify({'answer': answer})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_context_for_language(language):
    # In a real application, this would fetch from your database
    # For demo purposes, we're using static context
    contexts = {
        'english': "English is a West Germanic language that was first spoken in early medieval England. It is the third most spoken native language in the world. English has developed over more than 1,400 years. The earliest forms of English, a set of Anglo-Frisian dialects brought to Great Britain by Anglo-Saxon settlers in the 5th century, are called Old English.",
        'spanish': "El español es una lengua romance procedente del latín vulgar. Se originó en la península ibérica. Es la segunda lengua del mundo por número de hablantes nativos. El español moderno se desarrolló a partir del castellano medieval, que se hablaba en el Reino de Castilla durante la Edad Media.",
        'swahili': "Kiswahili ni lugha ya Kibantu yenye misamiati mingi ya Kiarabu. Inazungumzwa hasa katika nchi za Afrika Mashariki na Kati. Ni lugha ya taifa ya Kenya na Tanzania. Kiswahili kimekuwa na maneno mengi yaliyokopwa kutoka kwa lugha nyingine kama Kiarabu, Kiingereza na Kireno."
    }
    return contexts.get(language, contexts['english'])

def store_qa_in_mysql(language, question, answer):
    try:
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            query = "INSERT INTO questions (language, question, answer) VALUES (%s, %s, %s)"
            cursor.execute(query, (language, question, answer))
            connection.commit()
            cursor.close()
            connection.close()
    except Exception as e:
        print(f"Error storing in MySQL: {e}")

def store_qa_in_supabase(language, question, answer):
    try:
        data, count = supabase.table('questions').insert({
            "language": language,
            "question": question,
            "answer": answer
        }).execute()
    except Exception as e:
        print(f"Error storing in Supabase: {e}")

if __name__ == '__main__':
    app.run(debug=True)