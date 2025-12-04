from logic.compiler.lexicalanalyzer.lexicalanalyzer import LexicalAnalyzer
from logic.compiler.syntacticanalyzer.syntacticanalyzer import SyntacticAnalyzer

class Compiler:
    
    @staticmethod
    def compile(code_memory, io_manager, reserved_word_map, firsts_map, nexts_map, operator_precedence_manager):
        """
        Compiles file opened in io_manager.
        Returns code label dictionary.
        Args:
            code_memory: logic code memory where cells will be inserted.
            io_manager: IOManager with file open.
            reserved_word_map: ReservedWordMap dictionary of reserved words.
            firsts_map: MapManager dictionary of firsts of the grammar.
            nexts_map: MapManager dictionary of nexts of the grammar.
            operator_precedence_manager: OperatorPrecedenceManager dictionary of operators' precedence.
        """
        lexical_analyzer = LexicalAnalyzer(io_manager, reserved_word_map)
        syntactic_analyzer = SyntacticAnalyzer(lexical_analyzer, code_memory, firsts_map, nexts_map, operator_precedence_manager)
        syntactic_analyzer.start()
        return syntactic_analyzer.get_label_dictionary()