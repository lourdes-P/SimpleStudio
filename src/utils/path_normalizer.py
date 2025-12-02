
import os
import sys
import tempfile

class PathNormalizer:
    """
    Aims to bridge the gap between file path behavior on dev and on exe.
    """
    
    def resource_path(relative_path):
        """
        Parses a path to obtain an absolute path to resource.
        """
        """
        Works for either Nuitka 
        (tested, probably works for other programs that build executable with the interpreter located in 
        the root of the temp directory where the bundled files are extracted) 
        or PyInstaller"""
        if hasattr(sys, 'frozen') or '__compiled__' in globals():
            base_path = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
        else:
            base_path = os.path.abspath('.')
        
        return os.path.join(base_path, relative_path)
        
    
    
    