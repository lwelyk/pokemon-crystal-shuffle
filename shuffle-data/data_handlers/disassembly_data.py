import os

class DisassemblyData:
    def __init__(self):
        self.root = self.find_root()
        self.base = self.find_base()
 
    def find_root(self):
        for root, dirs, files in os.walk(os.getcwd()):
            if "constants" in dirs and "main.asm" in files:
                return root
 
    def find_base(self):
        if os.path.isfile(self.root + "/constants/16_bit_locking_constants.asm"):
            return "pokecrystal16"
        # No, this is not the best way to do this, but hey just wante a placeholder
        if os.path.isfile(self.root + "/constants/abilities.asm"):
            return "polishedcrystal"
        else:
            return "pokecrystal"