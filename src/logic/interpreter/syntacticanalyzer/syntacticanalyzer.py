from logic.expression_ast.expression_node import ExpressionNode
from logic.interpreter.syntacticanalyzer.syntacticexceptions import *
from logic.memories.codememory.codecell import CodeCell
from logic.memories.codememory.codememory import CodeMemory
from logic.processor.instructions import *
from logic.expression_ast.binaryop_nodes import *
from logic.expression_ast.unaryop_nodes import *
from logic.expression_ast.operand_nodes import *
from logic.interpreter.utils import MapManager, OperatorPrecedenceManager

class SyntacticAnalyzer:

    def __init__(self, lexical_analyzer, code_memory, firsts_map = MapManager("resources/firsts.csv"), nexts_map = MapManager("resources/nexts.csv"), operator_precedence_manager = OperatorPrecedenceManager()):
        self.current_token = None
        self.lexical_analyzer = lexical_analyzer
        self._code_memory = code_memory
        self._firsts_map = firsts_map
        self._nexts_map = nexts_map
        self._no_errors = True
        self._address = 0       # suma por cada instrucción que se guarda en la memoria C, incremento en 1
        self._operator_precedence_manager = operator_precedence_manager
        self._label_dictionary = {}
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
            self.add_label_to_dictionary(label, self._address)
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
                self.check_invalid_string_argument(argument1, instruction_token.lexeme)
                self.match("comma")
                argument2 = self.expression()
                instruction.set_argument1(ExpressionNode(argument1))
                instruction.set_argument2(ExpressionNode(argument2))
            case "pr_seth":
                instruction = SetHInstruction(instruction_token, self._address)
                self.match("pr_seth")
                argument1 = self.expression()
                self.check_invalid_string_argument(argument1, instruction_token.lexeme)                
                self.match("comma")
                argument2 = self.expression()
                instruction.set_argument1(ExpressionNode(argument1))
                instruction.set_argument2(ExpressionNode(argument2))
            case "pr_setactual":
                instruction = SetActualInstruction(instruction_token, self._address)
                self.match("pr_setactual")
                argument1 = self.expression()
                self.check_invalid_string_argument(argument1, instruction_token.lexeme)
                instruction.set_argument1(ExpressionNode(argument1))
            case "pr_setlibre":
                instruction = SetLibreInstruction(instruction_token, self._address)
                self.match("pr_setlibre")
                argument1 = self.expression()
                self.check_invalid_string_argument(argument1, instruction_token.lexeme)
                instruction.set_argument1(ExpressionNode(argument1))
            case "pr_setin":
                instruction = SetInInstruction(instruction_token, self._address)
                self.match("pr_setin")
                argument1 = self.expression()
                self.check_invalid_string_argument(argument1, instruction_token.lexeme)
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
                self.check_invalid_string_argument(argument1, instruction_token.lexeme)
                instruction.set_argument1(ExpressionNode(argument1))
            case "pr_setlabel":
                instruction = SetLabelInstruction(instruction_token, self._address)
                self.match("pr_setlabel")
                identifier_token = self.current_token
                self.match("identifier")
                self.match("comma")
                argument2 = self.expression()
                self.check_invalid_string_argument(argument2, instruction_token.lexeme)
                instruction.set_argument1(identifier_token)
                instruction.set_argument2(ExpressionNode(argument2))
            case "pr_jumpt":
                instruction = JumpTInstruction(instruction_token, self._address)
                self.match("pr_jumpt")
                argument1 = self.expression()
                self.check_invalid_string_argument(argument1, instruction_token.lexeme)
                self.match("comma")
                argument2 = self.expression()
                self.check_invalid_string_argument(argument2, instruction_token.lexeme)
                instruction.set_argument1(ExpressionNode(argument1))
                instruction.set_argument2(ExpressionNode(argument2))
            case "pr_jump":
                instruction = JumpInstruction(instruction_token, self._address)
                self.match("pr_jump")
                argument1 = self.expression()
                self.check_invalid_string_argument(argument1, instruction_token.lexeme)
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
            return self.expression_remainder_2(unary_op_node)
        elif self._firsts_map.contains_entry("Operand", self.current_token.token_name):
            operand_node = self.operand()
            return self.expression_remainder_2(operand_node)
        elif self._nexts_map.contains_entry("Expression", self.current_token.token_name):
            return None
        else:
            raise SyntacticException(self.current_token, self.concatenated_first_and_next_lists("Expression"))

    def unary_op_or_operand(self):
        if self._firsts_map.contains_entry("UnaryOp", self.current_token.token_name):
            unary_op_node = self.unary_op()
            operand_node = self.operand()
            self.check_string_operand_validity_unary(unary_op_node.token, operand_node)
            unary_op_node.set_operand_node(operand_node)
            return unary_op_node
        elif self._firsts_map.contains_entry("Operand", self.current_token.token_name):
            operand_node = self.operand()
            return operand_node
        else:
            raise SyntacticException(self.current_token, self.concatenated_first_and_next_lists("UnaryOp").extend(self.concatenated_first_and_next_lists("Operand")))

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
            case _:
                raise SyntacticException(self.current_token, self.concatenated_first_and_next_lists("UnaryOp"))


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
            case 'string':
                operand_node = StringNode(self.current_token)
                self.match("string")
            case _:
                raise SyntacticException(self.current_token, self.concatenated_first_and_next_lists("Operand"))

        return operand_node
            
    def expression_remainder_2(self, unary_op_or_operand):
        if self._firsts_map.contains_entry("ExpressionRemainder", self.current_token.token_name):
            return self.parse_binary_operation(-1, unary_op_or_operand)
        elif self._nexts_map.contains_entry("ExpressionRemainder", self.current_token.token_name):
            return unary_op_or_operand
        else:
            raise SyntacticException(self.current_token, self.concatenated_first_and_next_lists("ExpressionRemainder"))
          
    def parse_binary_operation(self, former_operator_precedence, left_side):
        while True:
            if not self._firsts_map.contains_entry("ExpressionRemainder", self.current_token.token_name):
                return left_side
            binary_operator = self.current_token

            current_operator_precedence = int(self.get_operator_precedence(binary_operator))

            if (current_operator_precedence < former_operator_precedence):
                return left_side            
            
            binary_operator_node = self.binary_op() # le asigno el operador en el medio, me falta izquierda y derecha
            
            right_side = self.unary_op_or_operand()
            
            self.check_string_operand_validity_binary(left_side, binary_operator, right_side)
            
            if self._firsts_map.contains_entry("ExpressionRemainder", self.current_token.token_name):
                next_operator = self.current_token
                next_operator_precedence = int(self.get_operator_precedence(next_operator))
                
                if current_operator_precedence < next_operator_precedence:
                    right_side = self.parse_binary_operation(current_operator_precedence+1, right_side)
                    
            binary_operator_node.set_left_side(left_side)
            binary_operator_node.set_right_side(right_side)
            left_side = binary_operator_node
            
    def binary_op(self):
        binary_op_node = None
        if self._firsts_map.contains_entry("BinaryOp", self.current_token.token_name):
            match self.current_token.token_name:
                case "plus":
                    binary_op_node = AdditionNode(self.current_token)
                    self.match("plus")                    
                case "minus":
                    binary_op_node = SubtractionNode(self.current_token)
                    self.match("minus")
                case "multiplication":
                    binary_op_node = MultiplicationNode(self.current_token)
                    self.match("multiplication")
                case "division":
                    binary_op_node = DivisionNode(self.current_token)
                    self.match("division")
                case "equals":
                    binary_op_node = EqualsNode(self.current_token)
                    self.match("equals")
                case "different":
                    binary_op_node = DiffersNode(self.current_token)
                    self.match("different")
                case "lesser":
                    binary_op_node = LesserNode(self.current_token)
                    self.match("lesser")
                case "lesser_or_equal":
                    binary_op_node = LesserOrEqualNode(self.current_token)
                    self.match("lesser_or_equal")
                case "greater":
                    binary_op_node = GreaterNode(self.current_token)
                    self.match("greater")
                case "greater_or_equal":
                    binary_op_node = GreaterOrEqualNode(self.current_token)
                    self.match("greater_or_equal")
                case "and":
                    binary_op_node = AndNode(self.current_token)
                    self.match("and")
                case "or":
                    binary_op_node = OrNode(self.current_token)
                    self.match("or")
                case "mod":
                    binary_op_node = ModulusNode(self.current_token)
                    self.match("mod")
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
        
    def get_operator_precedence(self, binary_operator_token):
        return self._operator_precedence_manager.get_precedence(binary_operator_token.token_name)
    
    def check_string_operand_validity_binary(self, left_side, binary_operator_token, right_side):
        if self.check_if_string(left_side) and left_side.__class__.__name__ == right_side.__class__.__name__ and (binary_operator_token.token_name == 'equals' or binary_operator_token.token_name == 'different'):
            pass
        elif self.check_if_string(left_side) and left_side.__class__.__name__ == right_side.__class__.__name__ and (binary_operator_token.token_name != 'equals' and binary_operator_token.token_name != 'different'):
            raise StringInvalidOperatorSyntacticException(binary_operator_token)
        elif self.check_if_string(right_side) and left_side.__class__.__name__ != right_side.__class__.__name__:
            raise StringInvalidComparationSyntacticException(left_side.token)
        elif self.check_if_string(left_side) and left_side.__class__.__name__ != right_side.__class__.__name__:
            raise StringInvalidComparationSyntacticException(right_side.token)
        else:
            pass
        
    def check_string_operand_validity_unary(self, unary_operator_token, operand):
        if operand.__class__.__name__ == 'StringNode':
            raise StringInvalidUnaryOperationSyntacticException(unary_operator_token)
        
    def check_invalid_string_argument(self, node, instruction_name):
        if self.check_if_string(node):
            raise InstructionInvalidStringArgumentSyntacticException(node.token, instruction_name)            
        
    def check_if_string(self, node):
        return True if node.__class__.__name__ == 'StringNode' else False
    
    def add_label_to_dictionary(self, label_token, address):
        label_name = str.lower(label_token.lexeme)
        if self._label_dictionary.get(label_name) == None:
            self._label_dictionary[label_name] = address
        else:
            raise DuplicatedLabelSyntacticException(label_token)
        
    def get_label_dictionary(self):
        return self._label_dictionary.copy()