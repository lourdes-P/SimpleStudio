from logic.processor.processor import Processor

class ExecutionEngine:
    COMPLETE_EXECUTION_MODE = 0
    SINGLE_STEP_EXECUTION_MODE = 1
    N_STEP_EXECUTION_MODE = 2
    
    def __init__(self, memory_manager, label_manager, breakpoint_manager, vm_error_handler):
        self._memory_manager = memory_manager
        self._label_manager = label_manager
        self._breakpoint_manager = breakpoint_manager
        self._vm_error_handler = vm_error_handler
        self._last_executed_instruction_address = None
        self._processor = None
    
    def reset(self):
        self._last_executed_instruction_address = None
    
    def execute_program(self, cache, mode, steps : int = None):
        self._memory_manager.reset(only_modified_cells=True)
        self._label_manager.clear_last_execution_added_labels()
        self._vm_error_handler.reset()
        state = Processor.SUCCESS
        
        if not self._memory_manager.there_is_code_memory():
            self._vm_error_handler.register_error('No source loaded')
            return
            
        match mode:
            case self.SINGLE_STEP_EXECUTION_MODE:
                state = self._single_step_execution(cache)
            case self.N_STEP_EXECUTION_MODE:
                state = self._n_step_execution(steps, cache)
            case self.COMPLETE_EXECUTION_MODE:
                state = self._complete_execution(cache)
                
        self._check_finished_execution_state(state)
      
    def finish_input_execution(self):
        state = self._processor.deliver_user_input()
        self._check_finished_execution_state(state)
    
    def set_processor(self, processor : Processor):
        self._processor = processor
    
    def get_pc(self):
        return self._processor.pc if self._processor != None else 0
    
    def get_last_executed_instruction_address(self):
        return self._last_executed_instruction_address
    
    def set_last_executed_instruction_address(self, last_executed_instruction_address):
        self._last_executed_instruction_address = last_executed_instruction_address
    
    def _single_step_execution(self, cache):
        pc = self.get_pc()
        cache.create_and_push_entry(self._last_executed_instruction_address, pc)
        state = self._processor.execute_next_instruction()
        self._last_executed_instruction_address = pc
            
        return state
        
    def _n_step_execution(self, steps : int, cache):
        state = self._single_step_execution(cache)
        steps-= 1
        while steps > 0 and state == Processor.SUCCESS and not (self._breakpoint_manager.address_in_breakpoint_list(self.get_pc())):
            state = self._single_step_execution(cache)   
            steps-= 1
        
        return state

    def _complete_execution(self, cache):
        state = self._single_step_execution(cache)
        while state == Processor.SUCCESS and not (self._breakpoint_manager.address_in_breakpoint_list(self.get_pc())):
            state = self._single_step_execution(cache)
        
        return state
            
    def _check_finished_execution_state(self, state):
        if state == Processor.COMPLETED or state == Processor.SUCCESS:
            pass
        elif state == Processor.FAILURE or state == Processor.DISABLED:
            error = self._vm_error_handler.get_last_registered_error()
            if error is None:
                error = self._processor.get_error()
                if error is None:
                    error = "Error while executing source code"
            self._vm_error_handler.register_error(error)