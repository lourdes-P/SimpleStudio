import csv
import os

class MapManager:

    def __init__(self, file_path):
        self.map = {}

        self.initialize_map(file_path)


    def initialize_map(self, file_path):
        with open(os.path.join(".", file_path), "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 2:
                    if(not self.map.get(row[0])):
                        valueList = []
                        self.map[row[0]] = valueList
                    self.map[row[0]].append(row[1])

        self.flatten_map()


    def flatten_map(self):
        keys = self.map.keys()
        for key in keys:
            value_list_copy = self.map[key].copy()
            for value in value_list_copy:
                if self.map.get(value) != None:
                    self.flatten_nested_list(key, value)


    def flatten_nested_list(self, key, value):
        value_as_key_list = self.map.get(value).copy()
        list_replacement = []
        for value_from_list in value_as_key_list:
            if self.map.get(value_from_list) != None:
                list_replacement.extend(self.flatten_nested_list(value, value_from_list))
            else:
                if self.map.get(key).count(value_from_list) == 0 and value_from_list not in list_replacement:                    
                        list_replacement.append(value_from_list)
        
        set_no_duplicates_replacement = set(list_replacement)
        self.map.get(key).remove(value)
        self.map.get(key).extend(set_no_duplicates_replacement)

        return set_no_duplicates_replacement
    

    def get_value(self, key):
        return self.map.get(key)
    
    def contains_key(self, key):
        return self.map.get(key) != None
    
    def contains_entry(self, production_name, token_name):
        return self.contains_single_entry(production_name, token_name)
    
    def contains_single_entry(self, key, value):
        if self.contains_key(key):
            return self.map.get(key).count(value) != 0
        else:
            return False
        

    def print_map(self):
        print(self.map)

