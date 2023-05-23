import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, url_for
from flask_assets import Environment, Bundle

# App imports
from utilities.api_requests import (
    get_request_from_search_by_main_ingredient, get_request_categories_information,
    get_request_from_search_by_category, get_request_random_meal_of_the_day, 
    get_request_from_search_by_name, get_request_from_meal_by_id)

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
def home():
    meal_of_the_day_category = get_request_random_meal_of_the_day()['meals'][0]['strCategory']
    meals = get_request_from_search_by_category(meal_of_the_day_category)['meals']
    print(meals)
    return render_template('main/home.html', meals = meals)

@app.route('/search')
def search():
    query_request = request.args.get(key = 'keyword', type = str)
    keyword = '' if query_request is None else query_request
    
    by_main_ingredient = get_request_from_search_by_main_ingredient(keyword)['meals']
    by_main_ingredient = [] if by_main_ingredient is None else by_main_ingredient
    by_meal_name = get_request_from_search_by_name(keyword)['meals']
    by_meal_name = [] if by_meal_name is None else by_meal_name

    by_meal_name_ids = [meal.get('idMeal') for meal in by_meal_name]
    meals = by_meal_name
    
    for meal in by_main_ingredient:
        meal_not_present_in_main_list = meal.get('idMeal') not in by_meal_name_ids
        if meal_not_present_in_main_list:
            meals.append(meal)

    return render_template('main/search.html', meals = meals, keyword = keyword)

@app.route('/category/<category_name>')
def category(category_name):
    meals = get_request_from_search_by_category(category_name)['meals']
    return render_template('main/category.html', meals = meals, category_name = category_name)

@app.route("/meal/<id>")
def meal_details(id):
    meal = get_request_from_meal_by_id(id)
    keys = [key for key in meal.keys()]

    meal_ingredients = []
    for key in keys:
        if not key.startswith('strIngredient'):
            continue
        ingredient_key = key
        ingredient = meal[ingredient_key]
        if ingredient != '':
            meal_ingredients.append(ingredient)

    meal_ingredients_measure = []
    for key in keys:
        if not key.startswith('strMeasure'):
            continue
        ingredient_measure_key = key
        ingredient_measure = meal[ingredient_measure_key]
        if ingredient_measure != '':
            meal_ingredients_measure.append(ingredient_measure)

    meal_ingredient_by_measure = dict(zip(meal_ingredients, meal_ingredients_measure))
    print(meal_ingredient_by_measure)

    return render_template(
        'main/meal_details.html', meal = meal, meal_ingredient_by_measure= meal_ingredient_by_measure)

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