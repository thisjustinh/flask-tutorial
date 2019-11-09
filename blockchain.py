import hashlib
import json


class Block:

    def __init__(self, transactions: list, previous = None):
        # Transactions are simplified into a list
        self.prev: str = previous
        self.transactions: list = transactions

    def __call__(self) -> dict:
        transactions: dict = {}
        for i in range(len(self.transactions)):
            transactions[f'{i}'] = self.transactions[i]

        return {
            'prev': self.prev,
            'transactions': transactions
        }

    def __str__(self) -> str:
        return json.dumps(self())


class Blockchain:

    def __init__(self, genesis_transactions: list):
        """
        Constructor initializes blockchain with a genesis block and an empty list of blocks
        """
        self.genesis: Block = Block(genesis_transactions)
        self.blocks: list = [self.genesis]

    def add(self, block: Block):
        self.blocks.append(block)

    def verify(self):
        pass

    def __str__(self) -> str:
        blockchain_json: dict = {}
        for i in range(len(self.blocks)):
            blockchain_json['block' + f'{i}'] = self.blocks[i]()
        
        return json.dumps(blockchain_json)
