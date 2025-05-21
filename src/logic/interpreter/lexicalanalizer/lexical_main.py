from lexicalanalizer import LexicalAnalizer
from iomanager.io_manager import IOManager
from reserved_word_manager.reserved_word_map import ReservedWordMap


# lexical analizer (self, io_manager, reserved_word_map)
# io manager (self, file_path)
reserved_word_map = ReservedWordMap()
io_manager = IOManager("./test1.txt")

lexical_analizer = LexicalAnalizer(io_manager, reserved_word_map)
finish = False

while (not finish):
    current_token = lexical_analizer.next_token()
    finish = (current_token.get_lexeme == IOManager.EOF)
    print("[" + current_token.get_token_name + ", " + current_token.get_lexeme + ", " + str(current_token.get_line_number) + "]")

