import time
import csv

def parse_tokens():
    tp = time.time()
    punc = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", ":", ";", "'", ",", ".", "?", '"',"`", "-", "_", "+", "=", "[", "]", "{", "}", "|"]
    docnos = []
    doc_text = [] 
    file = open('wsj.xml', 'r')
    words = file.read().lower()
    words = words.replace("<", " <")
    for i in range(len(punc)):
        if punc[i] == "-" or punc[i] == "." or punc[i] == ",":
            words = words.replace(punc[i], " ")
        else:
            words = words.replace(punc[i], "")

    words = ' '.join(words.split())
    words = words.split()

    txt = ""
    for i in range(len(words)):
        if words[i] != "<doc>":
            if words[i][0] != "<":
                txt = txt + " " + words[i]
        else:
            if txt != "":
                txt = txt.replace("/", " ")
                doc_text.append(txt)
            txt = ""
        if i == len(words)-1:
            txt = txt + " " + words[i]
            doc_text.append(txt)
    
    for i in range(len(doc_text)):
        temp = str(doc_text[i]).split()
        doc_text[i] = temp
        if i == len(doc_text)-1:
            doc_text[i] = doc_text[i][:-2]
        for x in range(len(doc_text[i])-1):
            if x == 0:
                val = doc_text[i][2]
                doc_text[i][0] = doc_text[i][0] + "-" + doc_text[i][1]
                del doc_text[i][1]
                doc_text[i][1] = val
                docnos.append(doc_text[i][0])
            #print(doc_text[i][x])
        #print("\n")
    print("parsed tokens in: ", (time.time() - tp) / 60, " minutes")
    print(doc_text[-1])
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
    print(len(doc_text))
    print(len(unique))

    
    print("writing inverted index to file")
    with open('test.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(inverted_index)




t1 = time.time()
build_inverted_index()
print("executed in: " ,(time.time()-t1) / 60, " minutes")