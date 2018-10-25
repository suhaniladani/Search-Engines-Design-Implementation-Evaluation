import os
import sys
from relevence_working import *

os.chdir("C:\\Users\\Rahul\\PycharmProjects\\IRpr\\Trial")
y=os.listdir(os.curdir)

for i in y:
    os.chdir("C:\\Users\\Rahul\\PycharmProjects\\IRpr\\Trial")
    with open(i, encoding='utf-8') as f:
        os.chdir("C:\\Users\\Rahul\\PycharmProjects\\IRpr\\Trial_nr")
        fh = open(i, 'w', encoding='utf-8')
        for line in f:
            try:

                line = line.split(" ")
                document = line[2]

                if document in qid_reldocs[str(line[0])]:
                    fh.write("R\n")
                    print("R")
                else:
                    fh.write("N\n")
                    print("N")
            except:
                print("i")

    print("done")

