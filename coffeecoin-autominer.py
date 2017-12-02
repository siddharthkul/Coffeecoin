#import coffeecoin_multiminer
import os, sys
from random import randint
import multiprocessing

args_passed = False

if(len(sys.argv)-2 == 0):
    print("No args passed")
    args_passed = True

if(args_passed):
    sys.exit([arg])

def spawn(num, j):
    t = randint(1,4)
    print('spawning miner '+str(num)+" with "+str(t)+" threads")
    os.system("python coffeecoin-multiminer.py "+str(t)+" "+str(sys.argv[2]))


j = multiprocessing.Value('i', 0)
for i in range(int(sys.argv[1])):
    p = multiprocessing.Process(target=spawn, args=(i,j))
    p.start()