from logic.interpreter.lexicalanalizer.lexicalanalizer import LexicalAnalizer
from logic.interpreter.iomanager.io_manager import IOManager
from logic.interpreter.lexicalanalizer.reserved_word_manager.reserved_word_map import ReservedWordMap
from logic.interpreter.lexicalanalizer.lexicalexceptions.lexicalexception import LexicalException
from logic.interpreter.lexicalanalizer.lexicalexceptions.lexicalexception_invalidoperator import LexicalExceptionInvalidOperator
from logic.interpreter.lexicalanalizer.lexicalexceptions.lexicalexception_invalidsymbol import LexicalExceptionInvalidSymbol
from logic.interpreter.syntacticanalizer.syntacticanalizer import SyntanticAnalizer
from logic.interpreter.syntacticanalizer.syntacticexceptions import *

# lexical analizer (self, io_manager, reserved_word_map)
# io manager (self, file_path)
reserved_word_map = ReservedWordMap()
io_manager = IOManager("./test1.txt")

lexical_analizer = LexicalAnalizer(io_manager, reserved_word_map)
syntactic_analizer = SyntanticAnalizer(lexical_analizer)
finish = False

try:
    syntactic_analizer.start()
except LexicalException as e:
    print(e)
except LexicalExceptionInvalidSymbol as e:
    print(e)
except LexicalExceptionInvalidOperator as e:
    print(e)
except SyntacticException as e:
    print(e)
except SyntacticExceptionNoMatch as e:
    print(e)
    
if lexical_analizer.no_errors and syntactic_analizer.no_errors:
    print("execution successful")
    

