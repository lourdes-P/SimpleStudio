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
from logic.processor.processor import Processor

class VirtualMachine:
    COMPLETE_EXECUTION_MODE = 0
    SINGLE_STEP_EXECUTION_MODE = 1
    N_STEP_EXECUTION_MODE = 2
    
    def __init__(self):
        self.reserved_word_map = ReservedWordMap()
        self._firsts_map = MapManager("resources/firsts.csv")
        self._nexts_map = MapManager("resources/nexts.csv")
        self._operator_precedence_manager = OperatorPrecedenceManager()
        self.code_memory = None
        self.data_memory = None
        self.heap_memory = None
        self.processor = None
        self.io_manager = None
        self.error = None
        self.breakpoint_list = None
        self._label_dictionary = None
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
            # TODO excecution buttons unabled in view
        
        self._label_dictionary = syntactic_analyzer.get_label_dictionary()
        self.initialize_processor()
        
        self.notify_load_finished()
        
    def update_breakpoint_list(self, breakpoint_list):
        self.breakpoint_list = breakpoint_list
        
    def initialize_processor(self):
        if self.processor:
            self.processor.reset()
        else:
            self.processor = Processor()
        
    def notify_load_finished(self):
        for listener in self.listeners:
            listener.load_has_finished()
        
    def notify_error(self):
        for listener in self.listeners:
            listener.trigger_error()
            
    def disable_execution(self):
        for listener in self.listeners:
            listener.disable_execution()
            # TODO
            
    def get_last_triggered_error(self):
        return self.error
    
    def get_code_memory(self):
        return self.code_memory
    
    # TODO get heap, and data memory
    def access_data_memory(self, address):
        return self._data_memory.get_cell(address)
    
    def access_heap_memory(self, address):
        return self._heap_memory.get_cell(address)
    
    def set_data_memory(self, address, data):
        annotation = self.code_memory.get_codecell(address).annotation
        self.data_memory.set_cell(address, data, annotation)
        
    def set_heap_memory(self, address, data):
        annotation = self.code_memory.get_codecell(address).annotation
        self.heap_memory.set_cell(address, data, annotation)
        
    def define_label(self, label_token, address):
        label_name = label_token.lexeme
        if self._label_dictionary.get(label_name) == None:
            self._label_dictionary[label_name] = address
        else:
            pass # TODO
        
    def trigger_user_input(self):
        for listener in self.listeners:
            listener.trigger_user_input()
            # TODO
            
    def deliver_user_input(self, input):
        self._last_user_input = input
        self.processor.deliver_user_input()
        
    def get_user_input(self):
        return self._last_user_input
    
    def get_pc(self):
        return self.processor.pc if self.processor else 0
        
    def execute_program(self, mode, steps = None):
        # TODO obtener breakpoints de la view
        match mode:
            case self.SINGLE_STEP_EXECUTION_MODE:
                self.single_step_execution()
            case self.N_STEP_EXECUTION_MODE:
                self.n_step_execution(steps)
            case self.COMPLETE_EXECUTION_MODE:
                pass
                
        # TODO check if instructions remaining: if there are less than n steps instructions, execute all instructions left
        # TODO unable to execute if all instructions have been executed (unable from view too)
        if not self.io_manager:
            self.error = 'No source loaded'
            self.notify_error()
            
    def single_step_execution(self):
        code = self.processor.execute_next_instruction()
        
    def n_step_execution(self, steps):
        code = self.single_step_execution()
        
        for i in range(steps-1):
            if code != self.processor.SUCCESS or self.breakpoint_list != None and self.get_pc in self.breakpoint_list:
                return
            else:
                code = self.processor.execute_next_instruction()                
                
    
        

                
                    