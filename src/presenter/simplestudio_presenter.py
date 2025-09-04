from logic.memories.codememory.codememory import CodeMemory
from view.components.codememory import CodeMemoryView
from view.main_view import SimpleStudioView

class SimpleStudioPresenter:
    def __init__(self, code_memory: CodeMemory, code_memory_view: CodeMemoryView = None, main_view: SimpleStudioView = None ):
        self.code_memory = code_memory
        self.code_memory_view = code_memory_view        # TODO hacer que se obtenga a partir de main_view
        self.main_view = main_view
    
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
        self.code_memory_view.set_current_pc(self.code_memory_view.current_pc + 3)
    
    def _get_instruction_string(self, code_cell):
        """Extract the instruction string from a CodeCell"""
        if hasattr(code_cell.instruction, 'generate_string'):
            return code_cell.instruction.generate_string()
        else:
            return str(code_cell.instruction)
        
    def on_file_selected(self, file_path):
        try:          
            success = self.model.load_program(file_path)
            if success:
                print(f"Successfully loaded program from {file_path}")
            else:
                self.main_view.display_error("Failed to load the program file")
        except Exception as e:
            self.main_view.display_error(f"Error loading file: {str(e)}")
        
    def update_pc(self, pc: int):
        self.code_memory_view.set_current_pc(pc)
    