import requests

# App imports
from utilities.essentials import load_binary, saveto_binary

def get_request_from_search(keyword: str, api: str, folder_name: str) -> dict:
    keyword = keyword.replace(' ', '_')
    api = f'{api}{keyword}'
    folder_name = 'by_main_ingredient'

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