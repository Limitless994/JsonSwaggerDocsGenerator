import os
import json
import shutil
from datetime import datetime
from tkinter import filedialog, Tk, simpledialog
from docx import Document
from general_section import add_general_section
from parameters_section import add_parameters_and_configurations_section
from endpoints_description import add_endpoints_description_section
from utils import read_swagger_file
import sys
sys.setrecursionlimit(1500)
def choose_directory():
    root = Tk()
    root.withdraw()
    root.update()
    directory_path = filedialog.askdirectory(title="Select Directory Containing JSON Files")
    root.destroy()
    return directory_path

def ask_github_link():
    root = Tk()
    root.withdraw()
    github_link = simpledialog.askstring("Input", "Please enter the GitHub repository link:")
    root.destroy()
    return github_link

def load_config():
    with open('config.json', 'r') as file:
        config = json.load(file)
    return config

def generate_documentation(swagger_data, input_file_path, github_link, config):
    if swagger_data:
        try:
            document = Document()
            general_index = 1
            parameters_index = 2
            models_index = 2 
            endpoints_index = 3
            general_index = add_general_section(document, swagger_data, general_index)
            parameters_index, models_index = add_parameters_and_configurations_section(document, swagger_data, parameters_index, models_index, github_link, config)
            add_endpoints_description_section(document, swagger_data, endpoints_index, input_file_path, config)
            
            file_name_without_extension = os.path.splitext(os.path.basename(input_file_path))[0]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M")
            output_file_name = f"{file_name_without_extension}_documentation_{timestamp}.docx"
            output_file_path = os.path.join("GeneratedDocs", output_file_name)
            
            os.makedirs("GeneratedDocs", exist_ok=True)
            
            document.save(output_file_path)
            print(f"Document saved successfully at: {output_file_path}")
            
            processed_folder = os.path.join("Processed", timestamp)
            os.makedirs(processed_folder, exist_ok=True)
            shutil.move(input_file_path, processed_folder)
            
        except Exception as e:
            print(f"Error saving document: {e}")
            
            error_folder = os.path.join("InError", timestamp)
            os.makedirs(error_folder, exist_ok=True)
            shutil.move(input_file_path, error_folder)
    else:
        print("Failed to generate documentation. Check the Swagger file.")
        
        error_folder = os.path.join("InError", timestamp)
        os.makedirs(error_folder, exist_ok=True)
        shutil.move(input_file_path, error_folder)

def process_directory(directory_path, config):
    for filename in os.listdir(directory_path):
        if filename.endswith(".json") and filename != "config.json":
            file_path = os.path.join(directory_path, filename)
            swagger_data = read_swagger_file(file_path)
            github_link = config['default_github_link'] + os.path.splitext(filename)[0]
            
            generate_documentation(swagger_data, file_path, github_link, config)

if __name__ == "__main__":
    config = load_config()
    #github_link = ask_github_link()
    directory_path = config['directory']
    if directory_path:
        #process_directory(directory_path, github_link, config)
        process_directory(directory_path, config)
    else:
        print("No directory selected. The script will be terminated.")
