#Ethan Smith - COSC431 Assignment 1 2023
import time
import pickle
from parse import parse_tokens
import sys

def binary_search(list, target):
    low = 0
    high = len(list)-1
    while low <= high:
        mid = low + (high - low)//2
        if list[mid] == target:
            return mid
        elif list[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

def binary_search_nested_list(nested_list, key, value, low, high):
    while low <= high:
        mid = (low + high) // 2
        if nested_list[mid][key] == value:
            return mid
        elif nested_list[mid][key] > value:
            high = mid - 1
        else:
            low = mid + 1

    return -1

def build_inverted_index():
    t1 = time.time()
    inverted_index = []
    doclens = []
    unique = []
    #get tokens and docnumbers from parse_tokens
    doc_text, docnos = parse_tokens()

    #from the tokens find every unique term and sort them
    #sets uses a hash function to store elements so checking if a new term is found is
    #an O(1) operation - this is the most crucial part to building this index in a useable timeframe
    sys.stdout.write("parsing complete, finding unique\n")
    t2 = time.time()
    unique = set()
    for doc in doc_text:
        for i in range(1, len(doc)):
            unique.add(doc[i])
    unique = sorted(list(unique))
    unitime = "Found unique in: {:.2f} minutes".format((time.time()-t2) / 60)
    sys.stdout.write(unitime+"\n")

    sys.stdout.write("sorting unique\n")
    unique = sorted(unique)

    #making dictionary allows for instant retrevial of unique term index
    unique_dict = {val: i for i , val in enumerate(unique)}

    #build inverted index from here on, start by establishing a nested list for every unique term found
    sys.stdout.write("Building index\n")
    t3 = time.time()
    for i in range(len(unique)):
        temp = [unique[i]]
        inverted_index.append(temp)

    #build full index storing document numbers and document term frequencies
    for i in range(len(doc_text)):
        doclens.append(len(doc_text[i]))
        for x in range(len(doc_text[i])):
            #use a dictionary to avoid searching for correct sublist location
            #instant retrevial of index
            unidx = unique_dict[doc_text[i][x]]
            #check if document has not been added to sublist for the current term
            if binary_search_nested_list(inverted_index[unidx], 0, i, 1, len(inverted_index[unidx])-1) == -1 or len(inverted_index[unidx]) == 1:
                #if a new document-term pairing is being added add a sublist of the document index and the 
                #term frequency within that document
                count = doc_text[i].count(doc_text[i][x])
                temp = [i, count]
                inverted_index[unidx].append(temp)

    #change document indexes to diff runs
    tc = time.time()
    for i in range(len(inverted_index)):
        if len(inverted_index[i]) > 2:
            diff = []
            for x in range(2,len(inverted_index[i])):
                diff.append(inverted_index[i][x][0] - inverted_index[i][x-1][0])
            for x in range(2,len(inverted_index[i])):
                inverted_index[i][x][0] = diff[x-2]

    #remove terms from index to reduce size
    #file of just words will be searched instead to avoid loading whole index
    inverted_index = [sublist[1:] for sublist in inverted_index] 

    difftime = "Difference change in: {:.2f} minutes".format((time.time()-tc) / 60)
    idxtime = "Built index in: {:.2f} minutes".format((time.time()-t3) / 60)
    sys.stdout.write(difftime+"\n")
    sys.stdout.write(idxtime+"\n")

    #write files required for searching
    sys.stdout.write("writing inverted index to file\n")
    with open('unique.bin', mode='wb') as file:
        pickle.dump(unique, file)

    with open('docnos.bin', mode='wb') as file:
        pickle.dump(docnos, file)

    with open('doclens.bin', mode='wb') as file:
        pickle.dump(doclens, file)

    with open('index.txt', 'w') as file:
        for i in range(len(inverted_index)):
            line = ' '.join([str(elem) for elem in inverted_index[i]])
            file.write(line + '\n')

t1 = time.time()
build_inverted_index()
tottime = "Executed in {:.2f} minutes".format((time.time()-t1)/60)
sys.stdout.write(tottime+"\n")
