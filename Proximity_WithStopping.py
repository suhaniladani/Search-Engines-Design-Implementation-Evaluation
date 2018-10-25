from math import log
import os
import sys
import collections
from collections import OrderedDict
from operator import itemgetter
import nltk
from query_to_dic import *
from generatingstopwords import *

k1 = 1.2
k2 = 100
b = 0.75
R = 0.0
r = 0.0
dl = {}
avdl = 0
docnames = {}
m = 0
termdocidtf = {}
doctermdocidtf = {}
docidbm = {}

def Positions(doc):
    global noOfTermsAppearingConseq, sumOfIntermediateTerms, query

    os.chdir(os.path.join(sys.path[0], "SP"))
    file = open(doc+'.txt', 'r')
    global query
    queryNew = query.lower()
    queryNew = nltk.word_tokenize(queryNew)
    docTermsWithoutStop = file.read().split()
    docTerms = []

    for i in range(0, len(docTermsWithoutStop)):
        if docTermsWithoutStop[i] not in stopwordlist:
            docTerms.append(docTermsWithoutStop[i])

    myDict = {}
    counterList = []
    commonTerms = []


    for qTerm in queryNew:
        if qTerm in docTerms:
            commonTerms.append(qTerm)

    for word in docTerms:
        index = [i for i, x in enumerate(docTerms) if x == word]

        if word not in myDict:

            myDict[word] = index

    timesProcessed = {}

    sumOfIntermediateTerms = 0
    noOfTermsAppearingConseq = 0
    commonTermsReversed = list(reversed(commonTerms))

    for i in range(0, len(commonTerms)-1):

        for r in range(0, len(myDict[commonTerms[i]])):
            for v in range(0, len(myDict[commonTerms[i+1]])):
                subtraction = myDict[commonTerms[i]][r] - myDict[commonTerms[i+1]][v]

                if subtraction<0 and abs(subtraction)<=4:
                    noOfTermsAppearingConseq = noOfTermsAppearingConseq + 1
                    sumOfIntermediateTerms = sumOfIntermediateTerms + abs(subtraction)

    file.close()


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
    global m, avdl, dl, docnames
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


def ranking(q):
    global noOfTermsAppearingConseq, sumOfIntermediateTerms

    query = {}
    filename = q
    q = q.lower()
    q = nltk.word_tokenize(q)
    ql = len(q)
    #print(q)
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
        Positions(nam)
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

        if sumOfIntermediateTerms > 0 and noOfTermsAppearingConseq > 0:
            bm = bm * noOfTermsAppearingConseq * (1 / sumOfIntermediateTerms)
        elif noOfTermsAppearingConseq > 0 and sumOfIntermediateTerms <= 0:
            bm = bm * noOfTermsAppearingConseq
        elif noOfTermsAppearingConseq <= 0 and sumOfIntermediateTerms > 0:
            bm = bm * (1 / sumOfIntermediateTerms)
        else:
            bm = bm
        docidbm[nam] = docidbm[nam] + bm

    keys = sorted(docidbm, key=docidbm.get, reverse=True)
    m = 0
    os.chdir(os.path.join(sys.path[0], "Results_WithTermPositions_WithStopping"))
    file = open(str(q_id) + ".txt", "w")
    for i in keys:

        if m > 99:
            break
        else:
            m = m + 1
            rank = str(m)
            print(str(q_id) + " Q0" " " + i + " " + rank + " " + str(docidbm[i]) + " WithTermPositions_WithStopping" + "\n")
            file.write(str(q_id) +" Q0" " " + i + " " + rank + " " + str(docidbm[i])+ " WithTermPositions_WithStopping"  + "\n")


def bm25main():
    global query, q_id
    dlandavdl()
    docwithtermfreq()

    for qid in qid_query:

        query = qid_query[qid]
        q_id = qid
        query = query.rstrip()

        ranking(query)

    print("Thank You")

bm25main()
