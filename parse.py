#Ethan Smith - COSC431 Assignment 1 2023
import sys
import time

def parse_tokens():
    t = time.time()

    #preprocess wsj.xml file so it can be split into tokens
    remove = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", ":", ";", "'", ",", ".", "?", '"',"`", "-", "_", "+", "=", "[", "]", "{", "}", "|", "0", "1", "2", "3", "4", "5", "6","7","8", "9"]
    docnos = []
    doc_text = [] 
    file = open('wsj.xml', 'r')
    words = file.read().lower()
    words = words.replace("<", " <")
    words = words.replace(".", " .")
    words = words.replace(",", " ,")
    words = words.split()

    #extract all document numbers and save them to use as a reference
    for i in range(len(words)):
        if words[i] == "<docno>":
            docnos.append(words[i+1])

    #once docnos are saved all hyphens can be removed
    words = ' '.join(words)
    for i in range(len(remove)):
            if remove[i] == "-":
                words = words.replace(remove[i], " ")
            else:
                words = words.replace(remove[i], "")
    words = ' '.join(words.split())
    words = words.split()

    #take the list of words and split them into tokens for each document
    #based on the tags
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
        
    #for each document take the words remove all non alphabetic tokens
    #and output the valid tokens with a line seperating documents
    for i in range(len(doc_text)):
        doc_text[i] = str(doc_text[i]).split()
        temp = []
        for x in range(len(doc_text[i])):
            if doc_text[i][x].isalpha():
                temp.append(doc_text[i][x])
                sys.stdout.write(doc_text[i][x]+"\n")
        doc_text[i] = temp
        sys.stdout.write("\n")

    runtime = "parsed tokens in: {:.2f} minutes".format((time.time() - t) / 60)
    sys.stdout.write(runtime+"\n")
    return doc_text, docnos

parse_tokens()