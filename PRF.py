from math import log
import os
import sys
import collections
from collections import OrderedDict
from operator import itemgetter
import nltk
from query_to_dic import *

k1 = 1.2
k2 = 100
b = 0.75
R = 0.0
r = 0.0
dl = {}
avdl = 0
colvoc=0
docnames = {}
m = 0
termdocidtf = {}
doctermdocidtf = {}
docidbm = {}
termcolfreq={}
termTF = {}

n_prf = 10
k_prf = 10

stopwordlist = []
fh = open("common_words.txt", 'r', encoding='utf-8')
for line in fh:
    line = line.split("\n")

    stopwordlist.append(line[0])
fh.close()

def score_BM25(n, f, qf, r, N, dl, avdl):
    K = compute_K(dl, avdl)
    first = log(((r + 0.5) / (R - r + 0.5)) / ((n - r + 0.5) / (N - n - R + r + 0.5)))
    second = ((k1 + 1) * f) / (K + f)
    third = ((k2 + 1) * qf) / (k2 + qf)
    return first * second * third


def compute_K(dl, avdl):
    return k1 * ((1 - b) + b * (float(dl) / float(avdl)))


# To make the document with Doc Id and Document Length
# with storing doc names in one list

def dlandavdl():
    global m, avdl, dl, docnames,colvoc
    v = os.path.join(sys.path[0], "SP")
    os.chdir(v)
    y = os.listdir(v)
    for i in y:
        m = m + 1
        with open(i, encoding='utf-8') as f:
            for line in f:
                dm = i.split(".txt")
                dm = dm[0]
                line = line.split(" ")
                dl[dm] = len(line)
                colvoc = colvoc+ len(line)
                for i in line:
                    if i in termcolfreq:
                        termcolfreq[i] = termcolfreq[i] + 1
                    else:
                        termcolfreq[i] = 1

            docnames[m] = dm
        avdl = avdl + len(line)

    avdl = avdl / 3204

# String in a dictionary of dictionary
# that is  a 2D array kind of a thing
# docid    d1 d2 d3 d4 d5
# terms
# term1     3  4  9  2  4
# term2     5  7  1  5  8
# .
# .
# .term n


def docwithtermfreq():
    x = os.path.join(sys.path[0], "projonegramterm.txt")
    file = open(x, 'r', encoding='utf-8')
    for line in file:
        line = line.split(">>")
        term = line[0]
        eachd = line[1].split(";")
        doctermdocidtf[term] = len(eachd) - 1
        termid = {}
        for doc in eachd:
            if doc not in ("\n"):
                doc = doc.split(" ")
                docid = doc[0]
                tf = doc[1]
                termid[docid] = tf
        termdocidtf[term] = termid

    file.close()


def findMostFreqWords(relevant_docs):

    new_queryWords = ""
    queryArray = nltk.word_tokenize(query)
    tempQueryWords = []
    tempQueryWords2 = []
    otherWords = []
    newTermColFreq = {}
    tempTermList = []
    tempTermColFreqList = {}

    for doc in relevant_docs:

        os.chdir(os.path.join(sys.path[0], "SP"))
           # "/media/aail/OS/MSCS_NEU/Semester1/InformationRetreival_NadaNaji/Project/ImplementationPart1/SP")
        with open(doc+".txt", encoding='utf-8') as f:
            for line in f:
                line = line.split(" ")

                for i in line:
                    if i in termTF:
                        termTF[i] = termTF[i] + 1
                    else:
                        termTF[i] = 1

    termTFSorted = {}
    sortedList = sorted(termTF.items(), key=lambda x:x[1], reverse=True)
    termTFSorted = OrderedDict(sortedList)
    termTFSortedItems = list(termTFSorted.items())

    indexCount = 0

    for term in termTFSorted:

        if indexCount>0:
            if termTFSorted[term] == termTFSorted[prevTerm] and indexCount!=(len(termTFSortedItems)-1):
                if len(tempTermList)==0:

                    tempTermList.append(prevTerm)
                    tempQueryWords = tempQueryWords[:-1]
                tempTermList.append(term)

            elif termTFSorted[term] == termTFSorted[prevTerm] and indexCount==(len(termTFSortedItems)-1):
                if len(tempTermList) > 0:
                    tempTermList.append(term)
                    for t in tempTermList:

                        tempTermColFreqList.update({t: termcolfreq[t]})

                    sortedTermColFreqList = sorted(tempTermColFreqList.items(), key=lambda x: x[1])
                    termColFreqSorted = OrderedDict(sortedTermColFreqList)
                    termColFreqSortedItems = list(termColFreqSorted)

                    tempQueryWords = tempQueryWords + termColFreqSortedItems
                    tempTermList = []
                    tempTermColFreqList = {}


            else:
                if len(tempTermList)>0:
                    for t in tempTermList:

                        tempTermColFreqList.update({t: termcolfreq[t]})

                    sortedTermColFreqList = sorted(tempTermColFreqList.items(), key=lambda x: x[1])
                    termColFreqSorted = OrderedDict(sortedTermColFreqList)
                    termColFreqSortedItems = list(termColFreqSorted)

                    tempQueryWords = tempQueryWords + termColFreqSortedItems
                    tempTermList = []
                    tempTermColFreqList = {}

                tempQueryWords.append(term)
        else:
            tempQueryWords.append(term)

        prevTerm = term
        indexCount = indexCount + 1

    for word in tempQueryWords:
        if word != '' and word not in stopwordlist:
            tempQueryWords2.append(word)

    newQueryWordsArray = new_queryWords.split(" ")


    noOfTerms = 0
    i=0

    while(noOfTerms<k_prf):

        if tempQueryWords2[i] not in newQueryWordsArray:
            noOfTerms = noOfTerms + 1

            new_queryWords = new_queryWords + " " + tempQueryWords2[i]

        i = i + 1

    new_queryWords = new_queryWords.split(' ')
    new_queryWords = new_queryWords[1:]
    new_queryWords = ' '.join(new_queryWords)

    ranking2(query+" "+new_queryWords)


