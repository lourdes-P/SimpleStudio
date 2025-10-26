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
from model.cache.cache import Cache
from model.utils.modified_cell_manager import ModifiedCellManager
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
        self._code_memory = None
        self._data_memory = DataMemory()
        self._heap_memory = HeapMemory()
        self._cache = Cache(10)
        self._processor = None
        self._io_manager = None
        self._error = None
        self._breakpoint_list = None
        self._label_dictionary = None
        self._last_execution_added_labels = {}
        self._listeners = []
        self._modified_cell_manager = ModifiedCellManager()
        self._all_time_modified_data_cells_addresses = []
        self._all_time_modified_heap_cells_addresses = []
        self._last_executed_instruction_address = None
        self._last_output_text = ''
        self._deleted_label_name = None
        
    def addListener(self, listener) : 
        self._listeners.append(listener)
        
    def load_program(self, file_path):        
        self._io_manager = IOManager(file_path)
        self._code_memory = CodeMemory()   
        try:
            lexical_analyzer = LexicalAnalyzer(self._io_manager, self._reserved_word_map)
            syntactic_analyzer = SyntacticAnalyzer(lexical_analyzer, self._code_memory, self._firsts_map, self._nexts_map, self._operator_precedence_manager)
            syntactic_analyzer.start()
            self._original_label_dictionary = syntactic_analyzer.get_label_dictionary()
            self._label_dictionary = syntactic_analyzer.get_label_dictionary()
            self.initialize_processor()
            self.notify_load_finished()
        except (LexicalException, LexicalExceptionInvalidSymbol, 
            LexicalExceptionInvalidOperator, SyntacticException, 
            SyntacticExceptionNoMatch, SimpleSyntacticException) as e:  # TODO ver estas excepciones catcheadas
            self._error = e
            self.notify_error()
        
    def reset(self, on_load = True):
        if self._code_memory is not None:
            self._deleted_label_name = None
            self._last_executed_instruction_address = None
            self._data_memory.reset()
            self._heap_memory.reset()
            self._cache.reset()
            self._last_execution_added_labels.clear()
            self._modified_cell_manager.reset()
            if not on_load:
                self._processor.reset()
                self._label_dictionary = self._original_label_dictionary.copy()
            else:
                self._breakpoint_list = None
            self.notify_reset_finished()
            
    def undo(self):
        try:
            cache_entry = self._cache.pop()
        except EmptyCacheException as e:
            self._error = e
            self.notify_error()
        self._deleted_label_name = None
        self._last_execution_added_labels.clear()
        self._modified_cell_manager.reset()
        self._last_executed_instruction_address = cache_entry.get_last_executed_instruction_address()
        self._processor.reinstate_pc(cache_entry.get_pc())
        self._undo_memory_modified_data_cells(cache_entry.get_memory_modified_data_cells())
        self._undo_register_modified_data_cells(cache_entry.get_register_modified_data_cells())
        self._undo_memory_modified_heap_cells(cache_entry.get_memory_modified_heap_cells())
        self._undo_register_modified_heap_cells(cache_entry.get_register_modified_heap_cells())
        self._undo_label_modification(cache_entry.get_label_added_entry())
        self._processor.enable()
        
        self.notify_undo_finished()
     
    def update_breakpoint_list(self, breakpoint_list):
        self._breakpoint_list = breakpoint_list
        
    def initialize_processor(self):
        if self._processor:
            self._processor.reset()
        else:
            self._processor = Processor(virtual_machine=self)
            
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
            
    # --------- notify listeners (END)
    
    def reset_all_time_modified_cells(self):
        self._all_time_modified_data_cells_addresses.clear()
        self._all_time_modified_heap_cells_addresses.clear()
    
    def access_data_memory(self, address):
        value = self._data_memory.get_cell(address).value
        return value
    
    def access_heap_memory(self, address):
        value = self._heap_memory.get_cell(address).value
        return value
    
    def set_data_memory(self, address, data = None, source_instruction_address = None):
        annotation = None
        if source_instruction_address is not None:
            annotation = self._code_memory.get_codecell(source_instruction_address).annotation
        cell = self._data_memory.get_cell(address)
        self._cache.set_last_entry_memory_modified_data_cell_list([cell])
        modified_cell = self._data_memory.set_cell(address, data, annotation)
        self._modified_cell_manager.add_to_memory_modified_data_cells(modified_cell)
        self._all_time_modified_data_cells_addresses.append(address)
        
    def set_heap_memory(self, address, data = None, source_instruction_address = None):
        annotation = None
        if source_instruction_address is not None:
            annotation = self._code_memory.get_codecell(source_instruction_address).annotation
        cell = self._heap_memory.get_cell(address)
        self._cache.set_last_entry_memory_modified_heap_cell_list([cell])
        modified_cell = self._heap_memory.set_cell(address, data, annotation)
        self._modified_cell_manager.add_to_memory_modified_heap_cells(modified_cell)
        self._all_time_modified_heap_cells_addresses.append(address)
        
    def set_libre(self, former_libre, libre):
        former = self._data_memory.get_cell(former_libre)
        new = self._data_memory.get_cell(libre)
        self._cache.peek().set_register_modified_data_cell_list([new, former])
        self._data_memory.place_libre(libre)
        self._modified_cell_manager.add_to_register_modified_data_cells(former)
        self._modified_cell_manager.add_to_register_modified_data_cells(new)
        self._all_time_modified_data_cells_addresses.append(new.address)
        self._all_time_modified_data_cells_addresses.append(former.address)
        
    def set_actual(self, former_actual, actual):
        former = self._data_memory.get_cell(former_actual)
        new = self._data_memory.get_cell(actual)
        self._cache.peek().set_register_modified_data_cell_list([new, former])
        self._data_memory.place_actual(actual)
        self._modified_cell_manager.add_to_register_modified_data_cells(former)
        self._modified_cell_manager.add_to_register_modified_data_cells(new)
        self._all_time_modified_data_cells_addresses.append(new.address)
        self._all_time_modified_data_cells_addresses.append(former.address) 
       
    def set_po(self, former_po, po):
        former = self._heap_memory.get_cell(former_po)
        new = self._heap_memory.get_cell(po)
        self._cache.peek().set_register_modified_heap_cell_list([new, former])
        self._heap_memory.place_po(po)
        self._modified_cell_manager.add_to_register_modified_heap_cells(former)
        self._modified_cell_manager.add_to_register_modified_heap_cells(new)
        self._all_time_modified_heap_cells_addresses.append(new.address)
        self._all_time_modified_heap_cells_addresses.append(former.address)
        
    def define_label(self, label_token, address):
        label_name = str.lower(label_token.lexeme)
        if self._original_label_dictionary.get(label_name) == None:  
            former_address = self._label_dictionary.get(label_name)
            self._cache.peek().set_label_added_entry({label_name : former_address}) # TODO reponer en logica y en vista
            self._label_dictionary[label_name] = address
            self._last_execution_added_labels[label_name] = address
            return Processor.SUCCESS
        else:
            self._error = f"Label with name {label_name} is already defined in the code memory."
            self.notify_error()
            return Processor.FAILURE
        
    def print_output(self, text):
        self._last_output_text = text
        self.notify_output()
            
    def deliver_user_input(self, input):
        self._last_user_input = input
        self._processor.deliver_user_input()
        
    def execute_program(self, mode, steps : int = None):
        self._modified_cell_manager.reset()
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
            
    def _undo_label_modification(self, label_entry):
        if label_entry is not None:
            label_name = label_entry.popitem()[0]
            former_address = label_entry.get(label_name)
            if former_address is None:
                if self._label_dictionary.get(label_name) is not None: 
                    self._label_dictionary.pop(label_name)
                    self._deleted_label_name = label_name
            else:
                self._label_dictionary[label_name] = former_address
                self._last_execution_added_labels[label_name] = former_address
        
    def _undo_memory_modified_data_cells(self, memory_modified_data_cells):
        original_data_cells = []
        if len(memory_modified_data_cells) > 0:
            undo_modified_cell = memory_modified_data_cells[0]
            address = undo_modified_cell.address
            original_data_cells.append(self._data_memory.set_cell(address, undo_modified_cell.value, undo_modified_cell.annotation))
            for i in range(1,len(memory_modified_data_cells)):
                original_data_cells.append(self._data_memory.get_cell(memory_modified_data_cells[i].address))
            self._modified_cell_manager.extend_memory_modified_data_cells(original_data_cells)
        
    def _undo_register_modified_data_cells(self, register_modified_data_cells):
        for undo_modified_cell in register_modified_data_cells:
            address = undo_modified_cell.address
            if undo_modified_cell.libre:
                self._processor.reinstate_libre(address)
                self._data_memory.place_libre(address)
            if undo_modified_cell.actual:
                self._processor.reinstate_actual(address)
                self._data_memory.place_actual(address)
        
        self._modified_cell_manager.extend_register_modified_data_cells(register_modified_data_cells)
        
    def _undo_memory_modified_heap_cells(self, memory_modified_heap_cells):
        original_heap_cells = []
        if len(memory_modified_heap_cells) > 0:
            undo_modified_cell = memory_modified_heap_cells[0]
            address = undo_modified_cell.address
            original_heap_cells.append(self._heap_memory.set_cell(address, undo_modified_cell.value, undo_modified_cell.annotation))
            for i in range(1,len(memory_modified_heap_cells)):
                original_heap_cells.append(self._data_memory.get_cell(memory_modified_heap_cells[i].address))
            self._modified_cell_manager.extend_memory_modified_data_cells(original_heap_cells)
        
    def _undo_register_modified_heap_cells(self, register_modified_heap_cells):
        for undo_modified_cell in register_modified_heap_cells:
            address = undo_modified_cell.address
 
            if undo_modified_cell.po:
                self._processor.reinstate_po(address)
                self._heap_memory.place_po(address)
        
        self._modified_cell_manager.extend_register_modified_data_cells(register_modified_heap_cells)
       
    # getters
         
    def _in_breakpoint_list(self, address : int):
        return self._breakpoint_list != None and address in self._breakpoint_list
    
    def get_instruction(self, address):
        return self._code_memory.get_instruction(address)
    
    def get_modified_data_cells(self):
        return self._modified_cell_manager.get_modified_data_cell_dictionary()
    
    def get_modified_heap_cells(self):
        return self._modified_cell_manager.get_modified_heap_cell_dictionary()
    
    def get_all_time_modified_data_cells_addresses(self):
        return self._all_time_modified_data_cells_addresses.copy() 
    
    def get_all_time_modified_heap_cells_addresses(self):
        return self._all_time_modified_heap_cells_addresses.copy() 
    
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
    
    def get_last_triggered_error(self):
        return self._error
    
    def get_last_executed_instruction_address(self):
        return self._last_executed_instruction_address
    
    def get_user_input(self):
        return self._last_user_input
    
    def get_label_dictionary(self):
        return self._label_dictionary
    
    def get_last_execution_added_labels(self):
        return self._last_execution_added_labels
    
    def get_last_output(self):
        return self._last_output_text
    
    def get_deleted_label_name(self):
        return self._deleted_label_name
    
    def get_cache_size(self):
        return self._cache.size()
    
    def get_code_memory(self):
        return self._code_memory
    
    def get_data_memory(self):
        return self._data_memory
    
    def get_heap_memory(self):
        return self._heap_memory