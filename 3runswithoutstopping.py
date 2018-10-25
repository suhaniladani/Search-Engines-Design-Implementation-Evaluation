from helper import *
import nltk
from math import log
import os
import sys
from relevence_working import *
from query_to_dic import *
from generatingstopwords import *

import collections
from collections import OrderedDict
from operator import itemgetter


dl = {}    # dict of document name and doc length by doc name ie id
avdl = 0  #avg document length
colvoc=0  #total words in volcal
docnames = {}  #document names dic with no can be used for mapping
m = 0    #counter while printing
termdocidtf = {}   # term with document id as well as term frequency  in each file
termdocfreq = {}     # term with its document frequency ie term - df
docidbm = {}    # For BM25 dict with doc id and bm25 value
docdf={}        # for doc and document freq
docidtfidf={}       # for TF IDF dict with doc id and tf idf value
docidsmq={}         #for SMoothed Query Doc id and smq value
termcolfreq={}    # term and collection frequency


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
                colvoc= colvoc+ len(line)
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
        termdocfreq[term] = len(eachd) - 1
        termid = {}
        for doc in eachd:
            if doc not in ("\n"):
                doc = doc.split(" ")
                docid = doc[0]
                tf = doc[1]
                termid[docid] = tf
        termdocidtf[term] = termid
    file.close()

def colfreq(q):
    return termcolfreq[q]/colvoc

def calcR(q_id):
    q_id=str(q_id)
    try:
        return qid_R[q_id]
    except:
        return 0

def calri(q,q_id):
    c=0;
    q_id=str(q_id)
    try:
        for i in qid_reldocs[q_id]:
            try:
                termdocidtf[q][i]
                c = c + 1
            except:
                c = c
        return c
    except:
        return 0

def tf(term,docname,nam):
    global termdocidtf,dl

    return int(termdocidtf[term][docname])/int(dl[nam])

def idf(term):
    global termdocfreq

    return log(3204/termdocfreq[term])

def bmranking(query, q_id):

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

            bm = bm + score_BM25(termdocfreq[q], int(t), query[q], calri(q,q_id), 3204, dl[nam], avdl,calcR(q_id))

        docidbm[nam] = docidbm[nam] + bm

    keys = sorted(docidbm, key=docidbm.get, reverse=True)
    m = 0
    # os.chdir(os.path.join(sys.path[0],"bm25_result"))
    #os.chdir("C:\\Users\\Rahul\\PycharmProjects\\IRpr\\bm25_result")
    #file = open(str(q_id)+".txt", 'w', encoding='utf-8')
    for i in keys:

        if m > 99:
            break
        else:
            m = m + 1
            rank = str(m)
            print(str(q_id) + " Q0" " " + i + " " + rank + " " + str(docidbm[i]) + " BM25" + "\n")
            #file.write(str(q_id) + " Q0" " " + i + " " + rank + "  " + str(docidbm[i]) + " BM25" + "\n")

    #file.close()

def tfidfranking(query, q_id):

    for i in range(1, len(docnames)):
        final=0
        nam = docnames[i]
        docidtfidf[nam] = 0
        ii = nam.split(" ")
        ii = ''.join(ii)
        ii=ii.rstrip()
        bm = 0

        for q in query:
            try:
                final = final + query[q]*tf(q,ii,nam)*idf(q)
            except:
                final = final + 0

        docidtfidf[nam] = docidtfidf[nam] + final

    keys = sorted(docidtfidf, key=docidtfidf.get, reverse=True)
    m = 0

    #os.chdir(os.path.join(sys.path[0], "tfidf_result"))
    #os.chdir("C:\\Users\\Rahul\\PycharmProjects\\IRpr\\tfidf_result")
    #file = open(str(q_id) + ".txt", 'w', encoding='utf-8')
    for i in keys:

        if m > 99:
            break
        else:
            m = m + 1
            rank = str(m)

            print(str(q_id) + " Q0" " " + i + " " + rank + "  " + str(docidtfidf[i]) + " TF-IDF " + "\n")
            #file.write(str(q_id) +" Q0" " "+ i + " " + rank + "  " + str(docidtfidf[i]) + " TF-IDF " + "\n")
    #file.close()

def smoothedquery(query, q_id):

    for i in range(1, len(docnames)):
        final=0
        nam = docnames[i]
        docidsmq[nam] = 0
        ii = nam.split(" ")
        ii = ''.join(ii)
        ii=ii.rstrip()
        bm = 0

        for q in query:
            try:
                final = final + query[q]*log(((0.65*tf(q,ii,nam))/(0.35*colfreq(q)))+1)


            except:
                final = final + 0

        docidsmq[nam] = docidsmq[nam] + final

    keys = sorted(docidsmq, key=docidsmq.get, reverse=True)
    m = 0

    #os.chdir(os.path.join(sys.path[0], "smq_result"))
    #os.chdir("C:\\Users\\Rahul\\PycharmProjects\\IRpr\\smq_result")
    #file = open(str(q_id) + ".txt", 'w', encoding='utf-8')
    for i in keys:

        if m > 99:
            break
        else:
            m = m + 1
            rank = str(m)
            print(str(q_id) + " Q0  " + i + " " + rank + "  " + str(docidsmq[i]) + " SMQ " + "\n")
            #file.write(str(q_id) +" Q0" " "+ i + " " + rank + "  " + str(docidsmq[i]) + " SMQ " + "\n")
    #file.close()

def query_ref(q):
    query = {}
    filename = q
    q = q.lower()
    q = nltk.word_tokenize(q)
    ql = len(q)
    c = []
    for i in q:
        if i in termdocidtf:
            c.append(i)
    #print(c)

    for i in c:
        if i in query:
            query[i] += 1
        else:
            query[i] = 1
    return query


def main():
    dlandavdl()
    docwithtermfreq()
    print("Select")
    print("1 for BM25")
    print("2 for TFIDF")
    print("3 for Smoothed_query")
    print("q to quit")
    sel = input()

    if (sel == "1"):
        for qid in qid_query:
            query = qid_query[qid]
            q_id = qid
            query = query.rstrip()
            bmranking(query_ref(query), q_id)
        main()
    if (sel == "2"):
        for qid in qid_query:
            query = qid_query[qid]
            q_id = qid
            query = query.rstrip()
            tfidfranking(query_ref(query), q_id)
        main()
    if (sel == "3"):
        for qid in qid_query:
            query = qid_query[qid]
            q_id = qid
            query = query.rstrip()
            smoothedquery(query_ref(query), q_id)
        main()
    if(sel=="q"):
        print("Thank You")


main()
#bmranking(query_ref("time sharing system"),"1")