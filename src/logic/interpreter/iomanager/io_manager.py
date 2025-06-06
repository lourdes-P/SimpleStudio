import os
class IOManager:
    EOF = ''
    END_OF_LINE = '\n'

    def __init__(self, file_path):
        self.current_char =' '
        self.line_number= 1
        self.line_char_index= 1
        self.line = ""
        relative_path = os.path.join(os.path.dirname(__file__), file_path)

        self.file_reader = open(relative_path, "r", encoding="utf-8")

    def get_next_char(self):
        if (self.current_char == self.END_OF_LINE):
            self.line_number+= 1
            self.line_char_index = 1
            self.line = ""
            
        if (self.current_char != self.EOF):
            self.current_char= self.file_reader.read(1)                    
        
        if (self.current_char == self.EOF):            
            self.file_reader.close()
        elif (self.current_char != self.END_OF_LINE):                                
            self.line += self.current_char
            self.line_char_index += 1

        return self.current_char

    @property
    def get_line_number(self):
        return self.line_number
    
    @property
    def get_line_char_index(self):
        return self.line_char_index
    
    def get_current_line(self):
        return self.line
    
    ## TODO get_whole_line (una vez que se encuentra un error, leo toda la línea, para devolverla)
    