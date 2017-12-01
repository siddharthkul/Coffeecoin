#import coffeecoin_multiminer
import os, sys
from random import randint
import multiprocessing

def spawn(num, j):
    t = randint(1,4)
    print('spawning miner '+str(num)+" with "+str(t)+" threads")
    os.system("python coffeecoin-multiminer.py "+str(t))


j = multiprocessing.Value('i', 0)
for i in range(int(sys.argv[1])):
    p = multiprocessing.Process(target=spawn, args=(i,j))
    p.start()