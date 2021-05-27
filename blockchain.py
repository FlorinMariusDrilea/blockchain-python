# Libaries
import datetime
import hashlib
import json
from flask import Flask, jsonify

# Building a Blockchain
class Blockchain:
    def __init__(self):
        self.chain = []
        self.creating_block(p = 1, previous_hash = '0')
        
    def creating_block(self, p, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': p,
                 'previous_hash': previous_hash}
        self.chain.append(block)
        return block;
    
    def get_prev_block(self):
        return self.chain[-1]
    
    def proof_working(self, previous_p):
        new_p= 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_p**2 + previous_p**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else: 
                new_p += 1
        return new_p
            
    def hashing(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()        
    
    def chain_validation(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hashing(previous_block):
                return False
            previous_p = previous_block['proof']
            p = block['proof']
            hash_operation = hashlib.sha256(str(p**2 + previous_p**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index +=1
        return True
    
# Mine blocks with postman using flask
app = Flask(__name__)

blockchain = Blockchain()

@app.route('/mining', methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_prev_block()
    previous_p = previous_block['proof']
    p = blockchain.proof_working(previous_p)
    previous_hash = blockchain.hashing(previous_block)
    block = blockchain.creating_block(p, previous_hash)
    response = {'message' : 'You mined a block!',
                'index' : block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash':block['previous_hash']}
    return jsonify(response), 200

@app.route('/get_full_chain', methods = ['GET'])
def get_chain():
    response = {'message': 'Here is the complete blockchain',
                'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

@app.route('/verify', methods = ['GET'])
def verify():
    verification = blockchain.chain_validation(blockchain.chain)
    if verification:
        response = {'message': 'The blockchain is valid!'}
    else:
        response = {'message' : 'The blockchain is not valid! Warning!'}
    return jsonify(response), 200

app.run(host = '0.0.0.0', port=5000)