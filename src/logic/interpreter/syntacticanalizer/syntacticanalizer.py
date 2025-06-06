from logic.interpreter.utils.mapmanager import MapManager
from logic.interpreter.syntacticanalizer.syntacticexceptions.syntacticexception import SyntacticException
from logic.interpreter.syntacticanalizer.syntacticexceptions.syntacticexception_nomatch import SyntacticExceptionNoMatch

class SyntanticAnalizer:

    def __init__(self,lexical_analizer):
        self.lexical_analizer = lexical_analizer
        self._firsts_map = MapManager("resources/firsts.csv")
        self._nexts_map = MapManager("resources/nexts.csv")
        self._no_errors = True
        # sólo se notifica un error


    def match(self, expected_token_name):
        if (expected_token_name == self.current_token.token_name):
            self.current_token = self.lexical_analizer.next_token()
        else:
            raise SyntacticExceptionNoMatch(self.current_token, expected_token_name)
        
    def start(self):
        self.current_token = self.lexical_analizer.next_token()
        if self._firsts_map.contains_entry("Start", self.current_token.token_name):
            self.instruction_list()
        elif self.current_token.token_name == "EOF":
            pass # termination
        else:
            raise SyntacticException(self.current_token, self._firsts_map.get_value("Start"))
        
    def instruction_list(self):
        if self._firsts_map.contains_entry("InstructionList", self.current_token.token_name):
            self.instruction()
            self.instruction_list()            
        elif (self._nexts_map.contains_entry("InstructionList", self.current_token.token_name)):
            pass
        else:
            raise SyntacticException(self.current_token, self.concatenated_first_and_next_lists("InstructionList"))
        
    def instruction(self):
        if self.current_token.token_name == "identifier":
            self.match("identifier")
            self.signature()
        elif self._firsts_map.contains_entry("Signature", self.current_token.token_name):
            self.signature()
        elif (self._nexts_map.contains_entry("Instruction", self.current_token.token_name)):
            pass
        else:
            raise SyntacticException(self.current_token, self.concatenated_first_and_next_lists("Instruction"))

    def signature(self):
        match self.current_token.token_name:
            case "pr_setd":
                self.match("pr_setd")
                self.expression()
                self.match("comma")
                self.expression()
            case "pr_seth":
                self.match("pr_seth")
                self.expression()
                self.match("comma")
                self.expression()
            case "pr_setactual":
                self.match("pr_setactual")
                self.expression()
            case "pr_setlibre":
                self.match("pr_setlibre")
                self.expression()
            case "pr_setin":
                self.match("pr_setin")
                self.expression()
            case "pr_setout":
                self.match("pr_setout")
                self.expression()
            case "pr_setpo":
                self.match("pr_setpo")
                self.expression()
            case "pr_setlabel":
                self.match("pr_setlabel")
                self.match("identifier")
                self.match("comma")
                self.expression()
            case "pr_jumpt":
                self.match("pr_jumpt")
                self.expression()
                self.match("comma")
                self.expression()
            case "pr_jump":
                self.match("pr_jump")
                self.expression()
            case "pr_halt":
                self.match("pr_halt")

    def expression(self):
        if self._firsts_map.contains_entry("UnaryOp", self.current_token.token_name):
            self.unary_op()
            self.expression()
            self.expression_remainder()
        elif self._firsts_map.contains_entry("Operand", self.current_token.token_name):
            self.operand()
            self.expression_remainder()
        elif (self._nexts_map.contains_entry("Expression", self.current_token.token_name)):
            pass
        else:
            raise SyntacticException(self.current_token, self.concatenated_first_and_next_lists("Expression"))

    def unary_op(self):
        match self.current_token.token_name:
            case "plus":
                self.match("plus")
            case "minus":
                self.match("minus")
            case "not":
                self.match("not")

    def expression_remainder(self):
        if self._firsts_map.contains_entry("ExpressionRemainder", self.current_token.token_name):
            self.binary_op()
            self.expression()
        elif (self._nexts_map.contains_entry("ExpressionRemainder", self.current_token.token_name)):
            pass
        else:
            raise SyntacticException(self.current_token, self.concatenated_first_and_next_lists("ExpressionRemainder"))

    def operand(self):
        match self.current_token.token_name:
            case "pr_d":
                self.match("pr_d")
                self.match("open_square_bracket")
                self.expression()
                self.match("close_square_bracket")
            case "pr_h":
                self.match("pr_h")
                self.match("open_square_bracket")
                self.expression()
                self.match("close_square_bracket")
            case "pr_actual":
                self.match("pr_actual")
            case "pr_libre":
                self.match("pr_libre")
            case "int":
                self.match("int")
            case "identifier":
                self.match("identifier")
            case "pr_pc":
                self.match("pr_pc")
            case "pr_po":
                self.match("pr_po")
            case "open_parenthesis":
                self.match("open_parenthesis")
                self.expression()
                self.match("close_parenthesis")
            
    def binary_op(self):
        if self._firsts_map.contains_entry("BinaryOp", self.current_token.token_name):
            match self.current_token.token_name:
                case "plus":
                    self.match("plus")
                case "minus":
                    self.match("minus")
                case "multiplication":
                    self.match("multiplication")
                case "division":
                    self.match("division")
                case "equals":
                    self.match("equals")
                case "different":
                    self.match("different")
                case "lesser":
                    self.match("lesser")
                case "lesser_or_equal":
                    self.match("lesser_or_equal")
                case "greater":
                    self.match("greater")
                case "greater_or_equal":
                    self.match("greater_or_equal")
                case "and":
                    self.match("and")
                case "or":
                    self.match("or")
        elif (self._nexts_map.contains_entry("BinaryOp", self.current_token.token_name)):
            pass # TODO ver si esto va aca... (no creo)
        else:
            raise SyntacticException(self.current_token, self.concatenated_first_and_next_lists("BinaryOp"))
        


    def concatenated_first_and_next_lists(self, production_name):
        copy_firsts_nexts_list = self._firsts_map.get_value(production_name).copy()
        copy_firsts_nexts_list.extend(self._nexts_map.get_value(production_name))
        return set(copy_firsts_nexts_list)
    
    def register_syntactic_error(self):
        self._no_errors = False

    @property
    def no_errors(self):
        return self._no_errors