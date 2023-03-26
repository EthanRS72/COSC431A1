import time
import csv
import pickle
import sys
def binary_search(array, target, low, high):

    while low <= high:
        mid = low + (high - low)//2
        if array[mid] == target:
            return mid
        elif array[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

def search():
    with open("unique.bin", 'rb') as file:
        unique = pickle.load(file)

    with open("docnos.bin", 'rb') as file:
        docnos = pickle.load(file)

    with open("inverted_index.bin", 'rb') as file:
        inverted_index = pickle.load(file)

    rsv = [0] * len(unique)
    inputs = sys.stdin.read()
    inputs = inputs.lower().split()
    print(inputs)

    #print(len(unique))

    
    for i in range(len(inputs)):
        x = binary_search(unique, inputs[i], 0, len(unique)-1)
        lst = inverted_index[x]
        idx = 0
        for i in range(len(lst)):
            idx += lst[i]
            rsv[idx] += 1

    #print(rsv)

    results = zip(docnos, rsv)
    sorted_results = sorted(results, key = lambda x: x[1], reverse = True)
    
    print("<docno>          <rsv>")
    i = 0
    while sorted_results[i][1] > len(inputs) / 2:
        print(sorted_results[i][0], "|", sorted_results[i][1])
        i += 1
    

    

        
        


t1 = time.time()
search()
print("executed in:", time.time() - t1, "seconds")