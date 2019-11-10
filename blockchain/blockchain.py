import hashlib
import json
import time


class Block:

    def __init__(self, transactions: list, previous = None):
        # Transactions are simplified into a list
        self.header = {
            'previous': previous,
            'merkle_root': hashlib.sha256(json.dumps(transactions).encode('ascii')).hexdigest(),
            'time': time.time()
        }

        self.transactions: list = transactions

    @property
    def hash(self):
        return hashlib.sha256(json.dumps(self.header).encode('ascii')).hexdigest()

    def __call__(self) -> dict:
        transactions: dict = {}
        for i in range(len(self.transactions)):
            transactions[f'{i}'] = self.transactions[i]

        return {
            'header': self.header,
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
        block.header['previous'] = self.blocks[-1].hash
        self.blocks.append(block)

    def verify(self) -> bool:
        for i in range(len(self.blocks) - 1):
            if self.blocks[i].hash != self.blocks[i + 1].header['previous']:
                return False
        return True

    def __str__(self) -> str:
        blockchain_json: dict = {}
        for i in range(len(self.blocks)):
            blockchain_json['block' + f'{i}'] = self.blocks[i]()
        
        return json.dumps(blockchain_json)


def import_chain(chain_json: (str, dict)) -> Blockchain:
    if isinstance(chain_json, str):
        chain_json: dict = json.loads(chain_json)
    chain = None

    for key, value in chain_json.items():
        trans = []
        for num, transaction in value['transactions'].items():
            trans.append(transaction)
        if key == 'block0':
            chain = Blockchain(trans)
        else:
            block = Block(trans)
            block.header = value['header']
            chain.add(block)

    return chain


if __name__ == '__main__':
    with open('blockchain/blockchains.json', 'r') as file:
        chains = file.read()
    chains = json.loads(chains)
    chain = import_chain(chains['chain0'])
    print(chain)