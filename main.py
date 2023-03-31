import os
from dotenv import load_dotenv
from flask import Flask, render_template, request

# App imports
from utilities.api_requests import (
    get_request_from_search_by_main_ingredient, get_request_categories_information,
    get_request_from_search_by_category)

# Load environment variables
load_dotenv()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

@app.context_processor
def inject_global_elements():
    categories_information = get_request_categories_information()['categories']
    return dict(
        categories_information = categories_information)

@app.route('/')
@app.route('/home')
def home():
    meals = get_request_from_search_by_main_ingredient('beef')['meals']
    return render_template('main/home.html', meals = meals)

@app.route('/search')
def search():
    query_request = request.args.get(key = 'keyword', type = str)
    keyword = '' if query_request is None else query_request
    meals = get_request_from_search_by_main_ingredient(keyword)['meals']
    return render_template('main/search.html', meals = meals)

@app.route('/category/<category_name>')
def category(category_name):
    meals = get_request_from_search_by_category(category_name)['meals']
    return render_template('main/category.html', meals = meals)


if __name__ == '__main__':
    app.run(debug=True)