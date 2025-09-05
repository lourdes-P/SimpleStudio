from logic.interpreter.lexicalanalyzer.lexicalanalyzer import LexicalAnalyzer
from logic.interpreter.iomanager.io_manager import IOManager
from logic.interpreter.lexicalanalyzer.reserved_word_manager.reserved_word_map import ReservedWordMap
from logic.interpreter.lexicalanalyzer.lexicalexceptions.lexicalexception import LexicalException
from logic.interpreter.lexicalanalyzer.lexicalexceptions.lexicalexception_invalidoperator import LexicalExceptionInvalidOperator
from logic.interpreter.lexicalanalyzer.lexicalexceptions.lexicalexception_invalidsymbol import LexicalExceptionInvalidSymbol
from logic.interpreter.syntacticanalyzer.syntacticanalyzer import SyntacticAnalyzer
from logic.interpreter.syntacticanalyzer.syntacticexceptions import *
from logic.memories.codememory.codememory import CodeMemory

class VirtualMachine:
    def __init__(self):
        self.reserved_word_map = ReservedWordMap()
        self.code_memory = None
        self.io_manager = None
        self.error = None
        self.D_memory = {}
        self.H_memory = {}
        self.listeners = []     # TODO listeners
        
    def addListener(self, listener) : 
        self.listeners.append(listener)
        
    def load_program(self, file_path):        
        self.io_manager = IOManager(file_path)
        self.code_memory = CodeMemory()
        lexical_analyzer = LexicalAnalyzer(self.io_manager, self.reserved_word_map)
        syntactic_analyzer = SyntacticAnalyzer(lexical_analyzer, self.code_memory)
        try:
            syntactic_analyzer.start()
        except (LexicalException, LexicalExceptionInvalidSymbol, 
            LexicalExceptionInvalidOperator, SyntacticException, 
            SyntacticExceptionNoMatch) as e:
            self.error = e
            self.notify_error()
        
        self.notify_load_finished()
        
    def notify_load_finished(self):
        for listener in self.listeners:
            listener.load_has_finished()
        
    def notify_error(self):
        for listener in self.listeners:
            listener.trigger_error()
            
    def get_last_triggered_error(self):
        return self.error
    
    def get_code_memory(self):
        return self.code_memory
    
    # TODO get heap, and data memory
        
    def execute_program(self):
        # TODO
        if not self.io_manager:
            self.error = 'No source loaded'
            self.notify_error()
                    