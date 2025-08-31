from logic.expression_ast.expression_node import ExpressionNode
from logic.interpreter.utils.mapmanager import MapManager
from logic.interpreter.syntacticanalyzer.syntacticexceptions.syntacticexception import SyntacticException
from logic.interpreter.syntacticanalyzer.syntacticexceptions.syntacticexception_nomatch import SyntacticExceptionNoMatch
from logic.interpreter.syntacticanalyzer.syntacticexceptions.syntacticexception_missingenter import SyntacticExceptionMissingEnter
from logic.interpreter.iomanager.io_manager import IOManager
from logic.memories.codememory.codecell import CodeCell
from logic.memories.codememory.codememory import CodeMemory
from logic.processor.instructions import *
from logic.expression_ast.binaryop_nodes import *
from logic.expression_ast.unaryop_nodes import *
from logic.expression_ast.operand_nodes import *


class SyntacticAnalyzer:

    def __init__(self, lexical_analyzer, code_memory):
        self.current_token = None
        self.lexical_analyzer = lexical_analyzer
        self._code_memory = code_memory
        self._firsts_map = MapManager("resources/firsts.csv")
        self._nexts_map = MapManager("resources/nexts.csv")
        self._no_errors = True
        self._address = 0       # suma por cada instrucción que se guarda en la memoria C, incremento en 1
        # sólo se notifica un error


    def match(self, expected_token_name):
        if expected_token_name == self.current_token.token_name:
            self.current_token = self.lexical_analyzer.next_token()
        else:
            raise SyntacticExceptionNoMatch(self.current_token, expected_token_name)
        
    def start(self):
        self.current_token = self.lexical_analyzer.next_token()
        if self._firsts_map.contains_entry("Start", self.current_token.token_name):
            self.instruction_list()
        elif self.current_token.token_name == "EOF":
            pass # termination
        else:
            raise SyntacticException(self.current_token, self._firsts_map.get_value("Start"))
        
    def instruction_list(self):
        if self._firsts_map.contains_entry("InstructionList", self.current_token.token_name):
            self.instruction()
            self.enter()
            self.instruction_list()            
        elif self._nexts_map.contains_entry("InstructionList", self.current_token.token_name):
            pass
        else:
            raise SyntacticException(self.current_token, self.concatenated_first_and_next_lists("InstructionList"))
        
    def enter(self):
        if self._firsts_map.contains_entry("Enter", self.current_token.token_name):
            self.match("enter")
        elif self._nexts_map.contains_entry("Enter", self.current_token.token_name):
            pass
        else:
            raise SyntacticExceptionMissingEnter(self.current_token)

    def instruction(self):
        if self.current_token.token_name == "identifier":
            codecell = CodeCell(address= self._address)
            # address is increased after         
            label = self.current_token
            codecell.set_label_token(label)
            self.match("identifier")
            instruction = self.signature()
            codecell.set_instruction(instruction)
            annotation = self.annotation()
            codecell.set_annotation(annotation)
            self._code_memory.add_codecell(codecell)
        elif self._firsts_map.contains_entry("Signature", self.current_token.token_name):
            codecell = CodeCell(address= self._address)   
            # address is increased after         
            instruction = self.signature()
            codecell.set_instruction(instruction)
            annotation = self.annotation()
            codecell.set_annotation(annotation)
            self._code_memory.add_codecell(codecell)
        elif self._nexts_map.contains_entry("Instruction", self.current_token.token_name):
            pass
        else:
            raise SyntacticException(self.current_token, self.concatenated_first_and_next_lists("Instruction"))

    def annotation(self):
        if self._firsts_map.contains_entry("Annotation", self.current_token.token_name):
            annotation = self.current_token
            self.match("annotation")
            return annotation
        elif self._nexts_map.contains_entry("Annotation", self.current_token.token_name):
            return None
        else:
            raise SyntacticException(self.current_token, self.concatenated_first_and_next_lists("Annotation"))

    def signature(self):
        instruction_token = self.current_token
        instruction = None
        match instruction_token.token_name:
            case "pr_setd":
                instruction = SetDInstruction(instruction_token, self._address)
                self.match("pr_setd")
                argument1 = self.expression()
                self.match("comma")
                argument2 = self.expression()
                instruction.set_argument1(ExpressionNode(argument1))
                instruction.set_argument2(ExpressionNode(argument2))
            case "pr_seth":
                instruction = SetHInstruction(instruction_token, self._address)
                self.match("pr_seth")
                argument1 = self.expression()
                self.match("comma")
                argument2 = self.expression()
                instruction.set_argument1(ExpressionNode(argument1))
                instruction.set_argument2(ExpressionNode(argument2))
            case "pr_setactual":
                instruction = SetActualInstruction(instruction_token, self._address)
                self.match("pr_setactual")
                argument1 = self.expression()
                instruction.set_argument1(ExpressionNode(argument1))
            case "pr_setlibre":
                instruction = SetLibreInstruction(instruction_token, self._address)
                self.match("pr_setlibre")
                argument1 = self.expression()
                instruction.set_argument1(ExpressionNode(argument1))
            case "pr_setin":
                instruction = SetInInstruction(instruction_token, self._address)
                self.match("pr_setin")
                argument1 = self.expression()
                instruction.set_argument1(ExpressionNode(argument1))
            case "pr_setout":
                instruction = SetOutInstruction(instruction_token, self._address)
                self.match("pr_setout")
                argument1 = self.expression()
                instruction.set_argument1(ExpressionNode(argument1))
            case "pr_setpo":
                instruction = SetPOInstruction(instruction_token, self._address)
                self.match("pr_setpo")
                argument1 = self.expression()
                instruction.set_argument1(ExpressionNode(argument1))
            case "pr_setlabel":
                instruction = SetLabelInstruction(instruction_token, self._address)
                self.match("pr_setlabel")
                identifier_token = self.current_token
                self.match("identifier")
                self.match("comma")
                argument2 = self.expression()
                instruction.set_argument1(identifier_token)
                instruction.set_argument2(ExpressionNode(argument2))
            case "pr_jumpt":
                instruction = JumpTInstruction(instruction_token, self._address)
                self.match("pr_jumpt")
                argument1 = self.expression()
                self.match("comma")
                argument2 = self.expression()
                instruction.set_argument1(ExpressionNode(argument1))
                instruction.set_argument2(ExpressionNode(argument2))
            case "pr_jump":
                instruction = JumpInstruction(instruction_token, self._address)
                self.match("pr_jump")
                argument1 = self.expression()
                instruction.set_argument1(ExpressionNode(argument1))
            case "pr_halt":
                instruction = HaltInstruction(instruction_token, self._address)
                self.match("pr_halt")
        self.increase_address()
        return instruction

    def expression(self):
        if self._firsts_map.contains_entry("UnaryOp", self.current_token.token_name):
            unary_op_node = self.unary_op()
            operand_node = self.operand()
            unary_op_node.set_operand_node(operand_node)
            return self.expression_remainder(unary_op_node)
        elif self._firsts_map.contains_entry("Operand", self.current_token.token_name):
            operand_node = self.operand()
            return self.expression_remainder(operand_node)
        elif self._nexts_map.contains_entry("Expression", self.current_token.token_name):
            return None
        else:
            raise SyntacticException(self.current_token, self.concatenated_first_and_next_lists("Expression"))

    def unary_op(self):
        unary_op_node = None
        match self.current_token.token_name:
            case "plus":
                unary_op_node = PlusNode(self.current_token)
                self.match("plus")
            case "minus":
                unary_op_node = MinusNode(self.current_token)
                self.match("minus")
            case "not":
                unary_op_node = NotNode(self.current_token)
                self.match("not")

        return unary_op_node

    def expression_remainder(self, unary_op_or_operand):
        if self._firsts_map.contains_entry("ExpressionRemainder", self.current_token.token_name):
            binary_op_node = self.binary_op()    
            binary_op_node.set_left_side(unary_op_or_operand)        
            sub_expression = self.expression()
            binary_op_node.set_right_side(sub_expression)                
            return binary_op_node
        elif self._nexts_map.contains_entry("ExpressionRemainder", self.current_token.token_name):
            return unary_op_or_operand
        else:
            raise SyntacticException(self.current_token, self.concatenated_first_and_next_lists("ExpressionRemainder"))

    def operand(self):
        operand_node = None
        match self.current_token.token_name:
            case "pr_d":
                data_memory_access_token = self.current_token
                self.match("pr_d")
                self.match("open_square_bracket")
                sub_expression_node = self.expression()                
                self.match("close_square_bracket")
                operand_node = DataMemoryAccessNode(data_memory_access_token, sub_expression_node)
            case "pr_h":
                heap_memory_access_token = self.current_token
                self.match("pr_h")
                self.match("open_square_bracket")
                sub_expression_node = self.expression()
                self.match("close_square_bracket")
                operand_node = HeapMemoryAccessNode(heap_memory_access_token, sub_expression_node)
            case "pr_actual":
                operand_node = ActualNode(self.current_token)
                self.match("pr_actual")                
            case "pr_libre":
                operand_node = LibreNode(self.current_token)
                self.match("pr_libre")                
            case "int":
                operand_node = IntNode(self.current_token)
                self.match("int")
            case "identifier":
                operand_node = IdentifierNode(self.current_token)
                self.match("identifier")
            case "pr_pc":
                operand_node = PCNode(self.current_token)
                self.match("pr_pc")
            case "pr_po":
                operand_node = PONode(self.current_token)
                self.match("pr_po")
            case "open_parenthesis":
                self.match("open_parenthesis")
                sub_expression_node = self.expression()
                self.match("close_parenthesis")
                operand_node = ParenthesizedExpressionNode(sub_expression_node)

        return operand_node
            
    def binary_op(self):
        binary_op_node = None
        if self._firsts_map.contains_entry("BinaryOp", self.current_token.token_name):
            binary_op_node = BinaryOpNode(self.current_token)
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
            return binary_op_node        
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
        
    def increase_address(self):
        self._address += 1