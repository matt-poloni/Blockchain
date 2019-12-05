# Paste your version of blockchain.py from the client_mining_p
# folder here

import hashlib
import json
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request


DIFFICULTY = 6


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.new_block(previous_hash='===============', proof=100)
        self.next_transaction = 1

    def new_block(self, proof, previous_hash=None):
        """
        Create a new Block in the Blockchain

        A block should have:
        * Index
        * Timestamp
        * List of current transactions
        * The proof used to mine this block
        * The hash of the previous block

        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }
        self.current_transactions = []
        self.chain.append(block)
        return block

    def hash(self, block):
        """
        Creates a SHA-256 hash of a Block

        :param block": <dict> Block
        "return": <str>
        """
        block_string = json.dumps(block, sort_keys=True).encode()
        hash = hashlib.sha256(block_string).hexdigest()
        return hash

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def valid_proof(block_string, proof):
        """
        Validates the Proof:  Does hash(block_string, proof) contain 3
        leading zeroes?  Return true if the proof is valid
        :param block_string: <string> The stringified block to use to
        check in combination with `proof`
        :param proof: <int?> The value that when combined with the
        stringified previous block results in a hash that has the
        correct number of leading zeroes.
        :return: True if the resulting hash is a valid proof, False otherwise
        """

        guess = f'{block_string}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        return guess_hash[:DIFFICULTY] == "0" * DIFFICULTY

    def new_transaction(self, sender, recipient, amount):
        """
        Create a method in the `Blockchain` class called `new_transaction` 
        that adds a new transaction to the list of transactions:

            :param sender: <str> Address of the Recipient
            :param recipient: <str> Address of the Recipient
            :param amount: <int> Amount
            :return: <int> The index of the `block` that will hold this transaction
        """
        transaction = {
          "id": self.next_transaction,
          "sender": sender,
          "recipient": recipient,
          "amount": amount
        }
        self.next_transaction += 1
        self.current_transactions.append(transaction)
    
    def user_transactions(self, user):
        chain = [*self.chain, {'transactions': self.current_transactions}]
        transactions = []
        for link in chain:
            for trx in link['transactions']:
                if any(v == user for v in [trx['sender'], trx['recipient'] ]):
                    transactions.append(trx)
        return transactions
    
    def user_balance(self, user, transactions):
        balance = 0
        for trx in transactions:
            balance += int(trx['recipient'] == user)
            balance -= int(trx['sender'] == user)
        return balance

from flask_cors import CORS
# Instantiate our Node
app = Flask(__name__)
CORS(app)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['POST'])
def mine():
    # Handle non-json responses
    try:
        data = request.get_json()
    except ValueError:
        response = {
          "message": "Non-JSON response"
        }
        return jsonify(response), 400
    
    # Pull data out of request
    required = ["proof", "id", "index"]
    if data is None or not all(keys in data for keys in required):
        response = {
          "message": "At least one of 'proof', 'id', and/or 'index' is missing"
        }
        return jsonify(response), 400
    
    # Check if block's already been forged
    last = blockchain.last_block
    if (index := data["index"]) <= last["index"]:
        response = {
          "message": f"Block {index} Already Forged"
        }
        return jsonify(response), 409

    block_string = json.dumps(last, sort_keys=True)
    proof = data['proof']
    if blockchain.valid_proof(block_string, proof):
        # Forge the new Block by adding it to the chain with the proof
        previous_hash = blockchain.hash(last)
        blockchain.new_block(proof, previous_hash)
        blockchain.new_transaction("0", data["id"], 1)
        response = {
            'message': "New Block Forged"
        }
        status = 201
    else:
        response = {
          'message': "Invalid Block"
        }
        status = 400
    return jsonify(response), status


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'length': len(blockchain.chain),
        'chain': blockchain.chain
    }
    return jsonify(response), 200

@app.route('/last_block', methods=['GET'])
def last():
    response = {
        'block': blockchain.last_block,
        'difficulty': DIFFICULTY
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def post_transaction():
    # Handle non-json responses
    try:
        data = request.get_json()
    except ValueError:
        response = {
          "message": "Non-JSON response"
        }
        return jsonify(response), 400
    
    # Pull data out of request
    required = ["sender", "recipient", "amount"]
    if data is None or not all(keys in data for keys in required):
        response = {
          "message": "At least one of 'sender', 'recipient', and/or 'amount' is missing"
        }
        return jsonify(response), 400
    blockchain.new_transaction(data["sender"], data["recipient"], data["amount"])

    last = blockchain.last_block
    response = {
      "block_index": last["index"],
      "block": last
    }
    return jsonify(response), 201

@app.route('/transactions/user/<user>', methods=['GET'])
def get_transactions(user):
    transactions = blockchain.user_transactions(user)
    balance = blockchain.user_balance(user, transactions)
    response = {
      "transactions": transactions,
      "balance": balance
    }
    return jsonify(response), 200

# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
