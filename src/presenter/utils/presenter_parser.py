from model.utils.modified_cell_manager import ModifiedCellManager

class PresenterParser:
    
    @staticmethod
    def parse_code_memory(codecell_list : list):
        """Returns a list of dictionaries with keys (label, address, instruction, annotation). Values are all strings"""
        code_data = []
        
        for code_cell in codecell_list:
            cell_data = {                
                'label': code_cell.label_string(),
                'address': code_cell.instruction.address,
                'instruction': PresenterParser.get_instruction_string(code_cell),
                'annotation': code_cell.annotation_string()
            }
            code_data.append(cell_data)
            
        return code_data
    
    @staticmethod
    def parse_modified_cells(cell_dictionary : dict):
        memory_modified = cell_dictionary[ModifiedCellManager.SET_MEMORY_MODIFIED]
        only_register_modified = cell_dictionary[ModifiedCellManager.ONLY_REGISTER_MODIFIED]
        modified_cells = PresenterParser.parse_data_heap_memory(memory_modified, True)
        modified_cells.extend(PresenterParser.parse_data_heap_memory(only_register_modified))
        return modified_cells
    
    @staticmethod
    def parse_data_heap_memory(cell_list : list, memory_modified = False):
        """Returns a list of dictionaries with keys (register, address, value, annotation, memory_modified)"""
        data = []
        for cell in cell_list:
            cell_data = {                
                'register': cell.generate_register_string(),
                'address': cell.address, 
                'value': cell.value if cell.value is not None else '###',
                'annotation': cell.annotation_string(),
                'memory_modified': memory_modified
            }
            data.append(cell_data)
        return data
    
    @staticmethod
    def parse_reset_data_heap_memory(cell_list : list, all_time_modified_cells_addresses):
        '''Returns a list of dictionaries with keys (register, address, value, annotation), with only the cells that have been modified as stated in all_time_modified_cells_addresses.
        For reset use'''
        data = []
        for cell in cell_list:
            address = cell.address
            if address in all_time_modified_cells_addresses:
                cell_data = {                
                    'register': cell.generate_register_string(),
                    'address': address, 
                    'value': cell.value if cell.value is not None else '###',
                    'annotation': cell.annotation_string(),
                }
                data.append(cell_data)
        return data
    
    @staticmethod
    def parse_label_dictionary(label_dictionary : dict):
        """
        Returns list with format
        [index] = {
                'name': 'label',
                'address': 'address' 
                }
        """
        label_list = []
        for key in label_dictionary.keys():
            label_data = {
                'name': key,
                'address': label_dictionary[key]
            }
            label_list.append(label_data)
        
        return label_list
    
    @staticmethod
    def get_instruction_string(code_cell):
        """Extract the instruction string from a codecell"""
        if hasattr(code_cell.instruction, 'generate_string'):
            return code_cell.instruction.generate_string()
        else:
            return str(code_cell.instruction)