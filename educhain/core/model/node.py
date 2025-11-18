from ..utils.crypto_utils import CryptoUtils
from .blockchain import Blockchain
from .block import Block


class ValidatorNode:
    def __init__(self, blockchain: Blockchain, validator_private_key: str):
        self.bc = blockchain
        self.priv = validator_private_key
        self.pub = CryptoUtils.get_public_key(self.priv)

    def mine_once(self):
        return self.bc.mine_block(self.priv)
