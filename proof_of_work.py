# This is the main file for Coffee Coin Proof of Work and Proof of Stake that will create 
# a target hash to get to and modify the difficulty level (d(t)) according to the 
# Originally adapted from [https://gist.github.com/aunyks/47d157f8bc7d1829a729c2a6a919c173]
# Authored by Siddharth Kulkarni and Sharan Duggirala November 18th, 2017

import hashlib 
import random
import string
import json

difficulty_level = 1
known_cpu = 0
known_gpu = 0

# Function to Initialize the Challenge String
def init_challenge(peer_nodes):

	# There is not point if the Server has not detected any nodes as 
	# of now 
	if (len(peer_nodes) == 0):
		answer = ''.join(random.choice(string.ascii_lowercase +
									string.ascii_uppercase +
									string.digits) 
									for _ in range(4)) 
		return answer 
	
	tot_gpu = 0
	tot_cpu = 0
	# Need to initialize the Known CPU and GPU values to start with 
	for key in peer_nodes:
		tot_gpu += peer_nodes[key].miner_gpu
		tot_cpu += peer_nodes[key].miner_cpu
	if (tot_gpu + tot_cpu > known_gpu + known_cpu):
		known_gpu = tot_gpu
		known_cpu = tot_cpu

	answer = ''.join(random.choice(string.ascii_lowercase +
									string.ascii_uppercase +
									string.digits) 
									for _ in range(4))
	return answer


# Function to refresh the Challenge String
def refresh_challenge(peer_nodes): 

	# Need to Discover the Known CPU and GPU values to start with 
	diff_level(peer_nodes)

	challenge = ''

	# Add the Required Number of 0s from the Difficulty Level
#	for i in range(difficulty_level):
#		challenge+='0'

	# Generate the 16 byte string that will function as the target
	global difficulty_level
	# answer = ''.join(random.choice(string.ascii_lowercase +
	# 								string.ascii_uppercase +
	# 								string.digits) 
	# 								for _ in range(4-difficulty_level))
	answer = ''.join(random.choice(string.ascii_lowercase +
									string.ascii_uppercase +
									string.digits) 
									for _ in range(4))

	challenge+=answer
	global difficulty_level
	return challenge, difficulty_level


# Calculate the Total GPU  and CPU utilazation and change the value of 
# of the difficulty level
def diff_level(peer_nodes):

	# There is not point if the Server has not detected any nodes as 
	# of now 
	if (len(peer_nodes) == 0) : 
		return

	else:  
		tot_gpu = 0
		tot_cpu = 0
		# Need to Discover the new CPU and GPU values to start with 
		for key in peer_nodes:
			tot_gpu += peer_nodes[key]['miner_gpu']
			tot_cpu += peer_nodes[key]['miner_cpu']

		#In the case where the CPU and GPU has doubled 
		if (tot_gpu + tot_cpu > 2*(known_gpu + known_cpu)):
			global known_gpu
			global known_cpu
			global difficulty_level
			difficulty_level+=1
			known_gpu = tot_gpu
			known_cpu = tot_cpu

		# In the case where CPU and GPU have halved
		if (tot_gpu + tot_cpu < 2*(known_gpu + known_cpu)):
			global difficulty_level
			difficulty_level-=1
			known_gpu = tot_gpu
			known_cpu = tot_cpu

		# If neither of these cases are true, just stay as is

