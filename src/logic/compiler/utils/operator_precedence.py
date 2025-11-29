import csv
import os
from utils.path_normalizer import PathNormalizer

class OperatorPrecedenceManager:
    
    def __init__(self, file_path= os.path.join('resources', 'operatorprecedence.csv')):
        self.operator_precedence_map = {}

        self.initialize_map(PathNormalizer.resource_path(file_path))

    def initialize_map(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 2:                
                    self.operator_precedence_map[row[0]] = row[1]
        
    def get_precedence(self, operator_name):
        return self.operator_precedence_map.get(operator_name)
    
    def contains_operator(self, operator_name):
        return self.operator_precedence_map.get(operator_name) != None
    
    def contains_operator_with_precedence(self, operator_name, precedence):
        if self.contains_key(operator_name):
            return self.map.get(operator_name).count(precedence) != 0
        else:
            return False
        
    def print_map(self):
        print(self.operator_precedence_map)