from flask import Flask, request, jsonify
import hashlib, time, os, json
import config

app = Flask(__name__)
blockchain = []
mempool = []
current_difficulty = config.INITIAL_DIFFICULTY

def create_genesis():
    if not blockchain:
        genesis = {
            "index": 0, 
            "timestamp": time.time(), 
            "transactions": [], 
            "hash": "0", 
            "prev": "0", 
            "nonce": 0,
            "difficulty": current_difficulty
        }
        blockchain.append(genesis)

def adjust_difficulty():
    """Adjusts difficulty every X blocks based on time taken."""
    global current_difficulty
    if len(blockchain) % config.ADJUSTMENT_INTERVAL != 0 or len(blockchain) < config.ADJUSTMENT_INTERVAL:
        return

    # Calculate time taken for the last 'n' blocks
    last_adjustment_block = blockchain[-config.ADJUSTMENT_INTERVAL]
    time_taken = blockchain[-1]['timestamp'] - last_adjustment_block['timestamp']
    expected_time = config.TARGET_BLOCK_TIME * config.ADJUSTMENT_INTERVAL

    print(f"Adjustment Check: Time taken {time_taken}s | Expected {expected_time}s")

    if time_taken < expected_time / 2:
        current_difficulty += 1
        print(f"Difficulty INCREASED to {current_difficulty}")
    elif time_taken > expected_time * 2 and current_difficulty > 1:
        current_difficulty -= 1
        print(f"Difficulty DECREASED to {current_difficulty}")

@app.route('/mine', methods=['GET'])
def mine():
    adjust_difficulty() # Check for difficulty update before mining
    
    last_block = blockchain[-1]
    new_block = {
        "index": len(blockchain),
        "timestamp": time.time(),
        "transactions": mempool[:],
        "prev": last_block['hash'],
        "nonce": 0,
        "difficulty": current_difficulty
    }
    
    # Proof of Work loop
    target = "0" * current_difficulty
    while True:
        block_string = json.dumps(new_block, sort_keys=True).encode()
        res = hashlib.sha256(block_string).hexdigest()
        if res.startswith(target):
            new_block['hash'] = res
            break
        new_block['nonce'] += 1
        
    blockchain.append(new_block)
    mempool.clear()
    return jsonify({
        "message": "Block Mined!",
        "block": new_block,
        "current_difficulty": current_difficulty
    })

@app.route('/chain', methods=['GET'])
def get_chain():
    return jsonify({
        "length": len(blockchain),
        "chain": blockchain,
        "difficulty": current_difficulty
    })

if __name__ == '__main__':
    create_genesis()
    print(f"BDcoin Node Started on Port {config.PORT}")
    app.run(host='0.0.0.0', port=config.PORT)
