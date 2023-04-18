#Ethan Smith - COSC431 Assignment 1 2023
import time
import pickle
import sys
import linecache
import math

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


#------------------------------------------------------------------#
#Run with query in .txt file like: cat query.txt | python search.py
#------------------------------------------------------------------# 


def search():
    #open reference files
    with open("unique.bin", 'rb') as file:
        unique = pickle.load(file)

    with open("docnos.bin", 'rb') as file:
        docnos = pickle.load(file)

    with open("doclens.bin", 'rb') as file:
        doclens = pickle.load(file)

    #instantiate retrival score value table and read search query
    rsv = [0] * len(docnos)
    inputs = sys.stdin.read()
    inputs = inputs.lower().split()

    #for every term in query, find if it exists
    for i in range(len(inputs)):
        x = binary_search(unique, inputs[i])
        #if search term exists load term from index and format into a nested list
        if x != -1:
            line = linecache.getline("index.txt", x+1).replace(",", "").replace("[", "").replace("]", "").split()
            token_index = []
            for i in range(len(line)):
                if i % 2 == 1:
                    token_index.append([int(line[i-1]), int(line[i])])

            #for each document containing the current term caluclate a tf-idf score for that term/document pair
            docidx = 0
            #idf will be the same for every document from a given term so only calculate once
            idf = math.log(len(doclens) / (len(token_index)))
            for i in range(len(token_index)):
                docidx += token_index[i][0]
                tf = token_index[i][1] / doclens[docidx]
                rsv[docidx] += (tf * idf)

    #attach scores to documents and sort
    results = zip(docnos, rsv)
    sorted_results = sorted(results, key = lambda x: x[1], reverse = True)

    #output
    sys.stdout.write("<docno>          <rsv>\n")
    i = 0
    while sorted_results[i][1] >= 0.2:
        line = str(sorted_results[i][0]) + "   " + "{:.3f}".format(sorted_results[i][1])
        sys.stdout.write(line+ "\n")
        i += 1

def main():
    t1 = time.time()
    search()
    runtime = "executed in: {:.2f} seconds".format(time.time() - t1)
    sys.stdout.write(runtime+"\n")

main()