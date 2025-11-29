from logic.expression_ast.exceptions.invalid_memory_access_operand_exception import InvalidMemoryAccessOperandException
from logic.expression_ast.exceptions.invalid_operator_exception import InvalidOperatorException
from logic.compiler.lexicalanalyzer.lexicalanalyzer import LexicalAnalyzer
from logic.compiler.lexicalanalyzer.lexicalexceptions.lexicalexception import LexicalException
from logic.compiler.lexicalanalyzer.lexicalexceptions.lexicalexception_invalidoperator import LexicalExceptionInvalidOperator
from logic.compiler.lexicalanalyzer.lexicalexceptions.lexicalexception_invalidsymbol import LexicalExceptionInvalidSymbol
from logic.compiler.syntacticanalyzer.syntacticanalyzer import SyntacticAnalyzer
from logic.compiler.syntacticanalyzer.syntacticexceptions import *
from logic.compiler.iomanager.io_manager import IOManager
from logic.compiler.lexicalanalyzer.reserved_word_manager.reserved_word_map import ReservedWordMap
from logic.compiler.utils import MapManager, OperatorPrecedenceManager

class ProgramLoader:
    LOAD_FAILURE = 0
    LOAD_SUCCESS = 1
    
    def __init__(self, memory_manager, label_manager, vm_error_handler):
        self._reserved_word_map = ReservedWordMap()
        self._firsts_map = MapManager("resources/firsts.csv")
        self._nexts_map = MapManager("resources/nexts.csv")
        self._operator_precedence_manager = OperatorPrecedenceManager()
        self._io_manager = IOManager()
        
        self._memory_manager = memory_manager
        self._label_manager = label_manager
        self._vm_error_handler = vm_error_handler
    
    def load_program(self, file_path):        
        code_memory = self._memory_manager.get_code_memory(new_memory=True)
        try:
            self._io_manager.load_code(file_path)
            lexical_analyzer = LexicalAnalyzer(self._io_manager, self._reserved_word_map)
            syntactic_analyzer = SyntacticAnalyzer(lexical_analyzer, code_memory, self._firsts_map, self._nexts_map, self._operator_precedence_manager)
            syntactic_analyzer.start()
            self._label_manager.set_label_dictionary(syntactic_analyzer.get_label_dictionary())
            return self.LOAD_SUCCESS
        except (LexicalExceptionInvalidSymbol, 
            LexicalExceptionInvalidOperator, LexicalException, 
            SyntacticException, SyntacticExceptionNoMatch, 
            SimpleSyntacticException, InvalidOperatorException,
            InvalidMemoryAccessOperandException, Exception) as e:
            if self._io_manager:
                self._io_manager.close()
            self._memory_manager.erase_code_memory()
            self._vm_error_handler.set_error(e)
            return self.LOAD_FAILURE
        
    def set_reserved_word_map(self, reserved_word_map):
        self._reserved_word_map = reserved_word_map
        
    def set_firsts_map(self, firsts_map):
        self._firsts_map = firsts_map
        
    def set_nexts_map(self, nexts_map):
        self._nexts_map = nexts_map
        
    def set_operator_precedence_manager(self, operator_precedence_manager):
        self._operator_precedence_manager = operator_precedence_manager
        
    def set_io_manager(self, io_manager):
        self._io_manager = io_manager