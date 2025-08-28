import csv
from pathlib import Path

current_dir = Path(__file__).parent
root = current_dir.parent.parent.parent.parent.parent

class ReservedWordMap:
    
    def __init__(self):
        self.reserved_word_map = {}
        self.initialize_map()

    def initialize_map(self):
        with open(root / "resources/reservedwords.csv", "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 2:
                    self.reserved_word_map[row[0]] = row[1]
    
    def get_reserved_word_id(self, word):
        return self.reserved_word_map.get(word.lower())
    
    def is_reserved_word(self, word):
        return word.lower() in self.reserved_word_map
    
    def show_map(self):
        for key, value in self.reserved_word_map.items():
            print(f"{key} = {value}")