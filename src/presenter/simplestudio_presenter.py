from logic.memories.codememory.codememory import CodeMemory
from model.virtual_machine import VirtualMachine
from view.components.codememory import CodeMemoryView
from view.main_view import SimpleStudioView
from listeners import VirtualMachineListener

class SimpleStudioPresenter(VirtualMachineListener):
    def __init__(self, code_memory: CodeMemory, virtual_machine : VirtualMachine):
        self.code_memory = code_memory        
        self.virtual_machine = virtual_machine
        self.start()
        
        
    def start(self):
        self.main_view = SimpleStudioView(self)
        self.code_memory_view = self.main_view.get_code_memory_view()
        self.virtual_machine.addListener(self)
        self.main_view.mainloop()
    
    def set_virtual_machine(self, virtual_machine : VirtualMachine):
        self.virtual_machine = virtual_machine
    
    def set_code_memory_view(self, code_memory_view):
        self.code_memory_view = code_memory_view
    
    def update_code_memory_view(self):        
        code_data = []
        
        for code_cell in self.code_memory.codecell_list:
            # Convert each CodeCell to the dictionary format
            cell_data = {                
                'label': code_cell.label_string(),
                'address': code_cell.instruction.address,  # TODO address o linea?
                'instruction': self._get_instruction_string(code_cell),
                'annotation': code_cell.annotation_string()
            }
            code_data.append(cell_data)

        
        self.main_view.load_code_onto_c_memory(code_data)
        #self.code_memory_view.set_current_pc(self.code_memory_view.current_pc + 3)
    
    def _get_instruction_string(self, code_cell):
        """Extract the instruction string from a CodeCell"""
        if hasattr(code_cell.instruction, 'generate_string'):
            return code_cell.instruction.generate_string()
        else:
            return str(code_cell.instruction)
       
    # --------- user view events    
     
    def on_file_selected(self):
        try:
            file_path = self.main_view.get_selected_file_path()
            # TODO self.main_view.loading(True)          
            self.virtual_machine.load_program(file_path)       # crear hilo? puede ser util si ya hay algo mostrandose?
        except Exception as e:
            self.main_view.display_error(f"Error loading file: {str(e)}")
            
    def on_user_input(self):
        input = self.get_user_input()
        self.virtual_machine.deliver_user_input(input)
        
    def on_breakpoint_change(self):
        breakpoint_list = self.main_view.get_breakpoints()
        self.virtual_machine.update_breakpoint_list(breakpoint_list)
        
    # --------- end user view events      
    
    # --------- listener methods
    
    def load_has_finished(self):
        # TODO self.main_view.loading(False)
        self.code_memory = self.virtual_machine.get_code_memory()
        self.update_code_memory_view()        
        
    def trigger_error(self):
        error = self.virtual_machine.get_last_triggered_error()
        self.main_view.display_error(error)
        
    def trigger_user_input(self):
        self.main_view.display_user_input() # TODO main_view.display_user_input
        
    def disable_execution(self):
        self.main_view.disable_execution()  # TODO main_view.disable_execution
        
    # --------- end listener methods
    
        
    def update_pc(self, pc: int):
        self.code_memory_view.set_current_pc(pc)
    