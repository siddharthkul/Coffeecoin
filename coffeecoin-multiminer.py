import multiprocessing
import string
import uuid
import time
import json
import urllib
import urllib2
from random import randint
import platform, subprocess, os
import random, hashlib, string

# Function to Detect CPU
def detectCPUs():
 """
 Detects the number of CPUs on a system.
 """
 # Linux, Unix and MacOS:
 if hasattr(os, "sysconf"):
     if os.sysconf_names.has_key("SC_NPROCESSORS_ONLN"):
         # Linux & Unix:
         ncpus = os.sysconf("SC_NPROCESSORS_ONLN")
         if isinstance(ncpus, int) and ncpus > 0:
             return ncpus
     else: # OSX:
         return int(os.popen2("sysctl -n hw.ncpu")[1].read())
 # Windows:
 if os.environ.has_key("NUMBER_OF_PROCESSORS"):
         ncpus = int(os.environ["NUMBER_OF_PROCESSORS"]);
         if ncpus > 0:
             return ncpus
 return 1 # Default

# Define Class
class Miner:
    def __init__(self,  miner_cpu, miner_gpu):
        #self.miner_address = uuid.uuid4()
        self.miner_address = randint(0,1000)
        #self.miner_address = miner_name
        self.miner_coins_earned = 0
        self.miner_cpu = miner_cpu
        self.miner_gpu = miner_gpu

# Miner Class Constructor
miner = Miner(
    #name,
    detectCPUs(),
    4 ** detectCPUs()
)

def spawn(num, v):
    # print("received " + str(v.value))
    # v.value+=1
    # print(miner.miner_coins_earned)

    #get Challenge
    req = urllib2.Request("http://localhost:5000/info", json.dumps({ 'miner_address' : miner.miner_address, 'coins_earned' : v.value , 'miner_cpu' : miner.miner_cpu, 'miner_gpu' : miner.miner_gpu}), headers={'Content-type': 'application/json', 'Accept': 'application/json'})
    response = urllib2.urlopen(req)
    challenge = response.read()
    #print challenge

    #solve Challenge
    #Now we can attempt to find the solution
    ping_index = 0
    found = False
    while found == False : 
       #print("finding")
        ping_index += 1
        answer = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits)for _ in range(4))
        if ping_index == 1000000 :
            #print("updating")
            ping_index = 0
            req2 = urllib2.Request("http://localhost:5000/info", json.dumps({ 'miner_address' : miner.miner_address, 'coins_earned' : v.value , 'miner_cpu' : miner.miner_cpu, 'miner_gpu' : miner.miner_gpu}), headers={'Content-type': 'application/json', 'Accept': 'application/json'})
            response2 = urllib2.urlopen(req2)
            challenge = response2.read()
            #print challenge
        if answer == challenge : 
            print("Found")
            my_answer = answer
            found = True
            #print str(miner.miner_address) + " has mined a coin"
    req3 = urllib2.Request("http://localhost:5000/mine", json.dumps({ 'miner_address' : miner.miner_address, 'coins_earned' : v.value , 'miner_cpu' : miner.miner_cpu, 'miner_gpu' : miner.miner_gpu , 'answer' : my_answer}), headers={'Content-type': 'application/json', 'Accept': 'application/json'})
    response3 = urllib2.urlopen(req3)
    the_page3 = response3.read()
    if(the_page3 != "Try Again"):
        print the_page3
        v.value+=1
        #miner.miner_coins_earned += 1
        #print("Coins earned " + str(miner.miner_coins_earned))
    else:
        print "Trying Again"

if __name__ == '__main__':
    v = multiprocessing.Value('i', 0)
    for i in range(8):
        p = multiprocessing.Process(target=spawn, args=(i,v))
        p.start()
        #p.join() #- one after the other, but we want parallel
