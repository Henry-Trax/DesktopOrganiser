import copy
import os
import shutil


def get_dt_file_path():
    dt_file_path = os.path.abspath(__file__)

    dt_file_path = dt_file_path.split("\\")

    dt_file_path = dt_file_path[:3]

    dt_file_path.append("Desktop")

    return "\\".join(dt_file_path)


def get_dt_file_list(dt_file_path=None):
    dt_list = os.listdir(dt_file_path)
    result_list = []

    for item in dt_list:

        if item.split()[-1] != "Sorted_Folder":
            result_list.append(item)

    return result_list


def get_file_extension(file_name=None):
    return file_name.split(".")[-1]


def get_dict_of_dt_files_and_paths(dt_files, dt_file_path):
    dt_simple_dict = {}
    for file in dt_files:
        dt_simple_dict[file] = dt_file_path + "/" + file

    return dt_simple_dict


def get_data_structure(dt_simple_dict):
    dt_items_dict = {}

    for key, value in dt_simple_dict.items():

        if os.path.isdir(value):
            dt_items_dict.setdefault("Directories", [])
            dt_items_dict["Directories"].append({key: value})

        elif os.path.isfile(value):
            extension = get_file_extension(key)
            dt_items_dict.setdefault(extension, [])
            dt_items_dict[extension].append({key: value})

        else:
            dt_items_dict.setdefault("special_files", [])
            dt_items_dict["special_files"].append({key: value})

    return dt_items_dict


def create_dt_folders_and_update_data_structure(dt_items_dict, dt_file_path):
    program_made_folders = {}

    for types, items in dt_items_dict.items():

        folder_name = f"{types} - Sorted_Folder"
        folder_path = "\\".join([dt_file_path, folder_name])

        try:
            os.mkdir(folder_path)

        except FileExistsError:
            pass

        finally:
            program_made_folders.setdefault(types, [])

    dt_items_dict.setdefault("program_made_folders", program_made_folders)

    return dt_items_dict


def move_files_and_directories(dt_items_dict, dt_file_path):
    dt_items_dict_temp = copy.deepcopy(dt_items_dict)

    for extension_key, items_list in dt_items_dict.items():

        if extension_key == "program_made_folders":
            continue

        for file in dt_items_dict[extension_key]:
            current_file_location = list(dt_items_dict_temp[extension_key][-1].values())[-1]
            shutil.move(current_file_location, f"{dt_file_path}\\{extension_key} - Sorted_Folder")

            single_item = dt_items_dict_temp[extension_key].pop()

            dt_items_dict_temp["program_made_folders"][extension_key].append(single_item)

    dt_items_dict = copy.deepcopy(dt_items_dict_temp)

    return dt_items_dict


def __main__():
    dt_file_path = get_dt_file_path()

    dt_files = get_dt_file_list(dt_file_path)

    dt_simple_dict = get_dict_of_dt_files_and_paths(dt_files, dt_file_path)

    dt_data_structure_dict = get_data_structure(dt_simple_dict)

    dt_data_structure_dict = create_dt_folders_and_update_data_structure(dt_data_structure_dict, dt_file_path)

    dt_data_structure_dict = move_files_and_directories(dt_data_structure_dict, dt_file_path)

    input("Desktop Organized")


if __name__ == "__main__":
    __main__()
