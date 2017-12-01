# This is the main file for Coffee Coin Experimentation
# Authored by Siddharth Kulkarni and Sharan Duggirala November 18th, 2017

# Imports
from flask import Flask
from flask import request
import json
node = Flask(__name__)
from Block import *
from coffee_functions import *
from txion import *
from proof_of_work import * 
import random
import hashlib
from datetime import datetime
from math import pow

# Ignore all Warnings for demo (Please comment out otherwise)
import warnings
warnings.filterwarnings("ignore")

# This node's blockchain copy
blockchain = []
blockchain.append(create_genesis_block())

# Store the mined transactions in a list on the server 
this_nodes_transactions = []

# Dictionary of Miner Information
miner_information_dict = {}

# Global variable challenge initialization
challenge = init_challenge(miner_information_dict)

# To Calculate the Energy Efficiency Timing is essential
startTime= datetime.now()
timeElapsed = 0

# Global Initializations to calculate the energy efficiency
# Please change according to the country and situation
rewardPerMine = 1
# This is the electricity cost in San Jose State currently
electricityCost = 0.189
# For the purpose of our experiment and demo efficiency, we
# have set the d_f to 1
difficultyLevel  = 1
# The average power consumption of a laptop is around 12W
powerConsumption = 0.012
# The exchange price of a coffeecoin is 1 Dollar
exchangeRate = 1

#############################################################################################################

def end_sequence():

  for key in miner_information_dict:
    # Need to calculate the Hash Rate First
    global timeElapsed
    coins_earned = miner_information_dict[key]['coins_earned']
    hashrate = (pow(2,32)*coins_earned)/(timeElapsed.total_seconds())
    miner_information_dict[key]['hashrate'] = hashrate

    #Calculate the Left side of the Power Efficiency
    global powerConsumption
    leftEquation = hashrate/powerConsumption
    miner_information_dict[key]['efficiency'] =leftEquation

    # Calculate the Right side of the Power Efficiency
    global rewardPerMine
    global electricityCost
    global difficultyLevel
    global exchangeRate
    rightEquation = (electricityCost*
          difficultyLevel)/(rewardPerMine*exchangeRate)

    # Determine if the System is Profitable
    if leftEquation > rightEquation:
      miner_information_dict[key]['profitability'] = 1

  print miner_information_dict

#############################################################################################################

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

#############################################################################################################

# New Miner Method
@node.route('/mine', methods=['POST'])
def mine():
  # Get the miner information including the answer
  informationMiner = request.get_json()
  miner_information_dict[informationMiner['miner_address']] = informationMiner
  answer = informationMiner['answer']

  # Get a random number, upto 10, transactions filled out from the transaction server 
  for _ in range(random.randint(2,11)):
    [new_sender, new_reciever, amount] = get_transactions()
    this_nodes_transactions.append(
      { "from": new_sender, "to": new_reciever, "amount": amount}
    )

  print "NEW TRANSACTIONS :"
  print this_nodes_transactions

  # Check if the Challenge and Answer are truly equal 
  if(len(this_nodes_transactions) != 0 and answer == challenge):

    # Create a new global challenge, since challenge has already been solved
    global challenge
    [challenge, d_level] = refresh_challenge(miner_information_dict)
    print str(challenge) + " new challenge"

    # Add the transaction where this server has given a coin to the miner
    this_nodes_transactions.append(
      { "from": "network", "to": informationMiner['miner_address'], "amount": 1 }
    )

    # Now we can gather the data needed to create the new block
    last_block = blockchain[len(blockchain) - 1]
    new_block_data = {
      "transactions": list(this_nodes_transactions)
    }
    new_block_index = last_block.index + 1
    new_block_timestamp = this_timestamp = date.datetime.now()
    last_block_hash = last_block.hash

    # Empty transaction list and create a new block
    this_nodes_transactions[:] = []
    mined_block = Block( new_block_index, new_block_timestamp, new_block_data,
                          last_block_hash)
    blockchain.append(mined_block)

    # Let the client know we mined a block
    return "\n" + json.dumps({
      "index": new_block_index,
      "timestamp": str(new_block_timestamp),
      "data": new_block_data,
      "hash": last_block_hash
    }) + "\n"

  # In the case where there is nothing to mine (no transactions)
  # Note: As of now, this part of the condition should never be invoked
  else:
    #print "Spam Miner"
    return "Try Again"
  
#############################################################################################################

# Get Challenge
@node.route('/info', methods=['POST'])
def get_info():
  informationMiner = request.get_json()
  miner_information_dict[informationMiner['miner_address']] = informationMiner
  return challenge

@node.route('/board', methods=['POST'])
def board():
  return json.dumps(miner_information_dict)
  
#############################################################################################################

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

#############################################################################################################

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

# Start server
node.run(threaded=True, host='0.0.0.0')

