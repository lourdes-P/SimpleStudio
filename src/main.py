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

def main():
    reserved_word_map = ReservedWordMap()
    io_manager = IOManager("./test1.txt")
    code_memory = CodeMemory()
    lexical_analyzer = LexicalAnalyzer(io_manager, reserved_word_map)    
    simplestudio_presenter = SimpleStudioPresenter(code_memory) 
    syntactic_analyzer = SyntacticAnalyzer(lexical_analyzer, code_memory)
    app = SimpleStudioView(simplestudio_presenter)
    
    simplestudio_presenter.set_code_memory_view(app.get_code_memory_view())
    # processor will be model in this MVP 
    
    try:
        syntactic_analyzer.start()
        
        if lexical_analyzer.no_errors and syntactic_analyzer.no_errors:
            print("Execution successful")
            code_memory.print_memory()
            
            app.load_parsed_code()
            
    except (LexicalException, LexicalExceptionInvalidSymbol, 
            LexicalExceptionInvalidOperator, SyntacticException, 
            SyntacticExceptionNoMatch) as e:
        print(f"Error: {e}")
        app.output_text.configure(state="normal")
        app.output_text.delete("1.0", "end")
        app.output_text.insert("end", f"Error: {e}\n")
        app.output_text.configure(state="disabled")
    
    app.mainloop()

if __name__ == "__main__":
    main()
