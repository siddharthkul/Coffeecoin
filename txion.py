# This file is responsible for containing the 
# a target hash to get to and modify the difficulty level (d(t)) according to the 
# Authored by Siddharth Kulkarni and Sharan Duggirala November 18th, 2017

import random
import urllib2

# List of Transactors in the network
transactor_data = []
# The Step reduction for the dithering Algorithm
step = 0.001
# For Dithering we need to remember the last event that happened
prev_address

# Needed for Sorting the events in the deck
class Card: 
	def __init__(self, miner_hash, prob):
		self.miner_hash = miner_hash
		self.prob = prob

# Need an Ask Method in the server Program that sends back data to this [o it's a [get]

#################

# Gets back the Miner Data
@node.route('/init_txion', methods=['POST'])
def get_data(): 
	# Figure out the next candidates given the Probabilistic Model
	[address1, address2] = prob_model()
	# Make a random amount of money for the transaction
	transaction_amount = random.randint(1,101)
	# Take the money from the sender and give it to the reciever
	for i in range(len(transactor_data)):
		# Cannot have negative coins or it's going to mess up the probabilistic model 
		if deck[i].miner_address = address1:
			if transaction_amount >= deck[i].coins:
				deck[i].coins = 0
			else: 
				deck[i].coins -= transaction_amount
		if deck[i].miner_address = address2:
			deck[i].coins += transaction_amount
	# Now we can send the transaction CURL request to the server
	try:
	    req = urllib2.Request(“http://localhost:5000/mine2“, 
	    						json.dumps(headers={‘Content-type’: ‘application/json’, 
	    										"from": address1, "to": address2,
	    										"amount": transaction_amount}))
	    response = urllib2.urlopen(req)
	    the_page = response.read()
	    print the_page
	except KeyboardInterrupt:
    	print("Transaction has been manually interrupted!")

#################

# Create a random list of transactors and give them money and adresses
def create_transactors(i): 
	transactor_data = []
	for x in the range(i): 
		# First determine a random miner address
		transactor_data[x].miner_address = ''.join(random.choice(string.ascii_lowercase +
												string.ascii_uppercase +
												string.digits) 
												for _ in range(4))
		# Next, each transactor gets a random number of coins
		transactor_data[x].coins = random.randint(1,101)
	return transactor_data

#################

# Sorts and chooses two miners randomly from the deck 
def deck_chooser(deck):
	# First sort the deck based on the Probabilities
	deck.sort(key = lambda x: x.prob, reverse = True)
	# Split into three different segments and shuffle them
	list1 = random.shuffle(deck[:len(deck)/3])
	list2 = random.shuffle(deck[len(deck)/3:2*(len(deck))])
	list3 = random.shuffle(deck[2*len(deck):])
	# Concat them back into one list
	deck = list1+ list2 + list3
	return [deck[0].miner_address, deck[1].miner_address]

#################

# Work out the Probabilistic Model for Transactions
def prob_model(): 

	# Case 1: This Function is being initialized as of now 
	if not transactors_data :
		global transactors_data
		transactor_data = create_transactors(100)
		# Start Calculating the Probabilities of the Events
		total_coins = 0
		deck = []
		# First Calculate the Total Number of Coins Calculated
		for i in range(len(transactor_data)):
			total_coins += transactor_data[i].coins
		# Gather the Probabilities of each Node Transacting
		for i in range(len(transactor_data)):
			deck[i] = Card(transactor_data.miner_address, miner_data[i].coins/total_coins)
		# Call the function to sort the deck and choose two events (prev_i is set here)
		return deck_chooser(deck)

	# Case 2 The transactors have already been intialized
	else: 
		# Simple Dithering Algorithm
		total_coins = 0
		deck = []
		# First Calculate the Total Number of Coins Calculated
		for i in range(len(transactor_data)):
			total_coins += transactor_data[i].coins
		# Gather the Probabilities of each Node Transacting
		for i in range(len(transactor_data)):
			deck[i] = Card(transactor_data.miner_address, miner_data[i].coins/total_coins)
		# It is important that we remove a particular amount of probability from 
		# the previous transaction
		global prev_address
		for i in range (len(deck)): 
			if deck[i].miner_hash == prev_address
				deck[i].prob -= step
		# Call the function to sort the deck and choose two events (prev_i is set here)
		return deck_chooser(deck)

#################