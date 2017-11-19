# This is the main file for Coffee Coin Proof of Work and Proof of Stake that will create 
# a target hash to get to and modify the difficulty level (d(t)) according to the 
# Originally adapted from [https://gist.github.com/aunyks/47d157f8bc7d1829a729c2a6a919c173]
# Authored by Siddharth Kulkarni and Sharan Duggirala November 18th, 2017

import hashlib 
import random
import string

difficulty_level = 1
known_cpu = 0
known_gpu = 0

# Function to Initialize the Challenge String
def init_challenge(peer_nodes):
	
	# Need to initialize the Known CPU and GPU values to start with 
	for i in range(len(peer_nodes)):
		tot_gpu += peer_nodes[i].miner_gpu
		tot_cpu += peer_nodes[i].miner_cpu
	if (tot_gpu + tot_cpu > known_gpu + known_cpu):
		known_gpu = tot_gpu
		known_cpu = tot_cpu

	challenge = '0'

	# Generate the 16 byte string that will function as the target
	answer = ''.join(random.choice(string.ascii_lowercase +
									string.ascii_uppercase +
									string.digits) for x in range(15))

	return challenge+=answer, difficulty_level

# Function to refresh the Challenge String
def refresh_challenge(peer_nodes): 

	# Need to Discover the Known CPU and GPU values to start with 
	diff_level(peer_nodes)

	challenge = ''

	# Add the Required Number of 0s from the Difficulty Level
	for i in range(difficulty_level):
		challenge+='0'

	# Generate the 16 byte string that will function as the target
	answer = ''.join(random.choice(string.ascii_lowercase +
									string.ascii_uppercase +
									string.digits) 
									for x in range(16-difficulty_level))

	return challenge+=answer, difficulty_level


# Calculate the Total GPU  and CPU utilazation and double every time
def diff_level(peer_nodes):

	# Need to Discover the new CPU and GPU values to start with 
	for i in range(len(peer_nodes)):
		tot_gpu += peer_nodes[i].miner_gpu
		tot_cpu += peer_nodes[i].miner_cpu

	#In the case where the CPU and GPU has doubled 
	if (tot_gpu + tot_cpu > 2*(known_gpu + known_cpu):
		difficulty_level++
		known_gpu = tot_gpu
		known_cpu = tot_cpu

	# In the case where CPU and GPU have halved
	else if (tot_gpu + tot_cpu < 2*(known_gpu + known_cpu)
		difficulty_level--
		known_gpu = tot_gpu
		known_cpu = tot_cpu

	# If neither of these cases are true, just stay as is


