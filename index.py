import time
import csv
import pickle
from parse import parse_tokens

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



def build_inverted_index():
    t1 = time.time()
    inverted_index = []
    next = []
    unique = []
    doc_text , docnos = parse_tokens()

    print("parsing complete, finding unique")
    t2 = time.time()
    unique = set()
    for doc in doc_text:
        for i in range(1, len(doc)):
            unique.add(doc[i])
    unique = sorted(list(unique))
    print("found unique in ", (time.time()-t2) / 60, " minutes")

    print("sorting unique")
    unique = sorted(unique)

    print("Building index")
    t3 = time.time()
    for i in range(len(unique)):
        temp = []
        temp.append(unique[i])
        inverted_index.append(temp)

    for i in range(len(doc_text)):
        for x in range(1,len(doc_text[i])):
            idx = binary_search(unique, doc_text[i][x], 0, len(unique)-1)
            if i != inverted_index[idx][-1]:
                inverted_index[idx].append(i)

    tc = time.time()
    for i in range(len(inverted_index)):
        temp = []
        if len(inverted_index[i]) > 2:
            for x in range(2,len(inverted_index[i])):
                temp.append(inverted_index[i][x] - inverted_index[i][x-1])
            inverted_index[i][2:] = temp

    #remove word from index
    inverted_index = [sublist[1:] for sublist in inverted_index]

    dictionary = {}
    for token in inverted_index:
        key = token[0]
        value = token[1:]
        dictionary[key] = value

    #for key in dictionary:
        #print(key, " : ", dictionary[key])

    print("difference change in ", (time.time()-tc) / 60, " minutes")
    print("built index in ", (time.time()-t3) / 60, " minutes")

    
    print("writing inverted index to file")
    with open('index.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(inverted_index)

    #read .bin with pickle.load
    with open('inverted_index.bin', mode='wb') as file:
        pickle.dump(inverted_index, file)
        

    #with open('unique.txt', mode='w') as file:
        #for word in unique:
            #file.write(word+"\n")

    with open('unique.bin', mode='wb') as file:
        pickle.dump(unique, file)

    with open('docnos.bin', mode='wb') as file:
        pickle.dump(docnos, file)

t1 = time.time()
build_inverted_index()
print("executed in: " ,(time.time()-t1) / 60, " minutes")