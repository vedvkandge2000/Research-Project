# Research-Project
### Packages required
* pandas == 1.1.5
* xlswriter == 1.7.6 

To install xlswrite
```
pip3 install xlswriter
```
### Run
```
python3 Data_separation.py <Data_set(JSON FILE)> <PATH (WHERE FOLDERS WILL BE CREATED)>
```
### To create ontology.json Run 
```
python3 make_ontology.py <Data_set(JSON FILE) (localization.json)> <PATH (WHERE FILE WILL BE CREATED)>
```
### To create h_attraction folder Run 
```
python3 h_data_separation_attraction.py <Data_set(FOLDER PATH of attraction)>  <Map_File_Path(JSON FILE) (localization.json)>  <PATH (WHERE _attraction FOLDER WILL BE CREATED)>
```