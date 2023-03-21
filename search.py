import time
import csv

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
    with open("index.csv") as f:
        reader = csv.reader(f)
        index = list(reader)

    lst = []
    for i in range(100000):
        lst.append(i)
    
    #idx = binary_search(lst, 57, 0, len(lst)-1)
    print(len(max(index, key=len))-1)
    print(max(index, key=len)[0])

        


t1 = time.time()
search()
print("executed in:", time.time() - t1, "seconds")