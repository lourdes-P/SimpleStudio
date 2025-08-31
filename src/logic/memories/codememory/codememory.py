from logic.memories.codememory.codecell import CodeCell

class CodeMemory:

    def __init__(self):
        self._codecell_list = []
        self._index = 0
        self._pc = 0
        

    def update_pc(self, pc):
        self._pc = pc

    def increase_pc(self):
        self._pc += 1

    def add_codecell(self, codecell):
        codecell.set_address(self._index)
        self._codecell_list.append(codecell)
        self._index += 1

    def get_codecell(self, address):
        return self._codecell_list[address]
    
    def get_next_instruction(self):
        next_instruction = self.get_instruction(self._pc)
        self.increase_pc()
        return next_instruction
    
    def get_instruction(self, address):
        return self._codecell_list[address].instruction

    # debug function
    def print_memory(self):
        for codecell in self._codecell_list:
            codecell.print_codecell()

    @property
    def codecell_list(self):
        return self._codecell_list
