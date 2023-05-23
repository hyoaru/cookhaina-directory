from datetime import datetime, timedelta
import requests

# App imports
from utilities.essentials import load_binary, saveto_binary

def get_request_from_search(keyword: str, api: str, folder_name: str) -> dict:
    keyword = keyword.replace(' ', '_')
    api = f'{api}{keyword}'
    folder_name = folder_name

    request = load_binary(file_name = keyword, data_root_path_folder_name = folder_name)
    request_not_exist_locally = request == {}

    if request_not_exist_locally:
        request = requests.get(api).json()
        saveto_binary(obj_structure = request, file_name = keyword, data_root_path_folder_name = folder_name)

    return request
    
def get_request_from_search_by_main_ingredient(keyword: str) -> dict:
    request = get_request_from_search(
        keyword = keyword, folder_name = 'by_main_ingredient', 
        api = 'https://www.themealdb.com/api/json/v1/1/filter.php?i=')
    
    return request

def get_request_categories_information() -> dict:
    api = 'https://www.themealdb.com/api/json/v1/1/categories.php'
    folder_name = 'categories_information'
    file_name = 'categories'

    request = load_binary(file_name = file_name, data_root_path_folder_name = folder_name)
    request_not_exist_locally = request == {}

    if request_not_exist_locally:
        request = requests.get(api).json()
        saveto_binary(obj_structure = request, file_name = file_name, data_root_path_folder_name = folder_name)

    return request

def get_request_from_search_by_category(keyword: str) -> dict:
    request = get_request_from_search(
        keyword = keyword, folder_name = 'category', 
        api = 'https://www.themealdb.com/api/json/v1/1/filter.php?c=')

    return request

def get_request_random_meal_of_the_day() -> dict:
    api = 'https://www.themealdb.com/api/json/v1/1/random.php'
    folder_name = 'random'
    file_name = 'meal_of_the_day'

    request = load_binary(file_name = file_name, data_root_path_folder_name = folder_name)
    request_not_exist_locally = request == {}

    if request_not_exist_locally:
        try:
            request = requests.get(api).json()
            request.update({'dateToReload': datetime.utcnow().date() + timedelta(days = 1)})
            saveto_binary(obj_structure = request, file_name = file_name, data_root_path_folder_name = folder_name)
        except:
            request = {}

    request_date_to_reload = request.get('dateToReload')

    if request_date_to_reload is not None and request_date_to_reload > datetime.utcnow().date():
        return request
    else:
        try:
            request = requests.get(api).json()
            request.update({'dateToReload': datetime.utcnow().date() + timedelta(days = 1)})
            saveto_binary(obj_structure = request, file_name = file_name, data_root_path_folder_name = folder_name)
        except:
            request = {}

    return request

def get_request_from_search_by_name(keyword: str) -> dict:
    request = get_request_from_search(
        keyword = keyword, folder_name = 'meal_name', 
        api = 'https://www.themealdb.com/api/json/v1/1/search.php?s=')

    return request

def get_request_from_meal_by_id(id):
    request = get_request_from_search(
        keyword = id, folder_name = 'meal_details',
        api = 'https://www.themealdb.com/api/json/v1/1/lookup.php?i='
    )

    return request