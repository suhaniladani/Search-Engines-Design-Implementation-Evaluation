import os
import sys
import string
from relevence_working import *
p=0
re=0

counter=0

def caclP_RE(path,sysnam):
    y = os.chdir(os.path.join(sys.path[0], path))
    y = os.listdir(y)
    #os.chdir("C:\\Users\\Rahul\\PycharmProjects\\IRpr\\NR\\bm25_NR")
    counter=0
    map = 0
    #file = open("PRF_p_20", 'w', encoding='utf-8')
    for i in y:
        print("-----------next query -------------")
        print("\n\n")
        #os.chdir("C:\\Users\\Rahul\\PycharmProjects\\IRpr\\recall\\re_tfidf_nostop")
        #file = open(i, 'w', encoding='utf-8')
        print("next doc" + i)
        m = 0
        p = 0
        avp=0

        mapp=0
        relcount = 0
        c = str(i)
        c = c.split(".txt")
        c = c[0]
        # os.chdir("C:\\Users\\Rahul\\PycharmProjects\\IRpr\\NR\\tfidf_NR")
        fe = open(i, 'r', encoding='utf-8')

        for line in fe:
            m = m + 1
            if line.startswith("N"):
                relcount = relcount
                p = relcount / m

                re = relcount / qid_R[c]
                print("Recall at rank " + str(m) + " " + str(re) + "\n")
                print("Precision at rank " + str(m) + " " + str(p) + "\n")
                # file.write("Recall at rank "+ str(m)+" " +str(re)+"\n")
                # if m==20:
                #      i = str(i)
                #      i=i.rstrip(".txt")
                #      #file.write("precision at 20 for query id"+ str(i)+"  is " + str(p)+"\n")

            else:
                relcount = relcount + 1
                p = relcount / m
                re = relcount / qid_R[c]
                print("Recall at rank " + str(m) + " " + str(re) + "\n")
                print("Precision at rank " + str(m) + " " + str(p) + "\n")
                # file.write("Recall at rank " + str(m) + " " + str(re) + "\n")
                # if m==20:
                #     i=str(i)
                #     i=i.rstrip(".txt")
                    #file.write("precision at 20 for query id" + str(i) + "  is  " + str(p)+"\n")
                #if m==20:
                #      print("precision at 20" + str(p))

                avp = avp + p


        try:
            map=map+avp/qid_R[c]
            print("Average Precision for query id " +str(i)+ " is "+str(avp/qid_R[c]))
            counter=counter+1
            #print(map)
            #print("arp "+str(avp/qid_R[c]))
        except:
            print("Average Precision for query id " + str(i) + "cannot be found ")
            map=map
        mapp=mapp+map
    #print(mapp)
    mapp=mapp/counter
    print("Map for System " + str(sysnam)+ "is  " + str(mapp))
# def calcMRR(y):
#     #file=open("RR.txt")
#     count = 0
#     c=0
#     for i in y:
#         fe = open(i, 'r', encoding='utf-8')
#         m=0
#
#         for line in fe:
#             try:
#                 if line.startswith("R"):
#                     m = m + 1
#                     count=count+1
#                     break
#                 elif line.startswith("N"):
#                     m = m + 1
#                 else:
#                     print("All are Nonrelevant")
#
#             except:
#                 print("Ignore as no relevant data available")
#
#         #print(i)
#         cm=i.split(".txt")
#         try:
#             print("RR for query id  " + str(cm[0]) +" is "  +  str(1/m))
#             c = c + (1 / m)
#         except:
#             c=c
#             print(str(i)+" RR cannot be found")
#
#
#     c=c/count
#     print("MRR for the System lucene is " + str(c))
#caclP_RE(y)
#calcMRR(y)
def main():
    print("Select")
    print("1 for BM25")
    print("2 for TFIDF")
    print("3 for Smoothed_query")
    print("4 for Lucene")
    print("5 for Pseudo Relevance Feedback")
    print("6 for BM25 with stopping")
    print("7 for TFIDF with stopping")
    print("8 for Smoothed_query with stopping")
    sel=input()

    if (sel == "1"):
        caclP_RE("NR\\bm25_NR","BM25")
    if (sel == "2"):
        caclP_RE("NR\\tfidf_NR","TFIDF")
    if (sel == "3"):
        caclP_RE("NR\\smq_NR","SMQ")
    if (sel == "4"):
        caclP_RE("NR\\lucene_NR","Lucene")
    if (sel == "5"):
        caclP_RE("NR\\PRF_NR","PRF")
    if (sel == "6"):
        caclP_RE("NR\\bm25stop_NR","BM25 with stop")
    if (sel == "7"):
        caclP_RE("NR\\tfidfstop_NR","TFIDF with Stop")
    if (sel == "8"):
        caclP_RE("NR\\smqstop_NR","SMQ with stop")



t=True
while t :
    main()
    i=input("Do u wanna quit? press q  - ")
    if i == "q":
        t=False
        print("Thank You")
    else:
        t=True

