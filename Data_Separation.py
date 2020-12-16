# Importing required packages
import pandas as pd
import os
import json
import sys

# Reading data from json from into dataframe
def load_data(data_path):
    data = pd.read_json(data_path)
    return data

# Function to create different files and folder depending on goals
def write_to_file(folder_name,file_name,data,root):
    """
    This function will find or create a files and folder and write the data in passed file_name
    
    paramerters: folder_name --> Name of folder in which file is present or want to create
                 file_name --> Name of file in which want to write the content
                 data ---> Data which we want to be write in file
                 
    """
    path = os.path.join(root,folder_name)
    if not os.path.exists(path):
        os.makedirs(path)
    file_path = os.path.join(path,file_name)
    with open(file_path,'w') as f:
        data = data.to_dict()
        json.dump(data,f, indent=3)
    f.close()
    text_file = os.path.join(root,folder_name+".txt")
    with open(text_file, 'a+') as t:
        t.write(file_name+"\n")
    t.close()

def main(data_path, root_path):

    """
    parameters: data_path ---> Path of the data file which we want to read
                root_path ---> path for root directory where all data folders will be created.
    """

    data = load_data(data_path)
    # Creating root diretory
    if not os.path.isdir(root_path):
        os.makedirs(root_path)   
    l = len(data.columns)

    # Extreacting file names from data
    file_names = data.columns

    # Counter variables to write number of files in excel
    count1 = 0
    count2 = 0
    count3 = 0
    count4 = 0
    count5 = 0
    count6 = 0
    count7 = 0
    # Iterrating over each file and checking different condition for different goals
    for i,file_name in enumerate(file_names):
        if(i % 1000 == 0):
            print("------Completed {}/{}------".format(i,l))
        if(len(data[file_name]["goal"]["attraction"]) != 0 and len(data[file_name]["goal"]["taxi"]) == 0 and len(data[file_name]["goal"]["restaurant"]) == 0):
            write_to_file("attraction", file_name,data[file_name],root_path)
            count1 += 1
            
        elif(len(data[file_name]["goal"]["taxi"]) != 0 and len(data[file_name]["goal"]["attraction"]) == 0 and len(data[file_name]["goal"]["restaurant"]) == 0):
            write_to_file("taxi", file_name,data[file_name],root_path)
            count2 += 1
                
        elif(len(data[file_name]["goal"]["restaurant"]) != 0 and len(data[file_name]["goal"]["attraction"]) == 0 and len(data[file_name]["goal"]["taxi"]) == 0):
            write_to_file("restaurant", file_name,data[file_name],root_path)
            count3 += 1
            
        elif(len(data[file_name]["goal"]["attraction"]) != 0 and len(data[file_name]["goal"]["taxi"]) != 0 and len(data[file_name]["goal"]["restaurant"]) == 0):
            write_to_file("attraction_&_taxi", file_name,data[file_name],root_path)
            count4 += 1
            
        elif(len(data[file_name]["goal"]["attraction"]) != 0 and len(data[file_name]["goal"]["restaurant"]) != 0 and len(data[file_name]["goal"]["taxi"]) == 0):
            write_to_file("attraction_&_restaurant", file_name,data[file_name],root_path)
            count5 += 1
            
        elif(len(data[file_name]["goal"]["restaurant"]) != 0 and len(data[file_name]["goal"]["taxi"]) != 0 and len(data[file_name]["goal"]["attraction"]) == 0):
            write_to_file("restaurant_&_taxi", file_name,data[file_name],root_path)
            count6 += 1
            
        else:
            write_to_file("other", file_name,data[file_name],root_path)
            count7 += 1
    df = pd.DataFrame({'Folders':["attraction","taxi","restaurant","attraction_&_taxi","attraction_&_restaurant","restaurant_&_taxi","others"],'No Of Files': [count1, count2, count3, count4, count5, count6, count7]})
    p = os.path.join(root_path,'trackOfNumberOfFiles.xlsx')
    writer = pd.ExcelWriter(p, engine='xlsxwriter') # pylint: disable=abstract-class-instantiated
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()

if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2])

