from datetime import date
import shutil
import subprocess
import os
import sys

run_create_org_data_file = 'createOrgDataFile.py'
run_create_org_data_args = [f'{sys.argv[1]}']
current_directory = os.getcwd()

subprocess.run(['python3', run_create_org_data_file] + run_create_org_data_args)

def find_org_data_files():
    org_data_files_path = []
    org_data_file_name = 'snyk-created-orgs-'
    matching_files = [f for f in os.listdir(current_directory) if f.startswith(org_data_file_name)]

    print("Files that start with '{}':".format(org_data_file_name))
    for file in matching_files:
        file_path = current_directory + '/' + file
        org_data_files_path.append(file_path)
    return org_data_files_path

def find_log_files():
    log_files = [f for f in os.listdir(current_directory) if f.endswith('.log')]
    log_file_data = []
    for file in log_files:
        file_path = current_directory + '/' + file
        log_file_data.append(file_path)
    return log_file_data

def find_import_data_file():
    import_data_file_name = 'gitlab-import-targets.json'
    matching_file = [f for f in os.listdir(current_directory) if f.startswith(import_data_file_name)]
    print(matching_file)
    print(f'Here is the lengtth of the import file list: {len(matching_file)}')
    if len(matching_file) >= 1:
        matching_file = current_directory + '/' + matching_file[0]
        return matching_file
    else:
        return None   

def import_repos(org_data_files_path):
    for org_data_file_path in org_data_files_path:
        print(org_data_file_path)
        org_data_value = f'--orgsData={org_data_file_path}'
        # Run snyk-api-import import:data command
        subprocess.run(f'{current_directory}/snyk-api-import-macos import:data {org_data_value} --source=gitlab --integrationType=gitlab', shell=True)
        # Find gitlab-import-targets.json and run import
        import_file_path = find_import_data_file()
        subprocess.run(f'DEBUG=* {current_directory}/snyk-api-import-macos import --file={import_file_path}', shell=True)

def clean_up(list_of_files, switch):
    today_date = date.today()
    formatted_date = today_date.strftime("%m%d%Y")
    folder_name_json_files = f'json-files-dir-{formatted_date}'
    folder_name_log_files = f'log-files-dir-{formatted_date}'
    file_name_counter = 2
    making_directory = True

    # Create the new directory
    if switch:
        while making_directory:
            if os.path.exists(current_directory + '/' + folder_name_json_files):
                try:
                    os.makedirs(current_directory + '/' + folder_name_json_files + '-run#' + str(file_name_counter))
                    new_dir_path = current_directory + '/' + folder_name_json_files + '-run#' + str(file_name_counter)
                    making_directory = False
                except:
                    file_name_counter = file_name_counter + 1
            else:
                os.makedirs(current_directory + '/' + folder_name_json_files)
                new_dir_path = current_directory + '/' + folder_name_json_files
                making_directory = False
    else:
        while making_directory:
            if os.path.exists(current_directory + '/' + folder_name_log_files):
                try:
                    os.makedirs(current_directory + '/' + folder_name_log_files + '-run#' + str(file_name_counter))
                    new_dir_path = current_directory + '/' + folder_name_log_files + '-run#' + str(file_name_counter)
                    making_directory = False
                except:
                    file_name_counter = file_name_counter + 1
            else:
                os.makedirs(current_directory + '/' + folder_name_log_files)
                new_dir_path = current_directory + '/' + folder_name_log_files
                making_directory = False


    # Move files to the new directory
    for file in list_of_files:
        # Check if the file exists
        if os.path.isfile(file):
            # Strip out file name
            split = file.split('/')
            file_name = split[(len(split)-1)]
            # Move the file
            shutil.move(file, os.path.join(new_dir_path, file_name))
        else:
            print(f"File {file} does not exist")

org_data_files_path = find_org_data_files()
import_data_file = find_import_data_file()
if import_data_file != None:
    org_data_files_path.append(import_data_file)

import_repos(org_data_files_path)
log_files_path = find_log_files()

clean_up(org_data_files_path, True)
clean_up(log_files_path, False)



