import copy
import os
import shutil
from time import sleep
import json


def get_dt_file_path():
    path = ["C:", os.environ["HOMEPATH"], "\\Desktop"]
    return "".join(path)


def clear():
    os.system('cls')


def create_defaults_settings():
    settings = {}
    settings.setdefault(1, True)
    # Organise folders in path
    settings.setdefault(2, get_dt_file_path())
    # Organise path

    return settings


def change_setting2(settings):
    while True:
        setting = "File path organised"
        print_header(f"Settings - {setting}")
        print(f"Current value = {settings[2]}")
        prev_answer = input("Enter new value or type 'Cancel' to cancel :: ")

        if prev_answer.lower() == "cancel":
            return settings

        elif os.path.isdir(prev_answer):
            settings[2] = prev_answer
            return settings

        else:
            print("Invalid Response")



def change_setting1(settings):
    while True:
        setting = "Organise existing folders"
        print_header(f"Settings - {setting}")
        print(f"Current value = {settings[1]}")
        prev_answer = input("Enter new value or type 'Cancel' to cancel :: ")

        if prev_answer.lower() == "cancel":
            return settings

        elif prev_answer.lower() in ["true", "false"]:

            if prev_answer.lower() == "false":
                settings[1] = False

            elif prev_answer.lower() == "true":
                settings[1] = True

            return settings

        else:
            print("Invalid Response")


def open_settings(settings):
    while True:
        setting2 = "Organise existing folders"
        setting3 = "Organise path"

        print_header("Settings")
        print(f"1 - Exit\n"
              f"2 - {setting2} - {settings[1]}\n"
              f"3 - {setting3} - {settings[2]}")

        try:
            prev_answer = int(input("Please select option :: "))

        except:
            continue

        if prev_answer == 1:
            break

        elif prev_answer == 2:
            settings = change_setting1(settings)

        elif prev_answer == 3:
            settings = change_setting2(settings)

    return settings


def print_header(header):
    clear()

    header = f"| {header} |"
    print(f"{'=' * 100}", end="")
    print(f"\r<{header:=^102}>")


def input_user_options():
    receiving_input = True
    settings = create_defaults_settings()

    while receiving_input:

        print_header("Options")
        print("1 - Settings \n"
              "2 - Run Program")

        try:
            prev_answer = int(input("Please select option :: "))

        except:
            continue

        if prev_answer == 2:
            receiving_input = False
            continue

        elif prev_answer == 1:
            settings = open_settings(settings)

    return settings


def get_dt_file_list(settings):
    dt_list = os.listdir(settings[2])
    result_list = []

    for item in dt_list:

        if item.split()[-1] != "Sorted_Folder" and get_file_extension(item) != "ini":
            result_list.append(item)

    return result_list


def get_file_extension(file_name=None):
    return file_name.split(".")[-1]


def get_dict_of_dt_files_and_paths(dt_files, settings):
    dt_simple_dict = {}
    for file in dt_files:
        dt_simple_dict[file] = settings[2] + "/" + file

    return dt_simple_dict


def get_data_structure(dt_simple_dict, settings):
    dt_items_dict = {}

    for key, value in dt_simple_dict.items():

        if os.path.isdir(value):

            if not settings[1]:
                continue

            else:
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


def create_dt_folders_and_update_data_structure(dt_items_dict, settings):
    program_made_folders = {}

    for types, items in dt_items_dict.items():

        folder_name = f"{types} - Sorted_Folder"
        folder_path = "\\".join([settings[2], folder_name])

        try:
            os.mkdir(folder_path)

        except FileExistsError:
            pass

        finally:
            program_made_folders.setdefault(types, [])

    dt_items_dict.setdefault("program_made_folders", program_made_folders)

    return dt_items_dict


def move_files_and_directories(dt_items_dict, settings):
    dt_items_dict_temp = copy.deepcopy(dt_items_dict)

    for extension_key, items_list in dt_items_dict.items():

        if extension_key == "program_made_folders":
            continue

        for file in dt_items_dict[extension_key]:
            current_file_location = list(dt_items_dict_temp[extension_key][-1].values())[-1]
            shutil.move(current_file_location, f"{settings[2]}\\{extension_key} - Sorted_Folder")

            single_item = dt_items_dict_temp[extension_key].pop()

            dt_items_dict_temp["program_made_folders"][extension_key].append(single_item)

    dt_items_dict = copy.deepcopy(dt_items_dict_temp)

    return dt_items_dict


def __main__():
    settings = input_user_options()

    dt_files = get_dt_file_list(settings)

    dt_simple_dict = get_dict_of_dt_files_and_paths(dt_files, settings)

    dt_data_structure_dict = get_data_structure(dt_simple_dict, settings)

    dt_data_structure_dict = create_dt_folders_and_update_data_structure(dt_data_structure_dict, settings)

    dt_data_structure_dict = move_files_and_directories(dt_data_structure_dict, settings)

    print_header("Desktop Organized")

    sleep(2)


if __name__ == "__main__":
    __main__()
