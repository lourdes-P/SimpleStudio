from logic.memories.codememory.codecell import CodeCell

class CodeMemory:

    def __init__(self):
        self._codecell_list = []
        self._index = 0

    def add_codecell(self, codecell):
        codecell.set_address(self._index)
        self._codecell_list.append(codecell)
        self._index += 1

    def get_codecell(self, address):
        return self._codecell_list[address]
    
    def get_instruction(self, address):
        if address < len(self._codecell_list):
            return self._codecell_list[address].instruction
        else:
            return None

    # debug function
    def print_memory(self):
        for codecell in self._codecell_list:
            codecell.print_codecell()

    @property
    def codecell_list(self):
        return self._codecell_list
