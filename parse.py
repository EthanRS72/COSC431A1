import time
import csv
import pickle

def parse_tokens():
    tp = time.time()
    remove = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", ":", ";", "'", ",", ".", "?", '"',"`", "-", "_", "+", "=", "[", "]", "{", "}", "|", "0", "1", "2", "3", "4", "5", "6","7","8", "9"]
    docnos = []
    doc_text = [] 
    file = open('wsj.xml', 'r')
    words = file.read().lower()
    words = words.replace("<", " <")
    words = words.replace(".", " .")
    words = words.replace(",", " ,")
    words = words.split()

    for i in range(len(words)):
        if words[i] == "<docno>":
            docnos.append(words[i+1])
    #print(docnos)

    words = ' '.join(words)
    for i in range(len(remove)):
            if remove[i] == "-":
                words = words.replace(remove[i], " ")
            else:
                words = words.replace(remove[i], "")
    words = ' '.join(words.split())
    words = words.split()

    txt = ""
    for i in range(len(words)):
        if words[i] != "<doc>":
            if words[i][0] != "<":
                txt = txt + " " + words[i]
        else:
            if txt != "":
                doc_text.append(txt)
            txt = ""
        if i == len(words)-1:
            txt = txt + " " + words[i]
            doc_text.append(txt)
    
    for i in range(len(doc_text)):
        doc_text[i] = str(doc_text[i]).split()
        temp = []
        for x in range(len(doc_text[i])):
            if doc_text[i][x].isalpha():
                temp.append(doc_text[i][x])
                #print(doc_text[i][x])
        doc_text[i] = temp
        #print("\n")
            
        

    with open('docnos.txt', mode='w') as file:
        for docid in docnos:
            file.write(docid+"\n")
        

    print("parsed tokens in: ", (time.time() - tp) / 60, " minutes")
    return doc_text

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
    inverted_index = []
    next = []
    unique = []
    doc_text = parse_tokens()

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
    print("difference change in ", (time.time()-tc) / 60, " minutes")
    print("built index in ", (time.time()-t3) / 60, " minutes")

    
    print("writing inverted index to file")
    with open('index.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(inverted_index)

    #read .bin with pickle.load
    with open('inverted_index.bin', mode='wb') as file2:
        pickle.dump(inverted_index, file2)
        

    with open('unique.txt', mode='w') as file:
        for word in unique:
            file.write(word+"\n")




t1 = time.time()
build_inverted_index()
print("executed in: " ,(time.time()-t1) / 60, " minutes")