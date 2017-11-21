import uuid
import time
import json
import urllib
import urllib2
from random import randint
import platform, subprocess, os

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

class Miner:
    def __init__(self,  miner_cpu, miner_gpu):
        #self.miner_address = uuid.uuid4()
        self.miner_address = randint(0,1000)
        self.miner_coins_earned = 0
        self.miner_cpu = miner_cpu
        self.miner_gpu = miner_gpu

miner = Miner(
    detectCPUs(),
    4 ** detectCPUs()
)

try:
    while True:
        req = urllib2.Request("http://localhost:5000/mine", json.dumps({ 'miner_address' : miner.miner_address, 'coins_earned' : miner.miner_coins_earned , 'miner_cpu' : miner.miner_cpu, 'miner_gpu' : miner.miner_gpu }), headers={'Content-type': 'application/json', 'Accept': 'application/json'})
        response = urllib2.urlopen(req)
        the_page = response.read()
        if(the_page != "Try Again"):
            print the_page
            miner.miner_coins_earned += 1
        else:
            print "Trying Again"
        time.sleep(1)
except KeyboardInterrupt:
    print('interrupted!')