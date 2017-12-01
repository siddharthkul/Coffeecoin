#import coffeecoin_multiminer
import os, sys
import multiprocessing

def spawn(num, j):
    print('spawning miner '+str(num))
    os.system("python coffeecoin-multiminer.py 4")


j = multiprocessing.Value('i', 0)
for i in range(int(sys.argv[1])):
    p = multiprocessing.Process(target=spawn, args=(i,j))
    p.start()