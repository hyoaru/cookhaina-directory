import os
import pickle

def saveto_binary(obj_structure, file_name: str, data_root_path_folder_name: str) -> None:
    """Saves an object structure to binary format."""

    data_root_path = f'data/{data_root_path_folder_name}'
    if not os.path.exists('data'):
        os.mkdir('data')
    if not os.path.exists(f'{data_root_path}'):
        os.mkdir(f'{data_root_path}')
    with open(f'{data_root_path}/{file_name}.bin', 'wb') as file:
        pickle.dump(obj_structure, file)


def load_binary(file_name: str, data_root_path_folder_name: str):
    """Loads and returns a binary object structure."""

    data_root_path = f'data/{data_root_path_folder_name}'
    if os.path.exists(f'{data_root_path}/{file_name}.bin'):
        file = open(f'{data_root_path}/{file_name}.bin', 'rb')
        obj_structure = pickle.load(file)
        file.close()
        return obj_structure
    else:
        return {}
    