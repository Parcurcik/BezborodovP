from multiprocessing import Pool
from time import *


start_time = time()

def func(a):
    return 2**20


if __name__ == "__main__":
    with Pool(7) as p:
        print(p.map(func, [2, 3, 4]))

print(time() - start_time)