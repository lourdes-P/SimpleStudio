from logic.interpreter.utils.mapmanager import MapManager
import csv
from pathlib import Path

current_dir = Path(__file__).parent
root = current_dir.parent.parent.parent.parent

class OperatorPrecedenceManager:
    
    def __init__(self):
        self.operator_precedence_map = {}

        self.initialize_map('resources/operatorprecedence.csv')      

    def initialize_map(self, file_path):
        with open(root / file_path, "r", encoding="utf-8") as file:
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