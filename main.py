import os
from dotenv import load_dotenv
from flask import Flask, render_template, request

# App imports
from utilities.search_requests import get_request_from_search_by_main_ingredient

# Load environment variables
load_dotenv()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

@app.route('/')
@app.route('/home')
def home():
    meals = get_request_from_search_by_main_ingredient('beef')['meals']
    return render_template('main/home.html', meals = meals)

if __name__ == '__main__':
    app.run(debug=True)