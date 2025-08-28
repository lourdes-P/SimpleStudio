import eel
from logic.interpreter.lexicalanalyzer.token_ import Token
from logic.memories.codememory.codememory import CodeMemory
from logic.memories.codememory.codecell import CodeCell

eel.init('./src/gui/static')

@eel.expose
def get_initial_code_memory():
    """Get the initial code memory to display"""
    # This would come from your actual implementation
    example_cells = [
        {
            'label': 'main',
            'address': 0,
            'instruction': 'LOAD R1, 10',
            'annotation': None
        },
        {
            'label': None,
            'address': 1,
            'instruction': 'ADD R1, R2',
            'annotation': '@ Add operation'
        }
    ]
    return example_cells

def start_gui():
    eel.start('index.html', size=(1000, 800), mode='chrome')

if __name__ == '__main__':
    start_gui()
