import os
import sys
qid_reldocs={}
qid_R={}
fh = open("changedqueryrel.txt", 'r', encoding='utf-8')

for i in fh:
    if i not in ("\n"):

        i = i.split(" ")

        id = i[0]
        doc = i[2]

        if id not in qid_reldocs and id not in qid_R:
            qid_reldocs[id] = [doc]
            qid_R[id] = 1

        else:
            qid_reldocs[id].append(doc)
            qid_R[id] = qid_R[id] + 1


#print(qid_reldocs)



