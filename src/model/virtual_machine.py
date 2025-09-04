from logic.interpreter.lexicalanalyzer.lexicalanalyzer import LexicalAnalyzer
from logic.interpreter.iomanager.io_manager import IOManager
from logic.interpreter.lexicalanalyzer.reserved_word_manager.reserved_word_map import ReservedWordMap
from logic.interpreter.lexicalanalyzer.lexicalexceptions.lexicalexception import LexicalException
from logic.interpreter.lexicalanalyzer.lexicalexceptions.lexicalexception_invalidoperator import LexicalExceptionInvalidOperator
from logic.interpreter.lexicalanalyzer.lexicalexceptions.lexicalexception_invalidsymbol import LexicalExceptionInvalidSymbol
from logic.interpreter.syntacticanalyzer.syntacticanalyzer import SyntacticAnalyzer
from logic.interpreter.syntacticanalyzer.syntacticexceptions import *
from logic.memories.codememory.codememory import CodeMemory
from view.main_view import SimpleStudioView
from presenter.simplestudio_presenter import SimpleStudioPresenter

"""
Este es el main de mvp de diseño (está en la carpeta de presentador idk why)
package main.java.presenter;

import main.java.model.SearchModel;
import main.java.utils.WikiSearchSimlator;

public class Main {

  public static void main(String[] args) {

    SearchModel model = new SearchModel();
    //We will simulate the search for now, basically until we implement a concrete connection to the WikiAPI
    model.setWikiSearcher(new WikiSearchSimlator());

    SearchPresenter presenter = new SearchPresenter(model);

    presenter.start();
  }

}
"""

class VirtualMachine:
    def __init__(self):
        self.program = None
        self.C_memory = {}
        self.D_memory = {}
        self.H_memory = {}
        
    def load_program(self, file_path):
        try:
            with open(file_path, 'r') as file:
                self.program = self.parse_program(file.read())
            return True
        except Exception as e:
            print(f"Error loading program: {e}")
            return False
            
    def parse_program(self, program_text):
        # Implement your intermediate code parsing logic here
        # This is a simple example - you'll need to adapt it to your specific format
        instructions = []
        lines = program_text.strip().split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if line and not line.startswith('#'):  # Skip empty lines and comments
                parts = line.split()
                instructions.append({
                    'line': line_num,
                    'opcode': parts[0],
                    'operands': parts[1:] if len(parts) > 1 else []
                })
                
        return instructions
        
    def execute_program(self):
        # Implement your virtual machine execution logic here
        if not self.program:
            raise Exception("No program loaded")
            
        # Your execution logic would go here
        # This would process the instructions and update C, D, H memories
        