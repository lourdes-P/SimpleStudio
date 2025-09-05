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

def main():
    reserved_word_map = ReservedWordMap()
    io_manager = IOManager("./test1.txt")
    # crear model (virtual machine)
    # setear la memoria de código (hacer que al setearlo, se seteen los listeners)
    virtual_machine = VirtualMachine()
    code_memory = CodeMemory()
    lexical_analyzer = LexicalAnalyzer(io_manager, reserved_word_map)    
    simplestudio_presenter = SimpleStudioPresenter(code_memory, virtual_machine) 
    
    # pasarle el modelo al presentador
    # en el presentador, crear la view
    """
    public void start() {
        searchView = new SearchView(this, searchModel);
        searchView.showView();
        initModelListeners();
    }
    private void initModelListeners() {
        searchModel.addListener(() -> searchView.showSearchResult(formatSearchResult()));
    }
    """
    # esto es cuando ya esté la virtual machine con la memoria C al menos
    # TODO refactor de ubicacion de la memoria C
    syntactic_analyzer = SyntacticAnalyzer(lexical_analyzer, code_memory)
    '''app = SimpleStudioView(simplestudio_presenter)
    
    simplestudio_presenter.set_code_memory_view(app.get_code_memory_view())'''
    # virtual machine will be model in this MVP 
    
    '''try:
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
    
    app.mainloop()'''

if __name__ == "__main__":
    main()
