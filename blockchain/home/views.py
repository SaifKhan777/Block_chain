from django.shortcuts import render, HttpResponse
from django.http import HttpResponse
import hashlib
import time
import random




def index(request):
    return render(request,'home/mainpage.html')

removedblocks = []
class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, "0", time.time(), "Genesis Block", self.calculate_hash(0, "0", time.time(), "Genesis Block"))
        self.chain.append(genesis_block)


    def create_block(self, data):
        previous_block = self.chain[-1]
        index = previous_block.index + 1
        timestamp = time.time()
        previous_hash = previous_block.hash
        hash = self.calculate_hash(index, previous_hash, timestamp, data)
        new_block = Block(index, previous_hash, timestamp, data, hash)
        self.chain.append(new_block)

    def calculate_hash(self, index, previous_hash, timestamp, data):
        value = str(index) + previous_hash + str(timestamp) + data
        return hashlib.sha256(value.encode()).hexdigest()

    def remove_random_block(self, removedblocks):
        if len(self.chain) <= 1:
            print("Cannot remove more blocks.")
            return

        random_index = random.randint(1, len(self.chain) - 1)
        if random_index not in removedblocks:
            removed_block = self.chain.pop(random_index)
            removedblocks.append(removed_block)
            print(f"Block at index {random_index} removed.")
        else:
            self.remove_random_block(removedblocks)

    def add_block_back(self, removedblocks):
        removedblocks.sort(key=lambda block: block.index)
        for block in removedblocks:
            self.chain.insert(block.index, block)
            print(f"Block added back to the chain: {block.index}")

    def print_chain(self):
        chain_output = ""
        for block in self.chain:
            chain_output += f"Index: {block.index}<br>"
            chain_output += f"Timestamp: {block.timestamp}<br>"
            chain_output += f"Previous Hash: {block.previous_hash}<br>"
            chain_output += f"Data: {block.data}<br>"
            chain_output += f"Hash: {block.hash}<br>"
            chain_output += "-" * 20 + "<br>"

        return chain_output

# Create a blockchain instance
blockchain = Blockchain()

# Create blocks
length = 20
for i in range(0, length):
    blockchain.create_block(f"Transaction Data: {i}")

# Define the 'startchain' view
def startchain(request):
        # Print the initial blockchain
    length = 1
    for i in range(0, length):
        blockchain.create_block(f"Transaction Data: {i}")
    # data = blockchain.print_chain()
    return render(request, 'home/mainpage.html')

# Define the 'chainprint' view
def chainprint(request):
    data = ""  # Initialize data as an empty string

    if request.method == 'POST':
        # Print the blockchain
        data = blockchain.print_chain()

        return render(request, 'home/chainprint.html', {'data': data})

def lock(request):
    global lockcounter
    if request.method =='POST':
        removed_length = int(length * 0.3)
        for i in range(0, removed_length):
            blockchain.remove_random_block(removedblocks)
        data = blockchain.print_chain()
        return render(request, 'home/lock.html', {'data': data})

def unlock(request):
    if request.method =='POST':
        blockchain.add_block_back(removedblocks)
        data = blockchain.print_chain()
        removedblocks.clear()
        return render(request, 'home/unlock.html', {'data': data})

def reset(request):
     if request.method =='POST':
        request.session.clear()
    
    # Redirect to the initial page or view you want to start from
        return render(request,'home/mainpage.html') 


    

