import hashlib
import tkinter as tk

class Block:
    def __init__(self, data, prev):
        self.data = data
        self.prev = prev
        if prev == None:
            self.prevHash = ""
        else:
            self.prevHash = prev.hashOf()

    def hashOf(self):
        return hashlib.sha256((str(self.data) + str(self.prevHash)).encode('UTF-8')).hexdigest()


class BlockChain:
    chainSize = 0

    def __init__(self, genesisBlock):
        self.topBlock = genesisBlock

    def add(self, data):
        self.topBlock = Block(data, self.topBlock)
        self.chainSize += 1

    def fetch(self, index, top=None):
        if top == None: top = self.topBlock

        if index == 0: return top

        return self.fetch(index - 1, top.prev)

    def fetch_from_bottom(self, index):
        return self.fetch(self.chainSize - index)

    def validate(self, verbose=False):
        n = self.topBlock
        a = 1
        valid = True

        while n.prev != None:
            if verbose: print("hash of block " + str(a) + " from top of chain: " + str(n.prev.hashOf()))
            if verbose: print("expected hash of " + str(a) + ": " + str(n.prevHash))
            if n.prevHash != n.prev.hashOf():
                if verbose: print('\033[91m' + "BLOCK " + str(a) + " INVALID!" + '\033[0m')
                valid = False
            n = n.prev
            a += 1

        return valid


app = tk.Tk()

app.mainloop()
