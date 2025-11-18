class PoAScheduler:
    def __init__(self, blockchain):
        self.blockchain = blockchain

    def get_expected_validator(self, block_index):
        authorities = sorted(list(self.blockchain.authority_set))
        if not authorities:
            raise ValueError("Không có validator nào trong Authority Set!")
        validator_index = block_index % len(authorities)
        return authorities[validator_index]
