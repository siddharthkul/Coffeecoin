# New Miner Method
@node.route(‘/mine2’, methods=[‘POST’])
def mine2():
  addressMiner = request.get_json()
  #return “1”
  if(len(this_nodes_transactions) != 0):
    # Get the last proof of work
    last_block = blockchain[len(blockchain) - 1]
    last_proof = last_block.data[‘proof-of-work’]
    # Find the proof of work for
    # the current block being mined
    # Note: The program will hang here until a new
    #       proof of work is found
    proof = proof_of_work(last_proof)
    # Once we find a valid proof of work,
    # we know we can mine a block so
    # we reward the miner by adding a transaction
    this_nodes_transactions.append(
      { “from”: “network”, “to”: addressMiner, “amount”: 1 }
      )
    # Now we can gather the data needed
    # to create the new block
    new_block_data = {
      “proof-of-work”: proof,
      “transactions”: list(this_nodes_transactions)
    }
    new_block_index = last_block.index + 1
    new_block_timestamp = this_timestamp = date.datetime.now()
    last_block_hash = last_block.hash
    # Empty transaction list
    this_nodes_transactions[:] = []
    # Now create the
    # new block!
    mined_block = Block(
      new_block_index,
      new_block_timestamp,
      new_block_data,
      last_block_hash
    )
    blockchain.append(mined_block)
    # Let the client know we mined a block
    return json.dumps({
      “index”: new_block_index,
      “timestamp”: str(new_block_timestamp),
      “data”: new_block_data,
      “hash”: last_block_hash
    }) + “\n”
  else:
    #print “Spam Miner”
    return “Sorry”

import uuid
import time
import json
import urllib
import urllib2
from random import randint

class Miner:
    def __init__(self,  miner_cpu, miner_gpu):
        #self.miner_address = uuid.uuid4()
        self.miner_address = randint(0,1000)
        self.miner_coins_earned = 0
        self.miner_cpu = miner_cpu
        self.miner_gpu = miner_gpu

miner = Miner(
    0,
    0
)

try:
    while True:
        req = urllib2.Request(“http://localhost:5000/mine2“, json.dumps({‘address’ : miner.miner_address}), headers={‘Content-type’: ‘application/json’, ‘Accept’: ‘application/json’})
        response = urllib2.urlopen(req)
        the_page = response.read()
        print the_page
        time.sleep(1)
except KeyboardInterrupt:
    print(‘interrupted!’)