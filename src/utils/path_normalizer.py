
import os
import sys

class PathNormalizer:
    """
    Aims to bridge the gap between file path behavior on dev and on exe.
    """
    
    def resource_path(relative_path):
        """
        Parses a path to obtain an absolute path to resource.
        """
        base_path = getattr(sys, '_MEIPASS', os.path.abspath('.'))
        
        return os.path.join(base_path, relative_path)
        
    
    
    