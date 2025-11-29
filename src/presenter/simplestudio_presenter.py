from model.components.execution_engine import ExecutionEngine
from model.virtual_machine import VirtualMachine
from presenter.view_presenter_interface import ViewPresenterInterface
from presenter.utils.presenter_file_manager import PresenterFileManager
from view.main_view import SimpleStudioViewInterface
from listeners import VirtualMachineListener
from presenter.utils.presenter_parser import PresenterParser

class SimpleStudioPresenter(VirtualMachineListener, ViewPresenterInterface):
    def __init__(self, virtual_machine : VirtualMachine):      
        self.virtual_machine = virtual_machine
        
    def start(self):
        self._resetting = False
        self.virtual_machine.addListener(self)
        self._initialize_data_memory_view(self.virtual_machine.get_data_memory())
        self._initialize_heap_memory_view(self.virtual_machine.get_heap_memory())
        self._file_manager = PresenterFileManager()
        self.main_view.start()
    
    def set_virtual_machine(self, virtual_machine : VirtualMachine):
        self.virtual_machine = virtual_machine
        
    def set_view(self, main_view : SimpleStudioViewInterface):
        self.main_view = main_view
        
    # --------- user view events    
     
    def on_file_selected(self):
        try:
            file_path = self.main_view.get_selected_file_path()         
            reset = self._file_manager.load_file(file_path)
            self.virtual_machine.load_program(file_path)
            if reset:
                self.virtual_machine.reset()
        except Exception as e:
            self._file_manager.set_loading_file(False)
            self.main_view.display_error(f"Error loading file: {str(e)}")
            
    def on_user_input(self, input):
        self.virtual_machine.deliver_user_input(input)
        
    def on_breakpoint_change(self):
        breakpoint_list = self.main_view.get_breakpoints()
        self.virtual_machine.update_breakpoint_list(breakpoint_list)
        
    def on_complete_execution(self):
        self.virtual_machine.execute_program(ExecutionEngine.COMPLETE_EXECUTION_MODE)
        
    def on_single_step_execution(self):
        self.virtual_machine.execute_program(ExecutionEngine.SINGLE_STEP_EXECUTION_MODE)
    
    def on_n_step_execution(self, steps=None):
        self.virtual_machine.execute_program(ExecutionEngine.N_STEP_EXECUTION_MODE, steps)
    
    def on_reset(self):
        try: 
            on_load = self._file_manager.reload_file()
            self._resetting = True
            if on_load:
                self.virtual_machine.load_program(self._file_manager.last_file_path)
                self.virtual_machine.reset()
            elif on_load is False:
                self.virtual_machine.reset(on_load=False)
        except Exception as e:
            self._resetting = False
            self.main_view.display_error(f"Error loading file: {str(e)}") 
            
    def on_undo(self):
        self.virtual_machine.undo()
        
    def on_switch_code_editor(self):
        selected_address = self.main_view.get_selected_code_address()
        self.main_view.switch_code_editor(self._get_code_line_number_from_address(selected_address))
        
    def on_save_file(self, content, file_path = None):
        try:
            if file_path is None:
                self._file_manager.save(content)
            else:
                self._file_manager.save_as(content, file_path)
                self.main_view.set_selected_file_path(file_path)
            self.main_view.on_save_code_editor()
        except Exception as e:
            self.main_view.display_error(f"Error saving file: {str(e)}")

    # --------- end user view events      
    
    # --------- listener methods
    
    def load_has_finished(self):
        if not self._resetting:
            self._file_manager.set_loading_file(False)
            self._update_code_memory_view()
        label_list = PresenterParser.parse_label_dictionary(self.virtual_machine.get_label_dictionary())
        self.main_view.load_label_panel(label_list)    
        
    def trigger_error(self):
        error = self.virtual_machine.get_last_triggered_error()
        self.disable_execution()
        self._update_code_memory_view(code_editor_only=True, load_new_file=False)
        self.main_view.display_error(error)
        
    def trigger_user_input(self):
        self.main_view.display_user_input(self.on_user_input)
        
    def execution_finished(self):
        pc = self.virtual_machine.get_pc()
        last_executed_instruction_address = self.virtual_machine.get_last_executed_instruction_address()
        modified_data_cells = self.virtual_machine.get_modified_data_cells()
        modified_heap_cells = self.virtual_machine.get_modified_heap_cells()
        added_labels = self.virtual_machine.get_last_execution_added_labels()
        
        self.main_view.set_pc(pc, last_executed_instruction_address)
        if added_labels is not None and len(added_labels) > 0:
            self.main_view.add_labels(PresenterParser.parse_label_dictionary(added_labels))
        self._update_memories(modified_data_cells, modified_heap_cells)
        self.main_view.set_cache_entry_disponibility(self.virtual_machine.get_cache_size())
        
    def reset_has_finished(self):
        if not self._file_manager.loading_file and self._resetting:
            self._update_code_memory_view(clear_breakpoints=False, load_new_file=False)
        else:
            self._file_manager.set_loading_file(False)
            if self._resetting:
                self._update_code_memory_view(load_new_file=False)
        all_time_modified_data_cells_addresses = self.virtual_machine.get_all_time_modified_data_cells_addresses()
        parsed_data_memory = PresenterParser.parse_reset_data_heap_memory(self.virtual_machine.get_data_memory().cell_list, all_time_modified_data_cells_addresses)
        all_time_modified_heap_cells_addresses = self.virtual_machine.get_all_time_modified_heap_cells_addresses()
        parsed_heap_memory = PresenterParser.parse_reset_data_heap_memory(self.virtual_machine.get_heap_memory().cell_list, all_time_modified_heap_cells_addresses)
        label_list = PresenterParser.parse_label_dictionary(self.virtual_machine.get_label_dictionary())
        self.virtual_machine.reset_all_time_modified_cells()
        self.main_view.reset(parsed_data_memory, parsed_heap_memory, label_list)
        self.main_view.set_cache_entry_disponibility(self.virtual_machine.get_cache_size())
        self._resetting = False
       
    def undo_has_finished(self):
        pc = self.virtual_machine.get_pc()
        last_executed_instruction_address = self.virtual_machine.get_last_executed_instruction_address()
        modified_data_cells = self.virtual_machine.get_modified_data_cells()
        modified_heap_cells = self.virtual_machine.get_modified_heap_cells()
        added_labels = self.virtual_machine.get_last_execution_added_labels()
        deleted_label_name = self.virtual_machine.get_deleted_label_name()
        self.main_view.set_pc(pc, last_executed_instruction_address)
        if added_labels is not None and len(added_labels) > 0:
            self.main_view.add_labels(PresenterParser.parse_label_dictionary(added_labels))
        elif deleted_label_name is not None:
            self.main_view.delete_label(deleted_label_name)
        self._update_memories(modified_data_cells, modified_heap_cells)
        self.main_view.set_cache_entry_disponibility(self.virtual_machine.get_cache_size())
        
    def print_output(self):
        output_text = self.virtual_machine.get_last_output()
        self.main_view.print_output(output_text)
        
    def disable_execution(self):
        self.main_view.disable_execution()
        
    def enable_execution(self):
        self.main_view.enable_execution()
        
    # --------- end listener methods
    
    def _update_code_memory_view(self, clear_breakpoints = True, code_editor_only = False, load_new_file = True):       
        if code_editor_only:
            self.main_view.load_code_editor(load_new_file)
        else:
            code_data = PresenterParser.parse_code_memory(self.virtual_machine.get_code_memory().codecell_list)
            self.main_view.load_code_onto_c_memory(code_data, self.main_view.get_selected_file_path(), load_new_file, clear_breakpoints)
    
    def _initialize_data_memory_view(self, data_memory):
        self.main_view.load_data_memory(PresenterParser.parse_data_heap_memory(data_memory.cell_list))
    
    def _initialize_heap_memory_view(self, heap_memory):
        self.main_view.load_heap_memory(PresenterParser.parse_data_heap_memory(heap_memory.cell_list))
        
    def _update_memories(self, modified_data_cells, modified_heap_cells):
        data_modified = PresenterParser.parse_modified_cells(modified_data_cells)
        heap_modified = PresenterParser.parse_modified_cells(modified_heap_cells)
        
        self.main_view.update_data_memory(data_modified)
        self.main_view.update_heap_memory(heap_modified)    
        
    def _get_code_line_number_from_address(self, address):
        if address is not None:
            instruction = self.virtual_machine.get_instruction(address)
            return instruction.line
        else:
            return None