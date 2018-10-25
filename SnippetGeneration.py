from math import log
import os
import sys
import collections
import string
from query_to_dic import *
from collections import OrderedDict
from bs4 import BeautifulSoup
import nltk
from generatingstopwords import *

impQueryTerms=[]
termcolfreq={}
tempTermDocFreqList ={}
doctermdocidtf = {}
termdocidtf = {}

noOfImpTerms =12

v = os.path.join(sys.path[0], "SP")
os.chdir(v)
y = os.listdir(v)
for i in y:
    
    with open(i, encoding='utf-8') as f:
        for line in f:
            
            line = line.split(" ")
            
            for i in line:
                if i in termcolfreq:
                    termcolfreq[i] = termcolfreq[i] + 1
                else:
                    termcolfreq[i] = 1

      

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



sentence=[]
punct = ['!',"''","'", '#', '"','``', '%', '$', '&', ')','”','“','.','(', '+', '*', '-','[',']','{','}',':',';',"b'",'"','"',',']

os.chdir(os.path.join(sys.path[0], "cacm"))

def impw(orgq,filename):
    global tempTermDocFreqList,impQueryTerms
    # query = "I am interested in articles written either by Prieve or Udo Pooch Prieve, B. Pooch, U."
    query=orgq
    query = query.lower()
    query = nltk.word_tokenize(query)
    for q in query:
        if q in termcolfreq:
            tempTermDocFreqList.update({q: termcolfreq[q]})

    sortedTermColFreqList = sorted(tempTermDocFreqList.items(), key=lambda x: x[1])
    termColFreqSorted = OrderedDict(sortedTermColFreqList)
    termColFreqSortedItems = list(termColFreqSorted)

    tempTermList = []
    indexCount = 0
    tempQueryWords = []
    startIndex = 0
    endIndex = 0
    tempTermDocFreqList = {}
    for term in termColFreqSorted:

       
        if indexCount > 0:
            if termColFreqSorted[term] == termColFreqSorted[prevTerm] and indexCount!=(len(termColFreqSorted)-1):
                
                if len(tempTermList) == 0:
                    
                    startIndex = indexCount - 1
                    
                    tempTermList.append(prevTerm)
                    tempQueryWords = tempQueryWords[:-1]
                
                tempTermList.append(term)

            elif termColFreqSorted[term] == termColFreqSorted[prevTerm] and indexCount==(len(termColFreqSorted)-1):
                if len(tempTermList) > 0:
                    tempTermList.append(term)
                    for t in tempTermList:
                        
                        tempTermDocFreqList.update({t: doctermdocidtf[t]})

                    
                    sortedTermDocFreqList = sorted(tempTermDocFreqList.items(), key=lambda x: x[1])
                    termDocFreqSorted = OrderedDict(sortedTermDocFreqList)
                    termDocFreqSortedItems = list(termDocFreqSorted)

                    
                    tempQueryWords = tempQueryWords + termDocFreqSortedItems

                    tempTermList = []
                    tempTermDocFreqList = {}

            else:
                if len(tempTermList) > 0:
                    endIndex = indexCount - 1
                    for t in tempTermList:
                        # print(tempTermDocFreqList)
                        # tempTermDocFreqList[t] = termcolfreq[t]
                        tempTermDocFreqList.update({t: doctermdocidtf[t]})

                    # print("tempTermDocFreqList:",tempTermDocFreqList)
                    sortedTermDocFreqList = sorted(tempTermDocFreqList.items(), key=lambda x: x[1])
                    termDocFreqSorted = OrderedDict(sortedTermDocFreqList)
                    termDocFreqSortedItems = list(termDocFreqSorted)

                    
                    tempQueryWords = tempQueryWords + termDocFreqSortedItems

                    tempTermList = []
                    tempTermDocFreqList = {}

                    # print("yes")
                tempQueryWords.append(term)
        else:
            tempQueryWords.append(term)

        prevTerm = term
        indexCount = indexCount + 1

    impQueryTerms = tempQueryWords[0:noOfImpTerms]
    # print("sortedterms:",termColFreqSorted)
    # print("Important Terms:", impQueryTerms)

    simpgen2(impQueryTerms,filename)



def simpgen2(query,i):
    global sp
    os.chdir(os.path.join(sys.path[0], "cacm"))
    html = open(i, 'r', encoding='utf-8')

    soup = BeautifulSoup(html, "html.parser")
    t = soup.get_text()
    c=t.split("\n\n")


    t = t.split("\n\n")

    til = c[2].replace("\n", '')
    name = t[5].replace("\n", '')
    # sentence.append(name)
    # sp.write(til+"\n")
    print(til+"\n")
    sentence = []
    # sentence.append(name)


    for q in query:
        if q not in stopwordlist and q not in punct:
            for i in t:
                
                if i not in ("''"):
                    i = i.replace("\n", "")
                    i = i.split(".")
                    for e in i:
                        if (q) in e.lower():
                            if e not in sentence:
                                sentence.append(e)

    for sm in sentence:
        # sp.write(t+"  ")
        nm=nltk.word_tokenize(sm)
        

        for i in nm:
            if i.lower() in impQueryTerms:
                # sp.write(i.upper()+ " ")
                print(i.upper()+ " ")
            else:
                # sp.write(i+" ")
                print(i+" ")
            

    # sp.write("\n\n")
    # sp.write(c[-4]+"\n\n\n")
    print("\n\n")
    print(c[-4]+"\n\n\n")


v = os.path.join(sys.path[0], "Results\\Phase-1-Task-1\\BM25_BaseLine_Result")
os.chdir(v)
y = os.listdir(v)
for i in range(1,65):
    os.chdir(os.path.join(sys.path[0], "Results\\Phase-1-Task-1\\BM25_BaseLine_Result"))
    # sp=open(str(i)+".txt",'w',encoding='utf-8')
    q=qid_query[i]
    os.chdir(v)
    files=open(str(i)+".txt",'r',encoding='utf-8')
    for line in files:
        # sp.write("--------------------------------------------------------------\n")
        # sp.write(line)
        print("--------------------------------------------------------------\n")
        print(line)
        line=line.split(" ")
        print(line[2])
        filename=line[2]+".html"
        # sp.write("\n\n")
        print("\n\n")
        impw(q,filename)


