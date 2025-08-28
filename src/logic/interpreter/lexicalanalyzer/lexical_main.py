from logic.interpreter.lexicalanalyzer.lexicalanalyzer import LexicalAnalyzer
from logic.interpreter.iomanager.io_manager import IOManager
from logic.interpreter.lexicalanalyzer.reserved_word_manager.reserved_word_map import ReservedWordMap
from logic.interpreter.lexicalanalyzer.lexicalexceptions.lexicalexception import LexicalException
from logic.interpreter.lexicalanalyzer.lexicalexceptions.lexicalexception_invalidoperator import LexicalExceptionInvalidOperator
from logic.interpreter.lexicalanalyzer.lexicalexceptions.lexicalexception_invalidsymbol import LexicalExceptionInvalidSymbol
from logic.interpreter.syntacticanalyzer.syntacticanalyzer import SyntacticAnalyzer
from logic.interpreter.syntacticanalyzer.syntacticexceptions import *
from logic.memories.codememory.codememory import CodeMemory

# lexical analizer (self, io_manager, reserved_word_map)
# io manager (self, file_path)
reserved_word_map = ReservedWordMap()
io_manager = IOManager("./test1.txt")
codememory = CodeMemory()
lexical_analizer = LexicalAnalyzer(io_manager, reserved_word_map, codememory)
syntactic_analizer = SyntacticAnalyzer(lexical_analizer)
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
    codememory.print_memory()
    

