import os
from dotenv import load_dotenv
from flask import Flask, render_template, request
from flask_assets import Environment, Bundle

# App imports
from utilities.api_requests import (
    get_request_from_search_by_main_ingredient, get_request_categories_information,
    get_request_from_search_by_category, get_request_random_meal_of_the_day, 
    get_request_from_search_by_name)

# Load environment variables
load_dotenv()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

Environment(app).register({
    'styles': Bundle(
        'assets/scss/style.scss', filters = ('libsass', 'cssmin'), 
        depends = 'packages/bootstrap-5.3.0-alpha3/scss/*.scss',
        output = 'assets/css/main.css', ), 
    'style_scripts': Bundle(
        'packages/bootstrap-5.3.0-alpha3/dist/js/bootstrap.bundle.js',
        filters = ('jsmin'), output = 'assets/js/style_scripts.js', ), 
    'user_scripts': Bundle(
        'assets/js/user_defined.js',
    ), })

@app.context_processor
def inject_global_elements():
    categories_information = get_request_categories_information()['categories']
    meal_of_the_day = get_request_random_meal_of_the_day()['meals'][0]
    return dict(
        categories_information = categories_information, meal_of_the_day = meal_of_the_day)

@app.route('/')
@app.route('/home')
def home():
    meals = get_request_from_search_by_main_ingredient('beef')['meals']
    return render_template('main/home.html', meals = meals)

@app.route('/search')
def search():
    query_request = request.args.get(key = 'keyword', type = str)
    keyword = '' if query_request is None else query_request
    
    by_main_ingredient = get_request_from_search_by_main_ingredient(keyword)['meals']
    by_main_ingredient = [] if by_main_ingredient is None else by_main_ingredient
    by_meal_name = get_request_from_search_by_name(keyword)['meals']
    by_meal_name = [] if by_meal_name is None else by_meal_name

    meals = by_meal_name + by_main_ingredient
    return render_template('main/search.html', meals = meals, keyword = keyword)

@app.route('/category/<category_name>')
def category(category_name):
    meals = get_request_from_search_by_category(category_name)['meals']
    return render_template('main/category.html', meals = meals, category_name = category_name)

@app.route('/about')
def about():
    return render_template('main/about.html')

@app.errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403

@app.errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)