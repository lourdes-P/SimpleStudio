from logic.processor.instructions.instruction import Instruction
from logic.processor.instructions.halt_instruction import HaltInstruction
from logic.processor.instructions.jump_instruction import JumpInstruction
from logic.processor.instructions.jumpt_instruction import JumpTInstruction
from logic.processor.instructions.setactual_instruction import SetActualInstruction
from logic.processor.instructions.setlibre_instruction import SetLibreInstruction
from logic.processor.instructions.setd_instruction import SetDInstruction
from logic.processor.instructions.seth_instruction import SetHInstruction
from logic.processor.instructions.setlabel_instruction import SetLabelInstruction
from logic.processor.instructions.setin_instruction import SetInInstruction
from logic.processor.instructions.setout_instruction import SetOutInstruction
from logic.processor.instructions.setpo_instruction import SetPOInstruction


__all__ = [ 'Instruction', 'HaltInstruction', 'JumpInstruction', 'JumpTInstruction', 'SetActualInstruction',
           'SetLibreInstruction', 'SetDInstruction', 'SetHInstruction', 'SetLabelInstruction', 'SetInInstruction',
           'SetOutInstruction', 'SetPOInstruction']