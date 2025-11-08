import os
import linecache

class IOManager:
    EOF = ''
    END_OF_LINE = '\n'

    def __init__(self, file_path):
        self.current_char =' '
        self.line_number= 1
        self.line_char_index= 0
        self.line = ""
        self.relative_path = os.path.join(os.path.dirname(__file__), file_path)

        self.file_reader = open(self.relative_path, "r", encoding="utf-8")

    def get_next_char(self):
        if self.current_char == self.END_OF_LINE:
            self.line_number+= 1
            self.line_char_index = 0
            self.line = ""
            
        if self.current_char != self.EOF:
            self.current_char= self.file_reader.read(1)
            
        if self.current_char == self.EOF:
            self.file_reader.close()
        elif self.current_char != self.END_OF_LINE:
            self.line += self.current_char
            self.line_char_index += 1

        return self.current_char

    def close(self):
        if self.file_reader:
            self.file_reader.close()
            
    @property
    def get_line_number(self):
        return self.line_number
    
    @property
    def get_line_char_index(self):
        return self.line_char_index
    
    def get_current_line(self):
        return self.line
    
    def get_whole_current_line(self):
        return linecache.getline(self.relative_path, self.line_number).removesuffix(self.END_OF_LINE)
    
    def get_whole_line(self, line_number):  # line number from 1 to n
        return linecache.getline(self.relative_path, line_number).removesuffix(self.END_OF_LINE)
    