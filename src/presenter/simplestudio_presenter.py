from logic.memories.codememory.codememory import CodeMemory
from model.virtual_machine import VirtualMachine
from view.main_view import SimpleStudioView
from listeners import VirtualMachineListener

class SimpleStudioPresenter(VirtualMachineListener):
    def __init__(self, code_memory: CodeMemory, virtual_machine : VirtualMachine):
        self.code_memory = code_memory        
        self.virtual_machine = virtual_machine
        self.start()   
        
    def start(self):
        self.main_view = SimpleStudioView(self)
        self.virtual_machine.addListener(self)
        self.initialize_data_memory_view(self.virtual_machine.get_data_memory())
        self.initialize_heap_memory_view(self.virtual_machine.get_heap_memory())
        self.main_view.mainloop()
    
    def set_virtual_machine(self, virtual_machine : VirtualMachine):
        self.virtual_machine = virtual_machine
    
    def set_code_memory_view(self, code_memory_view):
        self.code_memory_view = code_memory_view
    
    def update_code_memory_view(self):        
        code_data = []
        
        for code_cell in self.code_memory.codecell_list:
            cell_data = {                
                'label': code_cell.label_string(),
                'address': code_cell.instruction.address,
                'instruction': self._get_instruction_string(code_cell),
                'annotation': code_cell.annotation_string()
            }
            code_data.append(cell_data)

        
        self.main_view.load_code_onto_c_memory(code_data)
        #self.code_memory_view.set_current_pc(self.code_memory_view.current_pc + 3)
        
    def update_data_memory_view(self, data_memory):
        pass    # TODO update_data_memory_view
    """dos opciones:
        - despues de cada instruccion, si fue modificada la data memory (tener un boolean en la clase).
        - si fue mas de un step, y si fue modificada la data memory, guardo las addresses que fueron modificadas
        en un arreglo o algo, y cambio todas las lineas de una en la vista
    """
    
    def update_heap_memory_view(self, heap_memory):
        pass    # TODO update_heap_memory_view
    
    def _get_instruction_string(self, code_cell):
        """Extract the instruction string from a CodeCell"""
        if hasattr(code_cell.instruction, 'generate_string'):
            return code_cell.instruction.generate_string()
        else:
            return str(code_cell.instruction)
       
    # --------- user view events    
     
    def on_file_selected(self):
        #try:
        file_path = self.main_view.get_selected_file_path()
        # TODO self.main_view.loading(True)          
        self.virtual_machine.load_program(file_path)       # crear hilo? puede ser util si ya hay algo mostrandose?
        """except Exception as e:
            self.main_view.display_error(f"Error loading file: {str(e)}")"""
            
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
        self.virtual_machine.execute_program(steps, VirtualMachine.N_STEP_EXECUTION_MODE)
    
    def on_reset(self):
        pass # TODO on_reset (presenter)
        
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
        self.main_view.display_user_input(self.on_user_input)
        
    def execution_finished(self):
        pc = self.virtual_machine.get_pc()
        modified_data_cells = self.virtual_machine.get_modified_data_cells()
        modified_heap_cells = self.virtual_machine.get_modified_heap_cells()
        
        self.main_view.set_pc(pc)
        self.main_view.update_data_memory(self._parse_data_heap_memory(modified_data_cells))
        self.main_view.update_heap_memory(self._parse_data_heap_memory(modified_heap_cells))
        
    def disable_execution(self):
        self.main_view.disable_execution()
        
    def enable_execution(self):
        self.main_view.enable_execution()
        
    # --------- end listener methods
    
    def initialize_data_memory_view(self, data_memory):
        self.main_view.load_data_memory(self._parse_data_heap_memory(data_memory.cell_list))
    
    def initialize_heap_memory_view(self, heap_memory):
        self.main_view.load_heap_memory(self._parse_data_heap_memory(heap_memory.cell_list))
        
    def _parse_data_heap_memory(self, cell_list):
        data = []
        for cell in cell_list:
            cell_data = {                
                'register': cell.generate_register_string(),
                'address': cell.address, 
                'value': cell.value,
                'annotation': cell.annotation_string()
            }
            data.append(cell_data)
            
        return data
        
    def update_pc(self, pc: int):
        self.code_memory_view.set_current_pc(pc)
    