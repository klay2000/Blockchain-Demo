import hashlib
import random
from tkinter import *
from tkinter import ttk

class Block:
    def __init__(self, data, prev):
        self.data = data
        self.prev = prev
        if prev is None:
            self.prev_hash = ""
        else:
            self.prev_hash = prev.hash_of()

    def hash_of(self):
        return hashlib.sha256((str(self.data) + str(self.prev_hash)).encode('UTF-8')).hexdigest()


class BlockChain:
    chainSize = 0

    def __init__(self, genesis_block):
        self.topBlock = genesis_block

        block_list.insert(block_list.size(), "Initial Block")

    def add(self, data):
        self.topBlock = Block(data, self.topBlock)
        self.chainSize += 1

        block_list.insert(block_list.size(), "Block #" + str(block_list.size()))

    def fetch_from_top(self, index, top=None):
        if top is None:
            top = self.topBlock

        if index == 0:
            return top

        return self.fetch_from_top(index - 1, top.prev)

    def fetch(self, index):
        return self.fetch_from_top(self.chainSize - index)

    def remove_from_top(self, index):
        if index == 0:
            self.topBlock = self.topBlock.prev
        elif index == self.chainSize:
            self.fetch(1).prev = None
        else:
            self.fetch_from_top(index-1).prev = self.fetch_from_top(index).prev
        self.chainSize -= 1

        block_list.delete(self.chainSize+1-index)

    def remove(self, index):
        return self.remove_from_top(self.chainSize - index)

    def validate(self, verbose=False):
        n = self.topBlock
        a = 1
        valid = True

        while n.prev is not None:
            if verbose:
                print("hash of block " + str(a) + " from top of chain: " + str(n.prev.hash_of()))
                print("expected hash of " + str(a) + ": " + str(n.prev_hash))

            if n.prev_hash != n.prev.hash_of():
                if verbose:
                    print('\033[91m' + "BLOCK " + str(a) + " INVALID!" + '\033[0m')
                valid = False
            n = n.prev
            a += 1

        valid_label.config(text=("valid" if valid else "invalid!"))

        return valid


def select_block(evt):
    selected_block = chain.fetch(block_list.curselection()[0])
    block_num.set("Block #" + str(block_list.curselection()[0]))
    block_data.set(selected_block.data)
    block_prev_hash.set(selected_block.prev_hash)
    block_hash.set(selected_block.hash_of())


def update_block(var, index, mode):
    selected_block = chain.fetch(block_list.curselection()[0])
    selected_block.data = block_data.get()
    block_hash.set(selected_block.hash_of())


# setting up the window
root = Tk()
root.title("Blockchain Demonstrator")


# adding the content frame
main_frame = ttk.Frame(root)
main_frame.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=4)
main_frame.columnconfigure(2, weight=1)


# adding the block list and preparing the chain
list_frame = ttk.Frame(main_frame)
list_frame.grid(column=0, row=0, sticky=(N, W, S))
block_list = Listbox(list_frame, exportselection=False)
block_list.grid(column=0, row=0)
block_list.bind('<<ListboxSelect>>', select_block)
add_sub_frame = ttk.Frame(list_frame)
add_sub_frame.grid(column=0, row=1)

# prepare the blockchain
chain = BlockChain(Block("0123456789", None))
chain.add("a block")
chain.add("another block")
chain.add("a third block")
chain.add("a fourth block")

Button(add_sub_frame, text="Add Block", command=lambda: chain.add(str(random.randint(0, 1000000))))\
    .grid(column=0, row=0)
Button(add_sub_frame, text="Delete Block", command=lambda: chain.remove(block_list.curselection()[0]))\
    .grid(column=1, row=0)
Button(list_frame, text="validate Chain", command=lambda: chain.validate(verbose=True)).grid(column=0, row=2)
valid_label = Label(list_frame)
valid_label.grid(column=0, row=3)

# adding the block editor and preparing vars
block_num = StringVar()
block_data = StringVar()
block_prev_hash = StringVar()
block_hash = StringVar()

block_edit_container = ttk.Frame(main_frame)
block_edit_container.grid(column=1, row=0, sticky=(N, S))

num = ttk.Label(block_edit_container, textvariable=block_num)
num.grid(column=0, row=0)
num.config(font=("arial", 20))

block_edit = ttk.Frame(block_edit_container)
block_edit.grid(column=0, row=1, sticky=(N, S))

ttk.Label(block_edit, text="Block Data: ").grid(column=0, row=1)

data_box = ttk.Entry(block_edit, textvariable=block_data)
data_box.grid(column=1, row=1)
block_data.trace_add("write", update_block)

ttk.Label(block_edit, text="Previous Block's Hash: ").grid(column=0, row=2)
ttk.Label(block_edit, textvariable=block_prev_hash).grid(column=1, row=2)

ttk.Label(block_edit, text="Block's Hash: ").grid(column=0, row=3)
ttk.Label(block_edit, textvariable=block_hash).grid(column=1, row=3)


block_list.select_set(0)
select_block(None)

root.mainloop()
