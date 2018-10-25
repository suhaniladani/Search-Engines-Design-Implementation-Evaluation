#from makingN_R import *
import os
import sys

def calcMRR(path,sysnam):
    #file=open("RR.txt")
    y = os.chdir(os.path.join(sys.path[0], path))
    y = os.listdir(y)
    count = 0
    c=0
    for i in y:
        fe = open(i, 'r', encoding='utf-8')
        m=0

        for line in fe:
            try:
                if line.startswith("R"):
                    m = m + 1
                    count=count+1
                    break
                elif line.startswith("N"):
                    m = m + 1
                else:
                    print("All are Nonrelevant")

            except:
                print("Ignore as no relevant data available")

        #print(i)
        cm=i.split(".txt")
        try:
            print("RR for query id  " + str(cm[0]) +" is "  +  str(1/m))
            c = c + (1 / m)
        except:
            c=c
            print(str(i)+" RR cannot be found")


    c=c/count
    print("MRR for the System " + sysnam + " is " + str(c))


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
        calcMRR("NR\\bm25_NR","BM25")
    if (sel == "2"):
        calcMRR("NR\\tfidf_NR","TFIDF")
    if (sel == "3"):
        calcMRR("NR\\smq_NR","SMQ")
    if (sel == "4"):
        calcMRR("NR\\lucene_NR","Lucene")
    if (sel == "5"):
        calcMRR("NR\\PRF_NR","PRF")
    if (sel == "6"):
        calcMRR("NR\\bm25stop_NR","BM25 with stop")
    if (sel == "7"):
        calcMRR("NR\\tfidfstop_NR","TFIDF with Stop")
    if (sel == "8"):
        calcMRR("NR\\smqstop_NR","SMQ with stop")




# t=True
# while t :
#     main()
#     i=input("Do u wanna quit? press q - ")
#     if i == "q":
#         t=False
#         print("Thank You")
#     else:
#         t=True

# EC1
calcMRR("EC2_nr","proximity with stopping")
