from flask import request
import json

def find_new_chains(peer_nodes):
  # Get the blockchains of every
  # other node
  other_chains = []
  for node_url in peer_nodes:
    # Get their chains using a GET request
    block = requests.get(node_url + "/blocks").content
    # Convert the JSON object to a Python dictionary
    block = json.loads(block)
    # Add it to our list
    other_chains.append(block)
  return other_chains

# For use on single node system
def consensus(blockchain, peer_nodes):
  print "Consensus called!"
  # Get the blocks from other nodes
  other_chains = find_new_chains(peer_nodes)
  # If our chain isn't longest,
  # then we store the longest chain
  longest_chain = blockchain
  for chain in other_chains:
    if len(longest_chain) < len(chain):
      longest_chain = chain
  # If the longest chain isn't ours,
  # then we stop mining and set
  # our chain to the longest one
  blockchain = longest_chain

'''
# To be tested on multi-node system
def consensus(blockchain, peer_nodes):
  bool fraud
  # Get the blocks from other nodes
  other_chains = find_new_chains(peer_nodes)
  # Get current blockchain
  current_chain = blockchain
  for chain in other_chains:
    fraud = false
    if(len(current_chain) < len(chain)):
      for i in range(len(chain)):
        if(current_chain[i].hash != chain[i].hash):
            print "Fraudalence Detected"
            fraud = true
        if(fraud):
          break
      if(!fraud):
        current_chain = chain
  blockchain = current_chain
  '''

def proof_of_work(last_proof):
  # Create a variable that we will use to find
  # our next proof of work
  incrementor = last_proof + 1
  # Keep incrementing the incrementor until
  # it's equal to a number divisible by 9
  # and the proof of work of the previous
  # block in the chain
  while not (incrementor % 9 == 0 and incrementor % last_proof == 0):
    incrementor += 1
  # Once that number is found,
  # we can return it as a proof
  # of our work
  return incrementor