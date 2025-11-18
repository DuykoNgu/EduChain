from flask import Flask, request, jsonify
from educhain.core.model.transaction import Transaction


def create_app(blockchain):
    app = Flask(__name__)

    @app.route('/submit_transaction', methods=['POST'])
    def submit_transaction():
        tx_data = request.get_json()
        if not tx_data:
            return jsonify({"error": "No data"}), 400
        try:
            tx = Transaction.from_dict(tx_data)
            if blockchain.add_transaction_to_mempool(tx):
                return jsonify({"message": "Added to mempool", "tx_hash": tx.tx_hash}), 201
            else:
                return jsonify({"error": "Invalid tx or duplicate"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/mine_block', methods=['POST'])
    def mine_block():
        data = request.get_json()
        validator_private_key = data.get('validator_private_key')
        if not validator_private_key:
            return jsonify({"error": "validator_private_key required"}), 400
        new_block = blockchain.mine_block(validator_private_key)
        if new_block:
            return jsonify({"message": f"Mined block {new_block.index}", "block": new_block.to_dict()}), 200
        else:
            return jsonify({"error": "Mining failed (not your turn or other)"}), 403

    @app.route('/get_chain_status', methods=['GET'])
    def get_chain_status():
        last = blockchain.get_last_block()
        return jsonify({"length": len(blockchain.chain), "last_index": last.index, "last_hash": last.hash})

    @app.route('/get_block', methods=['GET'])
    def get_block():
        idx = request.args.get('index')
        try:
            i = int(idx)
        except Exception:
            return jsonify({"error": "invalid index"}), 400
        if i < 0 or i >= len(blockchain.chain):
            return jsonify({"error": "index out of range"}), 404
        return jsonify(blockchain.chain[i].to_dict()), 200

    @app.route('/query_nft_owner', methods=['GET'])
    def query_nft_owner():
        nft_id = request.args.get('nft_id')
        if not nft_id:
            return jsonify({"error": "nft_id required"}), 400
        owner = blockchain.state_db.get('nfts', {}).get(nft_id)
        if not owner:
            return jsonify({"owner": None}), 200
        return jsonify(owner), 200

    return app
