from model.presenter_vm_interface import PresenterVMInterface
from model.processor_vm_interface import ProcessorVMInterface
from logic.processor.processor import Processor
from model.cache.cache import Cache
from model.components.breakpoint_manager import BreakpointManager
from model.components.program_loader import ProgramLoader
from model.components.execution_engine import ExecutionEngine
from model.components.label_manager import LabelManager
from model.components.memory_manager import MemoryManager
from model.components.vm_error_handler import VMErrorHandler
from model.components.vm_io_handler import VMIOHandler
from model.exceptions.empty_cache_exception import EmptyCacheException

class VirtualMachine(PresenterVMInterface, ProcessorVMInterface):
    
    def __init__(self):
        self._vm_error_handler = VMErrorHandler(self)
        self._label_manager = LabelManager()
        self._memory_manager = MemoryManager()
        self._cache = Cache(10)
        self._processor = None
        self._listeners = []
        self._program_loader = ProgramLoader(self._memory_manager, self._label_manager, self._vm_error_handler)
        self._vm_io_handler = VMIOHandler()
        self._breakpoint_manager = BreakpointManager()
        self._execution_engine = ExecutionEngine(self._memory_manager, self._label_manager, self._breakpoint_manager, self._vm_error_handler)
        
    def addListener(self, listener): 
        self._listeners.append(listener)
        
    def load_program(self, file_path):        
        load_state = self._program_loader.load_program(file_path)
        if load_state == ProgramLoader.LOAD_SUCCESS:
            self._initialize_processor()
            self.notify_load_finished()
        elif load_state == ProgramLoader.LOAD_FAILURE:
            self.notify_error()
        
    def reset(self, on_load = True):
        if self._memory_manager.there_is_code_memory():
            self._label_manager.reset(on_load)
            self._execution_engine.reset()
            self._cache.reset()
            self._memory_manager.reset()
            self._vm_error_handler.reset()
            self._vm_io_handler.reset()
            if not on_load:
                self._initialize_processor()
            else:
                self._breakpoint_manager.reset()
            self.notify_reset_finished()
        
    def reset_all_time_modified_cells(self):
        self._memory_manager.reset_all_time_modified_cells()
            
    def undo(self):
        try:
            cache_entry = self._cache.pop()
        except EmptyCacheException as e:
            self._vm_error_handler.register_error(e)
            return
        self._label_manager.reset()
        self._memory_manager.reset(only_modified_cells= True)
        self._execution_engine.set_last_executed_instruction_address(cache_entry.get_last_executed_instruction_address())
        self._processor.reinstate_pc(cache_entry.get_pc())
        self._memory_manager.undo_memory_modified_data_cells(cache_entry.get_memory_modified_data_cells())
        self._memory_manager.undo_register_modified_data_cells(self._processor, cache_entry.get_register_modified_data_cells())
        self._memory_manager.undo_memory_modified_heap_cells(cache_entry.get_memory_modified_heap_cells())
        self._memory_manager.undo_register_modified_heap_cells(self._processor, cache_entry.get_register_modified_heap_cells())
        self._label_manager.undo_label_modification(cache_entry.get_label_added_entry())
        self._processor.enable()
        
        self.notify_undo_finished()
            
    def deliver_user_input(self, input):
        self._vm_io_handler.set_last_user_input(input)
        self._execution_engine.finish_input_execution()
        
    def execute_program(self, mode, steps : int = None):
        self._execution_engine.execute_program(self._cache, mode, steps)
        self.notify_execution_finished()
    
    def _initialize_processor(self):
        if self._processor:
            self._processor.reset()
        else:
            self._processor = Processor(virtual_machine=self)
            self._execution_engine.set_processor(self._processor)
    
    # --------- PROCESSOR use
    
    def access_data_memory(self, address):
        return self._memory_manager.access_data_memory(address)
    
    def access_heap_memory(self, address):
        return self._memory_manager.access_heap_memory(address)
    
    def set_data_memory(self, address, data = None, source_instruction_address = None):
        self._memory_manager.set_data_memory_cell(self._cache, address, data, source_instruction_address)
        
    def set_heap_memory(self, address, data = None, source_instruction_address = None):
        self._memory_manager.set_heap_memory_cell(self._cache, address, data, source_instruction_address)
        
    def set_libre(self, former_libre, libre):
        self._memory_manager.set_libre(self._cache.peek(), former_libre, libre)
        
    def set_actual(self, former_actual, actual):
        self._memory_manager.set_actual(self._cache.peek(), former_actual, actual)
       
    def set_po(self, former_po, po):
        self._memory_manager.set_po(self._cache.peek(), former_po, po)
        
    def define_label(self, label_token, address):
        if address >= 0:
            response = self._label_manager.define_label(label_token, address, cache=self._cache)
        else:
            response = "Label address value can only be a positive Integer."
        if response == Processor.SUCCESS:
            return response
        else:
            self._vm_error_handler.set_error(response)
            return Processor.FAILURE
        
    def print_output(self, text):
        self._vm_io_handler.set_last_output(text)
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
        return self._execution_engine.get_pc()
    
    def get_label_address(self, label_name):
        address = self._label_manager.get_label_address(label_name)
        if address == None:
            self._vm_error_handler.register_error(f"Label with name {label_name} does not exist")
            return
        return address
    
    def get_last_triggered_error(self):
        return self._vm_error_handler.get_last_registered_error()
    
    def get_last_executed_instruction_address(self):
        return self._execution_engine.get_last_executed_instruction_address()
    
    def get_user_input(self):
        return self._vm_io_handler.get_last_user_input()
    
    def get_label_dictionary(self):
        return self._label_manager.get_label_dictionary()
    
    def get_last_execution_added_labels(self):
        return self._label_manager.get_last_execution_added_labels()
    
    def get_last_output(self):
        return self._vm_io_handler.get_last_output()
    
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
    
    # dependency injection setters
    
    def set_vm_error_handler(self, error_handler):
        self._vm_error_handler = error_handler

    def set_label_manager(self, label_manager):
        self._label_manager = label_manager
        self._update_dependencies()

    def set_memory_manager(self, memory_manager):
        self._memory_manager = memory_manager
        self._update_dependencies()

    def set_cache(self, cache):
        self._cache = cache

    def set_processor(self, processor):
        self._processor = processor

    def set_listeners(self, listeners : list):
        self._listeners = listeners.copy()

    def set_program_loader(self, program_loader):
        self._program_loader = program_loader

    def set_vm_io_handler(self, io_handler):
        self._vm_io_handler = io_handler

    def set_breakpoint_manager(self, breakpoint_manager):
        self._breakpoint_manager = breakpoint_manager

    def set_execution_engine(self, execution_engine):
        self._execution_engine = execution_engine