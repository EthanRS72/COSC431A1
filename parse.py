import time

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
    
    print(len(doc_text))
    for i in range(len(doc_text)):
        doc_text[i] = str(doc_text[i]).split()
        temp = []
        for x in range(len(doc_text[i])):
            if doc_text[i][x].isalpha():
                temp.append(doc_text[i][x])
                print(doc_text[i][x])
        doc_text[i] = temp
        print()

    print("parsed tokens in: ", (time.time() - tp) / 60, " minutes")
    return doc_text, docnos


parse_tokens()