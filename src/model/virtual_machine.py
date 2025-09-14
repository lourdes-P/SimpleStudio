from logic.interpreter.lexicalanalyzer.lexicalanalyzer import LexicalAnalyzer
from logic.interpreter.iomanager.io_manager import IOManager
from logic.interpreter.lexicalanalyzer.reserved_word_manager.reserved_word_map import ReservedWordMap
from logic.interpreter.lexicalanalyzer.lexicalexceptions.lexicalexception import LexicalException
from logic.interpreter.lexicalanalyzer.lexicalexceptions.lexicalexception_invalidoperator import LexicalExceptionInvalidOperator
from logic.interpreter.lexicalanalyzer.lexicalexceptions.lexicalexception_invalidsymbol import LexicalExceptionInvalidSymbol
from logic.interpreter.syntacticanalyzer.syntacticanalyzer import SyntacticAnalyzer
from logic.interpreter.syntacticanalyzer.syntacticexceptions import *
from logic.memories.codememory.codememory import CodeMemory
from logic.interpreter.utils import MapManager, OperatorPrecedenceManager
from logic.memories.datamemory.data_memory import DataMemory
from logic.memories.heapmemory.heap_memory import HeapMemory

class VirtualMachine:
    def __init__(self):
        self.reserved_word_map = ReservedWordMap()
        self._firsts_map = MapManager("resources/firsts.csv")
        self._nexts_map = MapManager("resources/nexts.csv")
        self._operator_precedence_manager = OperatorPrecedenceManager()
        self.code_memory = None
        self.data_memory = None
        self.heap_memory = None
        self.io_manager = None
        self.error = None
        self.D_memory = {}
        self.H_memory = {}
        self.listeners = []     
        
    def addListener(self, listener) : 
        self.listeners.append(listener)
        
    def load_program(self, file_path):        
        self.io_manager = IOManager(file_path)
        self.code_memory = CodeMemory()
        self.data_memory = DataMemory()
        self.heap_memory = HeapMemory()
        lexical_analyzer = LexicalAnalyzer(self.io_manager, self.reserved_word_map)
        syntactic_analyzer = SyntacticAnalyzer(lexical_analyzer, self.code_memory, self._firsts_map, self._nexts_map, self._operator_precedence_manager)
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
    def access_data_memory(self, address):
        return self._data_memory.get_cell(address)
    
    def access_heap_memory(self, address):
        return self._heap_memory.get_cell(address)
        
    def execute_program(self, mode, steps = None):
        # TODO obtener breakpoints de la view
        # TODO check if instructions remaining: if there are less than n steps instructions, execute all instructions left
        # TODO unable to execute if all instructions have been executed (unable from view too)
        if not self.io_manager:
            self.error = 'No source loaded'
            self.notify_error()
                    