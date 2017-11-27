import uuid
import time
import json
import urllib
import urllib2
from random import randint
import platform, subprocess, os
import random, hashlib, string

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

def solveHash(challenge):
    # Now we can attempt to find the solution
    ping_index = 0
    found = False
    while found == False : 
        ping_index += 1
        answer = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits)for _ in range(4))
        if ping_index == 1000000 :
            ping_index = 0
            req2 = urllib2.Request("http://10.0.0.70:5000/info", json.dumps({ 'miner_address' : miner.miner_address, 'coins_earned' : miner.miner_coins_earned , 'miner_cpu' : miner.miner_cpu, 'miner_gpu' : miner.miner_gpu}), headers={'Content-type': 'application/json', 'Accept': 'application/json'})
            response2 = urllib2.urlopen(req2)
            challenge = response2.read()
            print challenge
        if answer == challenge : 
            found = True
            #print str(miner.miner_address) + " has mined a coin"
            return answer
            

class Miner:
    def __init__(self, miner_name,  miner_cpu, miner_gpu):
        #self.miner_address = uuid.uuid4()
        #self.miner_address = randint(0,1000)
        self.miner_address = miner_name
        self.miner_coins_earned = 0
        self.miner_cpu = miner_cpu
        self.miner_gpu = miner_gpu

name_case = False
while(name_case == False):
    name = raw_input('\nPlease input miner name(length more than 8 and less than 11) - ')
    if(len(name)>10):
        print('Length should be less than 11')
    if(len(name)<8):
        print('Length should be more than 8')
    if(len(name)>7 and len(name)<11):
        name_case = True

print(name)

miner = Miner(
    name,
    detectCPUs(),
    4 ** detectCPUs()
)

try:
    while True:
        req = urllib2.Request("http://10.0.0.70:5000/info", json.dumps({ 'miner_address' : miner.miner_address, 'coins_earned' : miner.miner_coins_earned , 'miner_cpu' : miner.miner_cpu, 'miner_gpu' : miner.miner_gpu}), headers={'Content-type': 'application/json', 'Accept': 'application/json'})
        response = urllib2.urlopen(req)
        challenge = response.read()
        print challenge
        my_answer = solveHash(challenge)
        req3 = urllib2.Request("http://10.0.0.70:5000/mine", json.dumps({ 'miner_address' : miner.miner_address, 'coins_earned' : miner.miner_coins_earned , 'miner_cpu' : miner.miner_cpu, 'miner_gpu' : miner.miner_gpu , 'answer' : my_answer}), headers={'Content-type': 'application/json', 'Accept': 'application/json'})
        response3 = urllib2.urlopen(req3)
        the_page3 = response3.read()
        if(the_page3 != "Try Again"):
            print the_page3
            miner.miner_coins_earned += 1
        else:
            print "Trying Again"
        
except KeyboardInterrupt:
    print('interrupted!')
