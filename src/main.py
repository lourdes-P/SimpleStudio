from logic.interpreter.lexicalanalyzer.lexicalanalyzer import LexicalAnalyzer
from logic.interpreter.iomanager.io_manager import IOManager
from logic.interpreter.lexicalanalyzer.reserved_word_manager.reserved_word_map import ReservedWordMap
from logic.interpreter.lexicalanalyzer.lexicalexceptions.lexicalexception import LexicalException
from logic.interpreter.lexicalanalyzer.lexicalexceptions.lexicalexception_invalidoperator import LexicalExceptionInvalidOperator
from logic.interpreter.lexicalanalyzer.lexicalexceptions.lexicalexception_invalidsymbol import LexicalExceptionInvalidSymbol
from logic.interpreter.syntacticanalyzer.syntacticanalyzer import SyntacticAnalyzer
from logic.interpreter.syntacticanalyzer.syntacticexceptions import *
from logic.memories.codememory.codememory import CodeMemory
from model.virtual_machine import VirtualMachine
from presenter.simplestudio_presenter import SimpleStudioPresenter

def main():
    virtual_machine = VirtualMachine()    
    simplestudio_presenter = SimpleStudioPresenter(virtual_machine) 
    simplestudio_presenter.start()

if __name__ == "__main__":
    main()
