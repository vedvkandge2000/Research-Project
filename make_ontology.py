# Importing required packages
import os
import json
import sys
# Reading data from json from into dataframe
def load_data(data_path):
    with open(data_path, "r", encoding="utf-8") as json_data:
        data = json.load(json_data)
    return data["hindi-attraction-original"]



# Function to create different files and folder depending on goals
def write_to_file(file_path,data):
    """
    This function will find or create a files and folder and write the data in passed file_name
    
    paramerters: 
                 file_name --> Name of file in which want to write the content
                 data ---> Data which we want to be write in file
                 
                 
    """

    with open(file_path,'w', encoding="utf-8") as f:
        json.dump(data,f, indent=3, ensure_ascii=False)
    f.close()
    
# creating ontology for hindi data
def main(data_path, file_path):

    """
    parameters: data_path ---> Path of the data file which we want to read
                root_path ---> path for root directory where all data folders will be created.
    """

    data = load_data(data_path)
    data1 = []
    data2 = []
    data3 = []
    for dict_data in data:
        data1.append(dict_data["area"]) 
        data2.append(dict_data["name"])
        data3.append(dict_data["type"])
    data1 = list(set(data1))
    data2 = list(set(data2))
    data3 = list(set(data3))
    ontology_data = {"h_attraction-semi-area":data1, "h_attraction-semi-name":data2, "h_attraction-semi-type":data3}
    write_to_file(file_path,ontology_data)

if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2])

