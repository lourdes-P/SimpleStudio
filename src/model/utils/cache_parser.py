
class CacheParser:
    
    @staticmethod
    def clone_cell_list(cell_list):
        if cell_list is not None:
            cloned_list = []
            for cell in reversed(cell_list):
                cloned_list.append(cell.clone())
                
            return cloned_list
        else:
            return None