# Importing required packages
import os
import json
import sys

# Reading data from json file
def load_data(data_path):
    with open(data_path, "r", encoding="utf-8") as json_data:
        data = json.load(json_data)
    return data


# creating mapping for English to hindi
def create_mapping(mapping_file_path):
    """
    This function create a mapping from english to hindi.
    
    paramerters: mapping_file_path --> path of file in which english and hindi mapping is present
                          
    """
    
    with open(mapping_file_path, "r", encoding="utf-8") as json_data:
        data = json.load(json_data)
    english = data["english-attraction-original"]
    hindi = data["hindi-attraction-original"]
    map_name = {english[i]["name"]: hindi[i]["name"] for i in range(len(english))}
    map_type = {english[i]["type"]: hindi[i]["type"] for i in range(len(english))}
    map_area = {english[i]["area"]: hindi[i]["area"] for i in range(len(english))}
    return map_name,map_type,map_area



# Function to create different files and folder depending on goals
def write_to_file(folder_name,file_name,data,root):
    """
    This function will find or create a files and folder and write the data in passed file_name
    
    paramerters: folder_name --> Name of folder in which file is present or want to create
                 file_name --> Name of file in which want to write the content
                 data ---> Data which we want to be write in file
                 root ---> root path to directory
                 
    """
    path = os.path.join(root,"h_"+folder_name)
    if not os.path.exists(path):
        os.makedirs(path)
    file_path = os.path.join(path,file_name)
    with open(file_path,'w', encoding="utf-8") as f:
        json.dump(data,f, indent=3, ensure_ascii=False)
    f.close()
    

def main(data_path, mapping_file_path, root_path):
    

    """
    parameters: data_path ---> Path of the data file which we want to read
                mapping_file_path ---> path of file in which english and hindi mapping is present
                root_path ---> path for root directory where all data folders will be created.
    """

    map_name_dict, map_type_dict, map_area_dict = create_mapping(mapping_file_path)

    files = os.listdir(data_path)
    for each_file in files:
        file_path = os.path.join(data_path,each_file)
        
        data = load_data(file_path)
        
        # Creating root diretory
        if not os.path.isdir(root_path):
            os.makedirs(root_path)   
        
        # updating attraction goal (mapping english data to hindi data)
        for key in data["goal"]["attraction"]:
            if (key != "reqt"):
                for keys in data["goal"]["attraction"][key]:
                    if(keys == "type"):
                        data["goal"]["attraction"][key][keys] = map_type_dict[data["goal"]["attraction"][key][keys]]
                    elif(keys == "area"):
                        data["goal"]["attraction"][key][keys] = map_area_dict[data["goal"]["attraction"][key][keys]]
                    elif(keys == "name"):
                        data["goal"]["attraction"][key][keys] = map_name_dict[data["goal"]["attraction"][key][keys]]
        goal_dict = {
            "attraction": data["goal"]["attraction"],
            "taxi": data["goal"]["taxi"],
            "restaurant": data["goal"]["restaurant"]
        }

        # Updating log part of file (mapping english data to hindi data)
        log = []
        for j,dic in enumerate(data["log"]):
                if(j % 2 != 0):
                    log.append(dic)
                else:
                    keys =[]
                    values = []
                    for each_dialog_act in dic["dialog_act"]:
                        keys.append(each_dialog_act)  
                        temp_dialog_act = []
                        for l in dic["dialog_act"][each_dialog_act]:
                            if(l[0] == "type"):
                                if(l[1] not in map_type_dict.keys()):
                                    temp_list = [l[0],l[1]]
                                else:
                                    temp_list = [l[0], map_type_dict[l[1]]]
                            elif(l[0] == "area"):
                                if(l[1] not in map_area_dict.keys()):
                                    temp_list = [l[0],l[1]]
                                else:
                                    temp_list = [l[0], map_area_dict[l[1]]]
                            elif(l[0] == "name"):
                                if(l[1] not in map_name_dict.keys()):
                                    temp_list = [l[0],l[1]]
                                else:
                                    temp_list = [l[0], map_name_dict[l[1]]]
                            else:
                                temp_list = [l[0],l[1]]
                            temp_dialog_act.append(temp_list)
                        values.append(temp_dialog_act)
                    temp = {keys[i]: values[i] for i in range(len(keys))}
                    temp_span_list = []
                    for l in dic["span_info"]:
                        temp_list2 = []
                        if(l[1] == "type"):
                            if(l[2] not in map_type_dict.keys()):
                                temp_list2 = [l[1],l[2]]
                            else:
                                temp_list2 = [l[1], map_type_dict[l[2]]]
                        elif(l[1] == "area"):
                            if(l[2] not in map_area_dict.keys()):
                                temp_list2 = [l[1],l[2]]
                            else:
                                temp_list2 = [l[1], map_area_dict[l[2]]]
                        elif(l[1] == "name"):
                            if(l[2] not in map_name_dict.keys()):
                                temp_list2 = [l[1],l[2]]
                            else:
                                temp_list2 = [l[1], map_name_dict[l[2]]]
                        else:
                            temp_list2 = [l[1],l[2]]
                        temp_span_list.append(temp_list2)

                    log_dict = {"text":dic["text"], "dialog_act":temp, "span_info":temp_span_list, "metadata": dic["metadata"]}
                    log.append(log_dict)
                   
        data_dictionary = {"goal": goal_dict, "log": log}
        write_to_file("attraction",each_file, data_dictionary,root_path)
        

if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2], sys.argv[3])

