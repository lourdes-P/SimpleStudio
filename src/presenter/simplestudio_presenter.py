from logic.memories.codememory.codememory import CodeMemory
from model.virtual_machine import VirtualMachine
from view.components.codememory import CodeMemoryView
from view.main_view import SimpleStudioView
from listeners import VirtualMachineListener

class SimpleStudioPresenter(VirtualMachineListener):
    def __init__(self, code_memory: CodeMemory, virtual_machine : VirtualMachine, code_memory_view: CodeMemoryView = None, main_view: SimpleStudioView = None ):
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
                'line': code_cell.address + 1,  # address + 1 as line number
                'instruction': self._get_instruction_string(code_cell),
                'annotation': code_cell.annotation_string()
            }
            code_data.append(cell_data)

        
        self.code_memory_view.load_code(code_data)
        #self.code_memory_view.set_current_pc(self.code_memory_view.current_pc + 3)
    
    def _get_instruction_string(self, code_cell):
        """Extract the instruction string from a CodeCell"""
        if hasattr(code_cell.instruction, 'generate_string'):
            return code_cell.instruction.generate_string()
        else:
            return str(code_cell.instruction)
        
    def on_file_selected(self):
        try:
            file_path = self.main_view.get_selected_file_path()
            # TODO self.main_view.loading(True)          
            self.virtual_machine.load_program(file_path)       # crear hilo? puede ser util si ya hay algo mostrandose?
        except Exception as e:
            self.main_view.display_error(f"Error loading file: {str(e)}")
    
    def load_has_finished(self):
        # TODO self.main_view.loading(False)
        self.code_memory = self.virtual_machine.get_code_memory()
        self.update_code_memory_view()        
        
    def trigger_error(self):
        error = self.virtual_machine.get_last_triggered_error()
        self.main_view.display_error(error)
        
    def update_pc(self, pc: int):
        self.code_memory_view.set_current_pc(pc)
    