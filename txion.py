# This file is responsible for containing the 
# a target hash to get to and modify the difficulty level (d(t)) according to the 
# Authored by Siddharth Kulkarni and Sharan Duggirala November 18th, 2017

# Imports
import random
import string

# Ignore all Warnings for demo (Please comment out otherwise)
import warnings
warnings.filterwarnings("ignore")

# List of Transactors in the network
transactor_data = []
# The Step reduction for the dithering Algorithm
step = 0.001
# For Dithering we need to remember the last event that happened
prev_address = 0
# Intialization Variable to know whether or not transactors have been initialized
init = False

# Needed for Sorting the events in the deck
class Card: 
	def __init__(self, miner_hash, prob):
		self.miner_hash = miner_hash
		self.prob = prob

# Need an Ask Method in the server Program that sends back data to this [o it's a [get]

#################

# Get the for the transactions
def get_transactions(): 
	# Figure out the next candidates given the Probabilistic Model
	[address1, address2] = prob_model()
	# Make a random amount of money for the transaction
	transaction_amount = random.randint(1,101)
	# Take the money from the sender and give it to the reciever
	for i in range(len(transactor_data)):
		# Cannot have negative coins or it's going to mess up the probabilistic model 
		if transactor_data[i].miner_address == address1:
			if transaction_amount >= transactor_data[i].coins:
				transactor_data[i].coins = 0
			else: 
				transactor_data[i].coins -= transaction_amount
		if transactor_data[i].miner_address == address2:
			transactor_data[i].coins += transaction_amount
	# Now we can return the information that the server needs for transactions
	return [address1, address2, transaction_amount]

#################

class Sample_transactor_data:
	def __init__(self, miner_address, coins):
		self.miner_address = miner_address
		self.coins = coins

# Create a random list of transactors and give them money and adresses
def create_transactors(i): 
	transactor_data = []
	for x in range(i): 
		# First Determine the Miner Address
		m_address = random.randint(1,9999)
		# Next, each transactor gets a random number of coins
		s_coins = random.randint(1,101)
		new_obj = Sample_transactor_data(m_address,s_coins)
		transactor_data.append(new_obj)
	return transactor_data

#################

# Sorts and chooses two miners randomly from the deck 
def deck_chooser(deck):
	# First sort the deck based on the Probabilities
	deck.sort(key = lambda x: x.prob, reverse = True)
	# Split into three different segments and shuffle them
	list1 = deck[:len(deck)/3]
	list1 = random.sample(list1,len(list1))
	list2 = deck[len(deck)/3:2*(len(deck))]
	list2 = random.sample(list2,len(list2))
	list3 = deck[2*len(deck):]
	list3 = random.sample(list3,len(list3))
	# Concat them back into one list
	deck[:] = []
	deck.extend(list1)
	deck.extend(list2)
	deck.extend(list3)
	prev_address = deck[0].miner_hash
	return [deck[0].miner_hash, deck[1].miner_hash]

#################

# Work out the Probabilistic Model for Transactions
def prob_model(): 

	# Case 1: This Function is being initialized as of now 
	global init
	if init == False: 
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
			deck.append(Card(transactor_data[i].miner_address, 
								transactor_data[i].coins/total_coins))
		# Set init to true from this point on 
		global init
		init = True
		# Call the function to sort the deck and choose two events (prev_i is set here)
		return deck_chooser(deck)

	# Case 2 The transactors have already been intialized
	else: 
		# Simple Dithering Algorithm
		total_coins = 0
		deck = []
		# First Calculate the Total Number of Coins Calculated
		global transactor_data
		for i in range(len(transactor_data)):
			total_coins += transactor_data[i].coins
		# Gather the Probabilities of each Node Transacting
		for i in range(len(transactor_data)):
			deck.append(Card(transactor_data[i].miner_address, 
								transactor_data[i].coins/total_coins))
		# It is important that we remove a particular amount of probability from 
		# the previous transaction
		for i in range (len(deck)): 
			global prev_address
			if (prev_address): 
				if deck[i].miner_hash == prev_address:
					deck[i].prob -= step
		# Call the function to sort the deck and choose two events (prev_i is set here)
		return deck_chooser(deck)

#################