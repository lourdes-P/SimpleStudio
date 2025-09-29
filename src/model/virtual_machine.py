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
    ONLY_REGISTER_MODIFIED = False
    SET_MEMORY_MODIFIED = True
    
    def __init__(self):
        self._reserved_word_map = ReservedWordMap()
        self._firsts_map = MapManager("resources/firsts.csv")
        self._nexts_map = MapManager("resources/nexts.csv")
        self._operator_precedence_manager = OperatorPrecedenceManager()
        self._code_memory = None
        self._data_memory = DataMemory()
        self._heap_memory = HeapMemory()  
        self._processor = None
        self._io_manager = None
        self._error = None
        self._breakpoint_list = None
        self._label_dictionary = None
        self._last_execution_added_labels = {}
        self._listeners = []
        self._modified_data_cells = {}
        self._modified_heap_cells = {}
        self._last_executed_instruction_address = 0
        
    def addListener(self, listener) : 
        self._listeners.append(listener)
        
    def load_program(self, file_path):        
        self._io_manager = IOManager(file_path)
        self._code_memory = CodeMemory()
        self._data_memory.reset()
        self._heap_memory.reset()     
        lexical_analyzer = LexicalAnalyzer(self._io_manager, self._reserved_word_map)
        syntactic_analyzer = SyntacticAnalyzer(lexical_analyzer, self._code_memory, self._firsts_map, self._nexts_map, self._operator_precedence_manager)
        try:
            syntactic_analyzer.start()
        except (LexicalException, LexicalExceptionInvalidSymbol, 
            LexicalExceptionInvalidOperator, SyntacticException, 
            SyntacticExceptionNoMatch) as e:
            self._error = e
            self.notify_error()
        
        self._original_label_dictionary = syntactic_analyzer.get_label_dictionary()
        self._label_dictionary = syntactic_analyzer.get_label_dictionary()
        self.initialize_processor()
        
        self.notify_load_finished()
        
    def reset(self):
        # TODO  have to divide the view methods in threads or something
        if self._code_memory is not None:
            self._data_memory.reset()
            self._heap_memory.reset()
            self._processor.reset()
            self._label_dictionary = self._original_label_dictionary.copy()
            self._last_execution_added_labels.clear()
            self._reset_modified_cells()
            self.enable_execution()
            self.notify_reset_finished()
        
    def update_breakpoint_list(self, breakpoint_list):
        self._breakpoint_list = breakpoint_list
        
    def initialize_processor(self):
        if self._processor:
            self._processor.reset()
        else:
            self._processor = Processor(virtual_machine=self)
            
    def _reset_modified_cells(self):
        if self._modified_data_cells.get(self.SET_MEMORY_MODIFIED) is not None:
            self._modified_data_cells[self.SET_MEMORY_MODIFIED].clear()
        else:
            self._modified_data_cells[self.SET_MEMORY_MODIFIED] = []
            
        if self._modified_data_cells.get(self.ONLY_REGISTER_MODIFIED) is not None:
            self._modified_data_cells[self.ONLY_REGISTER_MODIFIED].clear()
        else:
            self._modified_data_cells[self.ONLY_REGISTER_MODIFIED] = []
        
        if self._modified_heap_cells.get(self.SET_MEMORY_MODIFIED) is not None:
            self._modified_heap_cells[self.SET_MEMORY_MODIFIED].clear()
        else:
            self._modified_heap_cells[self.SET_MEMORY_MODIFIED] = []
            
        if self._modified_heap_cells.get(self.ONLY_REGISTER_MODIFIED) is not None:
            self._modified_heap_cells[self.ONLY_REGISTER_MODIFIED].clear()
        else:
            self._modified_heap_cells[self.ONLY_REGISTER_MODIFIED] = []
            
    # --------- notify listeners
        
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
            
    def disable_execution(self):
        for listener in self._listeners:
            listener.disable_execution()
            
    def enable_execution(self):
        for listener in self._listeners:
            listener.enable_execution()
            
    def trigger_user_input(self):
        for listener in self._listeners:
            listener.trigger_user_input()
            
    # --------- notify listeners (END)
            
    def get_last_triggered_error(self):
        return self._error
    
    def get_last_executed_instruction_address(self):
        return self._last_executed_instruction_address
    
    def get_instruction(self, address):
        return self._code_memory.get_instruction(address)
    
    def get_code_memory(self):
        return self._code_memory
    
    def get_data_memory(self):
        return self._data_memory
    
    def get_heap_memory(self):
        return self._heap_memory
    
    def get_modified_data_cells(self):
        return self._modified_data_cells
    
    def get_modified_heap_cells(self):
        return self._modified_heap_cells
    
    def get_user_input(self):
        return self._last_user_input
    
    def get_label_dictionary(self):
        return self._label_dictionary
    
    def get_last_execution_added_labels(self):
        return self._last_execution_added_labels
    
    def get_pc(self):
        return self._processor.pc if self._processor != None else 0
    
    def get_libre(self):
        return self._processor.libre if self._processor != None else 0
    
    def get_actual(self):
        return self._processor.actual if self._processor != None else 0
    
    def get_po(self):
        return self._processor.po if self._processor != None else 0
    
    def get_label_address(self, label_name):
        address = self._label_dictionary.get(str.lower(label_name))
        if address == None:
            self._error = f"Label with name {label_name} does not exist"
            self.notify_error()
        return address
    
    def access_data_memory(self, address):
        return self._data_memory.get_cell(address).value
    
    def access_heap_memory(self, address):
        return self._heap_memory.get_cell(address).value
    
    def set_data_memory(self, address, data = None, source_instruction_address = None):
        annotation = None
        if source_instruction_address is not None:
            annotation = self._code_memory.get_codecell(source_instruction_address).annotation
        modified_cell = self._data_memory.set_cell(address, data, annotation)
        self._add_to_modified_cell_dictionary(self._modified_data_cells, self.SET_MEMORY_MODIFIED, modified_cell)
        
    def set_heap_memory(self, address, data = None, source_instruction_address = None):
        annotation = None
        if source_instruction_address is not None:
            annotation = self._code_memory.get_codecell(source_instruction_address).annotation
        modified_cell = self._heap_memory.set_cell(address, data, annotation)
        self._add_to_modified_cell_dictionary(self._modified_heap_cells, self.SET_MEMORY_MODIFIED, modified_cell)
        
    def set_libre(self, former_libre, libre):
        former = self._data_memory.get_cell(former_libre)
        former.remove_libre()
        new = self._data_memory.get_cell(libre)
        new.place_libre()
        self._add_to_modified_cell_dictionary(self._modified_data_cells, self.ONLY_REGISTER_MODIFIED, former)
        self._add_to_modified_cell_dictionary(self._modified_data_cells, self.ONLY_REGISTER_MODIFIED, new)
        
    def set_actual(self, former_actual, actual):
        former = self._data_memory.get_cell(former_actual)
        former.remove_actual()
        new = self._data_memory.get_cell(actual)
        new.place_actual()
        self._add_to_modified_cell_dictionary(self._modified_data_cells, self.ONLY_REGISTER_MODIFIED, former)
        self._add_to_modified_cell_dictionary(self._modified_data_cells, self.ONLY_REGISTER_MODIFIED, new)
       
    def set_po(self, former_po, po):
        former = self._heap_memory.get_cell(former_po)
        former.remove_po()
        new = self._heap_memory.get_cell(po)
        new.place_po()
        self._add_to_modified_cell_dictionary(self._modified_heap_cells, self.ONLY_REGISTER_MODIFIED, former)
        self._add_to_modified_cell_dictionary(self._modified_heap_cells, self.ONLY_REGISTER_MODIFIED, new)
        
    def define_label(self, label_token, address):
        label_name = str.lower(label_token.lexeme)
        if self._original_label_dictionary.get(label_name) == None:  
            self._label_dictionary[label_name] = address
            self._last_execution_added_labels[label_name] = address
            return Processor.SUCCESS
        else:
            self._error = f"Label with name {label_name} is already defined in the code memory."
            self.notify_error()
            return Processor.FAILURE
            
    def deliver_user_input(self, input):
        self._last_user_input = input
        self._processor.deliver_user_input()
        
    def execute_program(self, mode, steps : int = None):
        self._reset_modified_cells()
        self._last_execution_added_labels.clear()
        state = Processor.SUCCESS
        
        if not self._io_manager:
            self._error = 'No source loaded'
            self.notify_error()
            
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
        self._last_executed_instruction_address = self.get_pc()
        state = self._processor.execute_next_instruction()
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
            pass # TODO ver si deberia hacer algo mas (ya se deshabilita)
        elif state == Processor.FAILURE:
            self._error = "Error while executing source code"   
            self.notify_error()
            
    def _add_to_modified_cell_dictionary(self, dictionary, key, cell):
        if dictionary.get(key) is not None:
            dictionary[key].append(cell)
            
    def _in_breakpoint_list(self, address : int):
        return self._breakpoint_list != None and address in self._breakpoint_list