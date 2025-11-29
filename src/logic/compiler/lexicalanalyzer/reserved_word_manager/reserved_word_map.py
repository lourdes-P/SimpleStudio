import csv
import os
from utils.path_normalizer import PathNormalizer

class ReservedWordMap:
    
    def __init__(self, file_path = os.path.join("resources","reservedwords.csv")):
        self.reserved_word_map = {}
        self.name_word_map = {}
        self.initialize_map(PathNormalizer.resource_path(file_path))

    def initialize_map(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 2:
                    self.reserved_word_map[row[0]] = row[1]
                    self.name_word_map[row[1]] = row[0]    
                    
    def get_reserved_word_id(self, word):
        return self.reserved_word_map.get(word.lower())
    
    def is_reserved_word(self, word):
        return word.lower() in self.reserved_word_map
    
    def get_reserved_word_from_id(self, word_id):
        return self.name_word_map.get(word_id.lower())
    
    def map_list_from_id_to_name(self, reserved_word_id_iterable):
        reserved_word_list = []
        for word_id in reserved_word_id_iterable:
            reserved_word = self.get_reserved_word_from_id(word_id)
            if reserved_word:
                reserved_word_list.append(reserved_word)
            else:
                reserved_word_list.append(word_id)
            
        return reserved_word_list
    
    def show_map(self):
        for key, value in self.reserved_word_map.items():
            print(f"{key} = {value}")