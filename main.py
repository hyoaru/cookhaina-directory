import os
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for, abort
from flask_assets import Environment, Bundle
from flask_login import login_user, current_user, logout_user, login_required

# App imports
from utilities.api_requests import (
    get_request_from_search_by_main_ingredient, get_request_categories_information,
    get_request_from_search_by_category, get_request_random_meal_of_the_day, 
    get_request_from_search_by_name, get_request_from_meal_by_id)

from forms import LoginForm, SignUpForm, CommentForm, AccountForm, UpdatePasswordForm
from models import User, Favorite, Comment
from instances import db, login_manager, bcrypt

# Load environment variables
load_dotenv()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
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

# Main

@app.route('/')
def home():
    meal_of_the_day_category = get_request_random_meal_of_the_day()['meals'][0]['strCategory']
    meals = get_request_from_search_by_category(meal_of_the_day_category)['meals']
    return render_template('main/home.html', meals = meals)

@app.route('/about')
def about():
    return render_template('main/about.html')

@app.route('/search_results')
def search_results():
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

    return render_template('main/search_results.html', meals = meals, keyword = keyword)

@app.route('/search')
def search():
    return render_template('main/search.html')

@app.route('/category/<category_name>')
def category(category_name):
    meals = get_request_from_search_by_category(category_name)['meals']
    return render_template('main/category.html', meals = meals, category_name = category_name)

@app.route("/meal/<id>", methods = ['GET', 'POST'])
def meal_details(id):
    is_favorite = False
    if current_user.is_authenticated:
        user_meal_favorites = Favorite.get_by_meal_id_and_user_id(meal_id = id, user_id = current_user.id)
        if user_meal_favorites:
            is_favorite = True

    meal = get_request_from_meal_by_id(id)['meals'][0]
    meal.update({"is_favorite": is_favorite})

    keys = [key for key in meal.keys()]

    def get_key_group(key_name_start_with: str) -> list:
        key_group_list = []
        for key in keys:
            if not key.startswith(key_name_start_with):
                continue
            item = meal[key]
            if item not in ['', None]:
                key_group_list.append(item)
        return key_group_list
        
    meal_ingredients = get_key_group('strIngredient')
    meal_ingredients_measure = get_key_group('strMeasure')
    meal_ingredient_by_measure = dict(zip(meal_ingredients, meal_ingredients_measure))

    comment_list = Comment.get_by_meal_id(meal_id = id)

    form = CommentForm()
    if form.validate_on_submit():
        Comment(comment = form.comment.data, meal_id = id, user = current_user, ).save()
        return redirect(url_for('meal_details', id = id))

    return render_template(
        'main/meal_details.html', form = form, meal = meal,
        meal_ingredient_by_measure = meal_ingredient_by_measure,
        comment_list = comment_list)


@app.route("/meal/<id>/comment/<comment_id>/delete")
@login_required
def meal_comment_delete(id, comment_id):
    comment = Comment.get_by_id(id = comment_id)
    if current_user != comment.user:
        abort(403)
    else:
        return redirect(url_for('meal_details', id = id))


@app.route("/meal/<id>/favorite")
@login_required
def meal_add_to_favorite(id):
    favorite = Favorite.get_by_meal_id_and_user_id(meal_id = id, user_id = current_user.id)
    if not favorite:
        Favorite(meal_id = id, user = current_user, ).save()
    else:
        favorite.delete()

    return redirect(url_for('meal_details', id = id))

@app.route("/user/<username>/favorites")
def user_favorites(username):
    user = User.get_by_username(username = username)
    favorites = []
    meals = []
    if user:
        favorites = Favorite.get_by_user_id(user_id = user.id)
        for favorite in favorites:
            meal = get_request_from_meal_by_id(f"{favorite.meal_id}")['meals'][0]
            meals.append(meal)
    else:
        abort(404)

    return render_template('main/user_favorites.html', meals = meals, user = user)


# Authentication

@app.route("/login", methods = ['POST', 'GET'])
def login():
    if not current_user.is_authenticated:
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username = form.username.data).first()
            if user and bcrypt.check_password_hash(pw_hash = user.password, password = form.password.data):
                login_user(user = user, remember = form.remember.data)
                return redirect(url_for('home'))
            
        return render_template('authentication/login.html', form = form)
    else:
        return redirect(url_for('home'))


@app.route("/signup", methods = ['POST', 'GET'])
def signup():
    if not current_user.is_authenticated:
        form = SignUpForm()
        if form.validate_on_submit():
            new_user = User(
                username = form.username.data,
                email = form.email.data,
                password = (
                    bcrypt
                    .generate_password_hash(form.password.data)
                    .decode('utf-8')), )
            
            new_user.save()
            return redirect(url_for('login'))

        return render_template('authentication/signup.html', form = form)
    else:
        return redirect(url_for('home'))

@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for('home'))


# Account

@app.route('/account', methods = ['GET', 'POST'])
@login_required
def account():
    form = AccountForm()
    if form.is_submitted():
        user = User.get_by_id(id = current_user.id)
        user.email = form.email.data if form.email.data and form.email.validate(form) else user.email
        user.username = form.username.data if form.username.data else user.username
            
        db.session.commit()
        return redirect(request.referrer)

    return render_template('authentication/account.html', form = form)

@app.route('/account/password', methods = ['GET', 'POST'])
@login_required
def account_password():
    form = UpdatePasswordForm()
    if form.validate_on_submit():
        current_user.password = (
            bcrypt
            .generate_password_hash(form.new_password.data)
            .decode('utf-8'))
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('authentication/account_password.html', form = form)


# Error pages

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
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    with app.app_context():
        db.create_all()

    app.run(debug=True)