import os
import re
import sys

def unigram(rt,cur):
    print("j")
    os.chdir(rt)
    y = os.listdir(os.curdir)
    print(y)
    unig = cur+"\\unigramfile"
    if os.path.exists(unig):
        i=input("enter a unique file to store 100 unigram files for use")
        os.makedirs(unig+i)
    else:
        os.makedirs(unig)


    for i in y:
        ct = dict()
        os.chdir(rt)

        with open(i, encoding='utf-8') as f:
            for line in f:
                lines = re.split(" ", line)
                for lin in lines:
                    if lin in ct:
                        ct[lin] = ct[lin] + 1
                    else:
                        ct[lin] = 1
        tit = re.split(".txt", i)
        t = tit[0]

        os.chdir(unig)
        fh = open(t+ ".txt", 'w', encoding='utf-8')
        for m in ct:
            y = re.split("\\n", m)
            c = y[0]
            fh.write(str(c) + " "+str(t)+" " + (str(ct[m]))+"\n")
            #print(str(c)+" "+str(ct[m]))
            fh.close

    os.chdir(unig)
    y = os.listdir(os.curdir)

    onegramdic = {}
    for i in y:
        with open(i, encoding='utf-8') as f:
            for line in f:
                spl = re.split(" ", line)
                term = spl[0]
                doc = spl[1:-1]
                count = re.split("\n", str(spl[-1]))
                con = count[0]
                doc = ''.join(doc)

                doc = str(doc) + " " + str(con)+";"
                if term not in onegramdic:
                    onegramdic[term] = [doc]
                else:
                    onegramdic[term].append(doc)



    os.chdir(cur)
    print(onegramdic)
    fh=open("projonegramterm.txt",'w',encoding='utf-8')
    for key in onegramdic:
        i= ''.join(onegramdic[key])
        fh.write(str(key)+">>"+str(i)+"\n")
    fh.close()


def bigram(rt,cur):
    os.chdir(rt)
    y = os.listdir(os.curdir)
    big = cur + "\\bigramfile"
    if os.path.exists(big):
        i=input("enter a file name to store 100 bigram files")
        os.makedirs(big + i)

    else:
        os.makedirs(big)


    for i in y:
        ct = dict()
        os.chdir(rt)

        with open(i, encoding='utf-8') as f:
            for line in f:
                lines = re.split(" ", line)
                #print(len(lines))
                for cc in range((len(lines) - 1)):
                    y = (str(lines[cc] + " " + str(lines[cc + 1])))

                    # y=(str(lin)+" "+str(lines[lin+1]))
                    if y in ct:
                        ct[y] = ct[y] + 1
                    else:
                        ct[y] = 1
        tit = re.split(".txt", i)
        t = tit[0]

        os.chdir(big)
        fh = open(t+".txt", 'w', encoding='utf-8')
        for m in ct:
            y = re.split("\\n", m)
            c = y[0]
            fh.write(str(c) + " " + str(t) + " " + (str(ct[m])) + "\n")
            # print(str(c)+" "+str(ct[m]))
        fh.close

    os.chdir(big)
    y = os.listdir(os.curdir)

    bigramdic = {}
    for i in y:
        with open(i, encoding='utf-8') as f:
            for line in f:
                spl = re.split(" ", line)
                term = str(spl[0]) + " " + str(spl[1])

                doc = spl[2:-1]
                count = re.split("\n", str(spl[-1]))
                con = count[0]
                doc = ''.join(doc)
                doc = str(doc) + " " + str(con) + ";"
                if term not in bigramdic:
                    bigramdic[term] = [doc]
                else:
                    bigramdic[term].append(doc)

    os.chdir(cur)
    fh=open("bigramterm.txt",'w',encoding='utf-8')
    for key in bigramdic:
        i= ''.join(bigramdic[key])
        fh.write(str(key)+">>"+str(i)+"\n")
    fh.close()

def trigram(rt,cur):
    os.chdir(rt)
    y = os.listdir(os.curdir)
    trig = cur + "\\trigramfile"
    if os.path.exists(trig):
        i=input("enter  a file name to store 1000 tri gram files")
        os.makedirs(trig + i)

    else:
        os.makedirs(trig)


    for i in y:
        ct = dict()
        os.chdir(rt)

        with open(i, encoding='utf-8') as f:
            for line in f:
                lines = re.split(" ", line)
                #print(len(lines))
                for cc in range((len(lines) - 2)):
                    y = (str(lines[cc] + " " + str(lines[cc + 1]) + " " + str(lines[cc + 2])))

                    # y=(str(lin)+" "+str(lines[lin+1]))
                    if y in ct:
                        ct[y] = ct[y] + 1
                    else:
                        ct[y] = 1
        tit = re.split(".txt", i)
        t = tit[0]
        os.chdir(trig)
        fh = open(t+".txt", 'w', encoding='utf-8')
        for m in ct:
            y = re.split("\\n", m)
            c = y[0]
            fh.write(str(c) + " " + str(t) + " " + (str(ct[m])) + "\n")
            # print(str(c)+" "+str(ct[m]))
        fh.close
    os.chdir(trig)
    y = os.listdir(os.curdir)

    trigramdic = {}
    for i in y:
        with open(i, encoding='utf-8') as f:
            for line in f:
                spl = re.split(" ", line)
                term = str(spl[0]) + " " + str(spl[1] + " " + str(spl[2]))

                doc = spl[3:-1]
                count = re.split("\n", str(spl[-1]))
                con = count[0]
                doc = ''.join(doc)
                doc = str(doc) + " " + str(con) + ";"
                if term not in trigramdic:
                    trigramdic[term] = [doc]
                else:
                    trigramdic[term].append(doc)

    os.chdir(cur)
    fh=open("trigramterm.txt",'w',encoding='utf-8')
    for key in trigramdic:
        i= ''.join(trigramdic[key])
        fh.write(str(key)+">>"+str(i)+"\n")
    fh.close()


rtf = os.path.join(sys.path[0], "SP")

print("Implementing a inverted index")
cur=os.getcwd()
while True:
    x=input("enter your choice \n "
            "1 for Unigram \n "
            "2 for Bigram \n "
            "3 for Trigram \n "
            "4 to Exit")
    if( x == "1"):
        unigram(rtf,cur)
    if (x == "2"):
        bigram(rtf,cur)
    if (x == "3"):
        trigram(rtf,cur)
    if (x == "4"):
        break




#C:\\Users\\Rahul\\PycharmProjects\\rawtext\\SP
#C:\\Users\\Rahul\\PycharmProjects\\rawtext\\uniterm_(doc_id )_tf
#C:\\Users\\Rahul\\PycharmProjects\\rawtext\\biterm_(doc_id)_tf
#C:\\Users\\Rahul\\PycharmProjects\\rawtext\\triterm_(doc_id)_tf