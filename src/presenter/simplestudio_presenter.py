from model.virtual_machine import VirtualMachine
from view.main_view import SimpleStudioView
from listeners import VirtualMachineListener
from presenter.utils.presenter_parser import PresenterParser
import os
import time

class SimpleStudioPresenter(VirtualMachineListener):
    def __init__(self, virtual_machine : VirtualMachine):      
        self.virtual_machine = virtual_machine
        
    def start(self):
        self.main_view = SimpleStudioView(self)
        self.virtual_machine.addListener(self)
        self._initialize_data_memory_view(self.virtual_machine.get_data_memory())
        self._initialize_heap_memory_view(self.virtual_machine.get_heap_memory())
        self._last_file_path = None
        self._file_last_modification_time = None
        self._loading_file = False
        self.main_view.mainloop()
    
    def set_virtual_machine(self, virtual_machine : VirtualMachine):
        self.virtual_machine = virtual_machine
    
    def update_code_memory_view(self):       
        code_data = PresenterParser.parse_code_memory(self.virtual_machine.get_code_memory().codecell_list)
        
        self.main_view.load_code_onto_c_memory(code_data, self.main_view.get_selected_file_path())
       
    # --------- user view events    
     
    def on_file_selected(self):
        try:
            file_path = self.main_view.get_selected_file_path()         
            self._loading_file = True
            self.virtual_machine.load_program(file_path)
            if self._last_file_path is not None:
                self.virtual_machine.reset()
            self._last_file_path = file_path
            self._file_last_modification_time = os.path.getmtime(file_path)
        except Exception as e:
            self.main_view.display_error(f"Error loading file: {str(e)}")
            self._loading_file = False
            
    def on_user_input(self, input):
        self.virtual_machine.deliver_user_input(input)
        
    def on_breakpoint_change(self):
        breakpoint_list = self.main_view.get_breakpoints()
        self.virtual_machine.update_breakpoint_list(breakpoint_list)
        
    def on_complete_execution(self):
        self.virtual_machine.execute_program(VirtualMachine.COMPLETE_EXECUTION_MODE)
        
    def on_single_step_execution(self):
        self.virtual_machine.execute_program(VirtualMachine.SINGLE_STEP_EXECUTION_MODE)
    
    def on_n_step_execution(self, steps=None):
        self.virtual_machine.execute_program(VirtualMachine.N_STEP_EXECUTION_MODE, steps)
    
    def on_reset(self):
        try: 
            if self._last_file_path != None:
                file_modification_time = os.path.getmtime(self._last_file_path)
                if self._file_last_modification_time == file_modification_time:
                    self.virtual_machine.reset(on_load=False)
                else:
                    self._loading_file = True
                    self.virtual_machine.load_program(self._last_file_path)
                    self._file_last_modification_time = file_modification_time
                    self.virtual_machine.reset()
        except Exception as e:
            self.main_view.display_error(f"Error loading file: {str(e)}")
            
    def on_undo(self):
        self.virtual_machine.undo()
        
    def on_switch_code_editor(self):
        selected_line_number = self.main_view.get_selected_code_line()
        self.main_view.switch_code_editor(selected_line_number)
        
    # --------- end user view events      
    
    # --------- listener methods
    
    def load_has_finished(self):
        self.update_code_memory_view()
        label_list = PresenterParser.parse_label_dictionary(self.virtual_machine.get_label_dictionary())
        self.main_view.load_label_panel(label_list)  
        self._loading_file = False    
        
    def trigger_error(self):
        error = self.virtual_machine.get_last_triggered_error()
        self.disable_execution()
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
        reset_code_memory = True
        if not self._loading_file:
            self.update_code_memory_view()
        else:
            self._loading_file = False
            reset_code_memory = False
        all_time_modified_data_cells_addresses = self.virtual_machine.get_all_time_modified_data_cells_addresses()
        parsed_data_memory = PresenterParser.parse_reset_data_heap_memory(self.virtual_machine.get_data_memory().cell_list, all_time_modified_data_cells_addresses)
        all_time_modified_heap_cells_addresses = self.virtual_machine.get_all_time_modified_heap_cells_addresses()
        parsed_heap_memory = PresenterParser.parse_reset_data_heap_memory(self.virtual_machine.get_heap_memory().cell_list, all_time_modified_heap_cells_addresses)
        label_list = PresenterParser.parse_label_dictionary(self.virtual_machine.get_label_dictionary())
        self.virtual_machine.reset_all_time_modified_cells()
        self.main_view.reset(parsed_data_memory, parsed_heap_memory, label_list, reset_code_memory)
        self.main_view.set_cache_entry_disponibility(self.virtual_machine.get_cache_size())
       
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
    
    def _initialize_data_memory_view(self, data_memory):
        self.main_view.load_data_memory(PresenterParser.parse_data_heap_memory(data_memory.cell_list))
    
    def _initialize_heap_memory_view(self, heap_memory):
        self.main_view.load_heap_memory(PresenterParser.parse_data_heap_memory(heap_memory.cell_list))
        
    def _update_memories(self, modified_data_cells, modified_heap_cells):
        data_modified = PresenterParser.parse_modified_cells(modified_data_cells)
        heap_modified = PresenterParser.parse_modified_cells(modified_heap_cells)
        
        self.main_view.update_data_memory(data_modified)
        self.main_view.update_heap_memory(heap_modified)    