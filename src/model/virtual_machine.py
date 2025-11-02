from logic.interpreter.lexicalanalyzer.lexicalanalyzer import LexicalAnalyzer
from logic.interpreter.iomanager.io_manager import IOManager
from logic.interpreter.lexicalanalyzer.reserved_word_manager.reserved_word_map import ReservedWordMap
from logic.interpreter.lexicalanalyzer.lexicalexceptions.lexicalexception import LexicalException
from logic.interpreter.lexicalanalyzer.lexicalexceptions.lexicalexception_invalidoperator import LexicalExceptionInvalidOperator
from logic.interpreter.lexicalanalyzer.lexicalexceptions.lexicalexception_invalidsymbol import LexicalExceptionInvalidSymbol
from logic.interpreter.syntacticanalyzer.syntacticanalyzer import SyntacticAnalyzer
from logic.interpreter.syntacticanalyzer.syntacticexceptions import *
from logic.interpreter.utils import MapManager, OperatorPrecedenceManager
from logic.processor.processor import Processor
from model.cache.cache import Cache
from model.label_manager import LabelManager
from model.memory_manager import MemoryManager
from model.exceptions.empty_cache_exception import EmptyCacheException

class VirtualMachine:
    COMPLETE_EXECUTION_MODE = 0
    SINGLE_STEP_EXECUTION_MODE = 1
    N_STEP_EXECUTION_MODE = 2
    
    def __init__(self):
        self._reserved_word_map = ReservedWordMap()
        self._firsts_map = MapManager("resources/firsts.csv")
        self._nexts_map = MapManager("resources/nexts.csv")
        self._operator_precedence_manager = OperatorPrecedenceManager()
        self._label_manager = LabelManager()
        self._memory_manager = MemoryManager()
        self._cache = Cache(10)
        self._processor = None
        self._io_manager = None
        self._error = None
        self._breakpoint_list = None
        self._listeners = []
        self._last_executed_instruction_address = None
        self._last_output_text = ''
        
    def addListener(self, listener) : 
        self._listeners.append(listener)
        
    def load_program(self, file_path):        
        self._io_manager = IOManager(file_path)
        code_memory = self._memory_manager.get_code_memory(new_memory=True)
        try:
            lexical_analyzer = LexicalAnalyzer(self._io_manager, self._reserved_word_map)
            syntactic_analyzer = SyntacticAnalyzer(lexical_analyzer, code_memory, self._firsts_map, self._nexts_map, self._operator_precedence_manager)
            syntactic_analyzer.start()
            self._label_manager.set_label_dictionary(syntactic_analyzer.get_label_dictionary())
            self._initialize_processor()
            self.notify_load_finished()
        except (LexicalException, LexicalExceptionInvalidSymbol, 
            LexicalExceptionInvalidOperator, SyntacticException, 
            SyntacticExceptionNoMatch, SimpleSyntacticException, Exception) as e:  # TODO ver estas excepciones catcheadas
            self._error = e
            self.notify_error()
            return
        
    def reset(self, on_load = True):
        if self._memory_manager.there_is_code_memory():
            self._label_manager.reset(on_load)
            self._last_executed_instruction_address = None
            self._cache.reset()
            self._memory_manager.reset()
            if not on_load:
                self._initialize_processor()
            else:
                self._breakpoint_list = None
            self.notify_reset_finished()
        
    def reset_all_time_modified_cells(self):
        self._memory_manager.reset_all_time_modified_cells()
            
    def undo(self):
        try:
            cache_entry = self._cache.pop()
        except EmptyCacheException as e:
            self._error = e
            self.notify_error()
            return
        self._label_manager.reset()
        self._memory_manager.reset(only_modified_cells= True)
        self._last_executed_instruction_address = cache_entry.get_last_executed_instruction_address()
        self._processor.reinstate_pc(cache_entry.get_pc())
        self._memory_manager.undo_memory_modified_data_cells(cache_entry.get_memory_modified_data_cells())
        self._memory_manager.undo_register_modified_data_cells(self._processor, cache_entry.get_register_modified_data_cells())
        self._memory_manager.undo_memory_modified_heap_cells(cache_entry.get_memory_modified_heap_cells())
        self._memory_manager.undo_register_modified_heap_cells(self._processor, cache_entry.get_register_modified_heap_cells())
        self._label_manager.undo_label_modification(cache_entry.get_label_added_entry())
        self._processor.enable()
        
        self.notify_undo_finished()
     
    def update_breakpoint_list(self, breakpoint_list):
        self._breakpoint_list = breakpoint_list
            
    def deliver_user_input(self, input):
        self._last_user_input = input
        self._processor.deliver_user_input()
        
    def execute_program(self, mode, steps : int = None):
        self._memory_manager.reset(only_modified_cells=True)
        self._label_manager.clear_last_execution_added_labels()
        state = Processor.SUCCESS
        
        if not self._io_manager:
            self._error = 'No source loaded'
            self.notify_error()
            return
            
        match mode:
            case self.SINGLE_STEP_EXECUTION_MODE:
                state = self._single_step_execution()
            case self.N_STEP_EXECUTION_MODE:
                state = self._n_step_execution(steps)
            case self.COMPLETE_EXECUTION_MODE:
                state = self._complete_execution()
                
        self._check_execution_state(state)
                
        self.notify_execution_finished()
            
    def _single_step_execution(self):
        pc = self.get_pc()
        self._cache.create_and_push_entry(self._last_executed_instruction_address, pc)
        state = self._processor.execute_next_instruction()
        self._last_executed_instruction_address = pc
            
        return state
        
    def _n_step_execution(self, steps : int):
        state = self._single_step_execution()
        steps-= 1
        while steps > 0 and state == Processor.SUCCESS and not (self._in_breakpoint_list(self.get_pc())):
            state = self._single_step_execution()     
            steps-= 1
        
        return state
                
    def _complete_execution(self):
        state = self._single_step_execution()
        while state == Processor.SUCCESS and not (self._in_breakpoint_list(self.get_pc())):
            state = self._single_step_execution()
        
        return state
            
    def _check_execution_state(self, state):
        if state == Processor.COMPLETED:
            pass 
        elif state == Processor.FAILURE:
            error = self._processor.get_error()
            if error is not None:
                self._error = error
            else:
                self._error = "Error while executing source code"   
            self.notify_error()
    
    def _initialize_processor(self):
        if self._processor:
            self._processor.reset()
        else:
            self._processor = Processor(virtual_machine=self)
         
    def _in_breakpoint_list(self, address : int):
        return self._breakpoint_list != None and address in self._breakpoint_list
    
    # --------- PROCESSOR use
    
    def access_data_memory(self, address):
        return self._memory_manager.access_data_memory(address)
    
    def access_heap_memory(self, address):
        return self._memory_manager.access_heap_memory(address)
    
    def set_data_memory(self, address, data = None, source_instruction_address = None):
        self._memory_manager.set_data_memory(self._cache, address, data, source_instruction_address)
        
    def set_heap_memory(self, address, data = None, source_instruction_address = None):
        self._memory_manager.set_heap_memory(self._cache, address, data, source_instruction_address)
        
    def set_libre(self, former_libre, libre):
        self._memory_manager.set_libre(self._cache.peek(), former_libre, libre)
        
    def set_actual(self, former_actual, actual):
        self._memory_manager.set_actual(self._cache.peek(), former_actual, actual)
       
    def set_po(self, former_po, po):
        self._memory_manager.set_po(self._cache.peek(), former_po, po)
        
    def define_label(self, label_token, address):
        response = self._label_manager.define_label(label_token, address, cache=self._cache)
        if response == Processor.SUCCESS:
            return response
        else:
            self._error = response
            self.notify_error()
            return Processor.FAILURE
        
    def print_output(self, text):
        self._last_output_text = text
        self.notify_output()
        
    # processor use END ---------
    # --------- notify LISTENERS
        
    def notify_load_finished(self):
        for listener in self._listeners:
            listener.load_has_finished()
        
    def notify_error(self):
        for listener in self._listeners:
            listener.trigger_error()
            
    def notify_execution_finished(self):
        for listener in self._listeners:
            listener.execution_finished()
            
    def notify_reset_finished(self):
        for listener in self._listeners:
            listener.reset_has_finished()
            
    def notify_undo_finished(self):
        for listener in self._listeners:
            listener.undo_has_finished()
            
    def notify_output(self):
        for listener in self._listeners:
            listener.print_output()
            
    def disable_execution(self):
        for listener in self._listeners:
            listener.disable_execution()
            
    def enable_execution(self):
        for listener in self._listeners:
            listener.enable_execution()
            
    def trigger_user_input(self):
        for listener in self._listeners:
            listener.trigger_user_input()
            
    # notify listeners END ---------
    # --------- GETTERS
    
    def get_instruction(self, address):
        return self._memory_manager.get_instruction(address)
    
    def get_modified_data_cells(self):
        return self._memory_manager.get_modified_data_cells()
    
    def get_modified_heap_cells(self):
        return self._memory_manager.get_modified_heap_cells()
    
    def get_all_time_modified_data_cells_addresses(self):
        return self._memory_manager.get_all_time_modified_data_cells_addresses()
    
    def get_all_time_modified_heap_cells_addresses(self):
        return self._memory_manager.get_all_time_modified_heap_cells_addresses()
    
    def get_pc(self):
        return self._processor.pc if self._processor != None else 0
    
    def get_label_address(self, label_name):
        address = self._label_manager.get_label_address(label_name)
        if address == None:
            self._error = f"Label with name {label_name} does not exist"
            self.notify_error()
            return
        return address
    
    def get_last_triggered_error(self):
        return self._error
    
    def get_last_executed_instruction_address(self):
        return self._last_executed_instruction_address
    
    def get_user_input(self):
        return self._last_user_input
    
    def get_label_dictionary(self):
        return self._label_manager.get_label_dictionary()
    
    def get_last_execution_added_labels(self):
        return self._label_manager.get_last_execution_added_labels()
    
    def get_last_output(self):
        return self._last_output_text
    
    def get_deleted_label_name(self):
        return self._label_manager.get_deleted_label_name()
    
    def get_cache_size(self):
        return self._cache.size()
    
    def get_code_memory(self):
        return self._memory_manager.get_code_memory()
    
    def get_data_memory(self):
        return self._memory_manager.get_data_memory()
    
    def get_heap_memory(self):
        return self._memory_manager.get_heap_memory()