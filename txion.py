# This file is responsible for containing the 
# a target hash to get to and modify the difficulty level (d(t)) according to the 
# Authored by Siddharth Kulkarni and Sharan Duggirala November 18th, 2017

import random
import urllib2

miner_data = []
step = 0.001
known_number
prev_i

# Needed for Sorting the events in the deck
class Card: 
	def __init__(self, miner_hash, prob):
		self.miner_hash = miner_hash
		self.prob = prob

# Need an Ask Method in the server Program that sends back data to this [o it's a [get]

# Gets back the Miner Data
@node.route('/miner_data', methods=['POST'])
def get_data(): 
	miner_data = request.get_json()
	prob_model(miner_data)
	try:
	    req = urllib2.Request(“http://localhost:5000/mine2“, json.dumps({‘address’ : miner.miner_address}), headers={‘Content-type’: ‘application/json’, ‘Accept’: ‘application/json’})
	    response = urllib2.urlopen(req)
	    the_page = response.read()
	    print the_page
	    time.sleep(1)
	except KeyboardInterrupt:
    	print(‘interrupted!’)


# Sorts and chooses two miners randomly from the deck 
def deck_chooser():



# Work out the Probabilistic Model for Transactions
def prob_model(miner_data): 

	# Case 1: This Function is being initialized as of now 
	if known_number == None :
		# Simple Dithering Algorithm
		total_coins = 0
		deck = []
		# First Calculate the Total Number of Coins Calculated
		for i in range(len(miner_data)):
			total_coins += miner_data[i].miner_coins_earned
		# Gather the Probabilities of each Node Transacting
		for i in range(len(miner_data))
			deck[i] = Card(miner.miner_address, miner_data[i].miner_coins_earned/total_coins)
		# When the event has already happened, we need to decrease the probability
		# of it happening once more (Bayesian Model)
		known_number = len(miner_data)
		# Call the function to sort the deck and choose two events (prev_i is set here)
		deck_chooser(deck)

	# Case 2 The function has already been intialized
	else: 
		# Case 2 A The function has been intialized before but there has not been a 
		if (len(miner_data) == known_number):
			if prev_i != None :
				deck[prev_i].prob -= step
			# Call the function to sort the deck and choose the two events (prev_i is set here)
		else: 
			# Simple Dithering Algorithm
			total_coins = 0
			deck = []
			# First Calculate the Total Number of Coins Calculated
			for i in range(len(miner_data)):
				total_coins += miner_data[i].miner_coins_earned
			# Gather the Probabilities of each Node Transacting
			for i in range(len(miner_data))
				deck[i] = Card(miner.miner_address, miner_data[i].miner_coins_earned/total_coins)
			# When the event has already happened, we need to decrease the probability
			# of it happening once more (Bayesian Model)
			known_number = len(miner_data)
			# Call the function to sort the deck and choose two events (prev_i is set here)
			deck_chooser(deck)