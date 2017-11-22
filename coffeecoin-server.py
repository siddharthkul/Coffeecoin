from flask import Flask
from flask import request
import json
node = Flask(__name__)
from Block import *
from coffee_functions import *
from proof_of_work import * 
import random
import hashlib

# This is the main file for Coffee Coin Experimentation
# Originally adapted from [https://gist.github.com/aunyks/47d157f8bc7d1829a729c2a6a919c173]
# Authored by Siddharth Kulkarni and Sharan Duggirala November 18th, 2017

# A completely random address of the owner of this node
#miner_address = "q3nf394hjg-random-miner-address-34nf3i4nflkn3oi"
# This node's blockchain copy
blockchain = []
blockchain.append(create_genesis_block())
# Store the transactions that
# this node has in a list
this_nodes_transactions = []

# Dictionary of Miner Information
miner_information_dict = {}

#global variable challenge 
challenge = init_challenge(miner_information_dict)

@node.route('/txion', methods=['POST'])
def transaction():
  # On each new POST request,
  # we extract the transaction data
  new_txion = request.get_json()
  # Then we add the transaction to our list
  this_nodes_transactions.append(new_txion)
  # Because the transaction was successfully
  # submitted, we log it to our console
  print "New transaction"
  print "FROM: {}".format(new_txion['from'].encode('ascii','replace'))
  print "TO: {}".format(new_txion['to'].encode('ascii','replace'))
  print "AMOUNT: {}\n".format(new_txion['amount'])
  # Then we let the client know it worked out
  return "Transaction submission successful\n"

# shaCha = hashlib.sha256()
# shaAns = hashlib.sha256()

# New Miner Method
@node.route('/mine', methods=['POST'])
def mine():
  informationMiner = request.get_json()
  miner_information_dict[informationMiner['miner_address']] = informationMiner
  #print "Miner " + str(informationMiner['miner_address']) + " now mining"
  answer = informationMiner['answer']
  print str(answer) + " received from miner : " + str(informationMiner['miner_address']) + ", Checking correctness"

  ############################################
  # Debugging
  #print miner_information_dict
  if(len(this_nodes_transactions) != 0 and answer == challenge):
    # First find the Challenge
    # Not really using the difficulty level here at all, but leaving it for 
    # debugging and future use! 
    global challenge
    [challenge, d_level] = refresh_challenge(miner_information_dict)
    print str(challenge) + " new challenge"

    # Give Blockchain Data
    last_block = blockchain[len(blockchain) - 1]

    # Not Doing Hashes for Demos since Mining takes too long
    # shaCha.update(challenge)
    # challenge = shaCha.hexdigest()
    # Once we find a valid proof of work,
    # we know we can mine a block so 
    # we reward the miner by adding a transaction
    this_nodes_transactions.append(
      { "from": "network", "to": informationMiner['miner_address'], "amount": 1 }
      )
    # Now we can gather the data needed
    # to create the new block
    new_block_data = {
      "transactions": list(this_nodes_transactions)
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
    return "\n" + json.dumps({
      "index": new_block_index,
      "timestamp": str(new_block_timestamp),
      "data": new_block_data,
      "hash": last_block_hash
    }) + "\n"
  else:
    #print "Spam Miner"
    return "Try Again"
  
  ############################################

# Get Challenge
@node.route('/info', methods=['POST'])
def get_info():
  informationMiner = request.get_json()
  miner_information_dict[informationMiner['miner_address']] = informationMiner
  return challenge

@node.route('/board', methods=['POST'])
def board():
  return json.dumps(miner_information_dict)
  

# Internal Blocks Method
@node.route('/blocks', methods=['GET'])
def get_blocks():
  chain_to_send = blockchain
  for i in range(len(chain_to_send)):
    block = chain_to_send[i]
    block_index = str(block.index)
    block_timestamp = str(block.timestamp)
    block_data = str(block.data)
    block_hash = block.hash
    assembled = json.dumps({
    "index": block_index,
    "timestamp": block_timestamp,
    "data": block_data,
    "hash": block_hash
    })
    if blocklist == "":
      blocklist = assembled
    else:
      blocklist =  blocklist + assembled
  return blocklist

#External Blocks Method
@node.route('/print_block', methods=['GET'])
def print_blocks():
  #print '\nLength ',len(this_nodes_transactions)
  chain_to_send = blockchain
  blocklist = ""
  for i in range(len(chain_to_send)):
    block = chain_to_send[i]
    block_index = str(block.index)
    block_timestamp = str(block.timestamp)
    block_data = str(block.data)
    block_hash = block.hash
    assembled = json.dumps({
    "index": block_index,
    "timestamp": block_timestamp,
    "data": block_data,
    "hash": block_hash}, sort_keys=False, indent=4)
    if blocklist == "":
      blocklist = assembled
    else:
      blocklist =  blocklist + assembled
  return blocklist

node.run()