def bm25main():
    global query
    global q_id
    global count
    global flag_prf

    count = 0
    flag_prf = 0

    dlandavdl()
    docwithtermfreq()


    for qid in qid_query:

        query = qid_query[qid]
        q_id = qid
        query = query.rstrip()

        ranking(query)

    print("Thank You")

def ranking(q):

    global count
    global flag_prf

    count = count + 1
    relevant_docs = []

    query = {}
    filename = q
    q = q.lower()
    q = nltk.word_tokenize(q)
    ql = len(q)
    c = []
    for i in q:
        if i in termdocidtf:
            c.append(i)
    print(c)

    for i in c:
        if i in query:
            query[i] += 1
        else:
            query[i] = 1
    for i in range(1, len(docnames)):

        nam = docnames[i]
        docidbm[nam] = 0
        ii = nam.split(" ")
        ii = ''.join(ii)
        bm = 0
        for q in query:

            try:

                t = termdocidtf[q][ii]


            except:

                t = 0

            bm = bm + score_BM25(doctermdocidtf[q], int(t), query[q], r, 3204, dl[nam], avdl)

        docidbm[nam] = docidbm[nam] + bm

    keys = sorted(docidbm, key=docidbm.get, reverse=True)

    if count%2!=0:
        new_queryWords = ""
        relevant_docs = keys[0:n_prf]

        flag_prf = 1
        findMostFreqWords(relevant_docs)


    m = 0
    for i in keys:

        if m > 99:
            break
        else:
            m = m + 1
            rank = str(m)

            flag_prf = 0

def ranking2(q):

    global count
    global flag_prf

    count = count + 1
    relevant_docs = []

    query = {}
    filename = q
    q = q.lower()
    q = nltk.word_tokenize(q)
    ql = len(q)
    c = []
    for i in q:
        if i in termdocidtf:
            c.append(i)
    print(c)

    for i in c:
        if i in query:
            query[i] += 1
        else:
            query[i] = 1
    for i in range(1, len(docnames)):

        nam = docnames[i]
        docidbm[nam] = 0
        ii = nam.split(" ")
        ii = ''.join(ii)
        bm = 0

        for q in query:

            try:

                t = termdocidtf[q][ii]

            except:

                t = 0

            bm = bm + score_BM25(doctermdocidtf[q], int(t), query[q], r, 3204, dl[nam], avdl)

        docidbm[nam] = docidbm[nam] + bm

    keys = sorted(docidbm, key=docidbm.get, reverse=True)

    m = 0
    #os.chdir(os.path.join(sys.path[0], "Results_PRF"))
    #file = open(str(q_id) + ".txt", "w")
    for i in keys:

        if m > 99:
            break
        else:
            m = m + 1
            rank = str(m)

            print(str(q_id) + " Q0" " " + i + " " + rank + " " + str(docidbm[i]) + " PRF" + "\n")

            #file.write(str(q_id) +" Q0" " " + i + " " + rank + " " + str(docidbm[i])+ " PRF "  + "\n")

bm25main()


