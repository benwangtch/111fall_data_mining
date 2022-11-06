from collections import defaultdict, OrderedDict
from csv import reader
from itertools import chain, combinations
from optparse import OptionParser
from utils import *
import time
def fpgrowth(itemSetList, minSupRatio, minConf):
    frequency = getFrequencyFromList(itemSetList)
    minSup = len(itemSetList) * minSupRatio
    fpTree, headerTable = constructTree(itemSetList, frequency, minSup)
    if(fpTree == None):
        print('No frequent item set')
    else:
        freqItems = []
        mineTree(headerTable, minSup, set(), freqItems)
        rules = associationRule(freqItems, itemSetList, minConf)
        return freqItems, rules
    
def dataFromFile(fname):
    """Function which reads from the file and yields a generator"""
    with open(fname, "r") as file_iter:
        for line in file_iter:
            line = line.strip().rstrip(",")  # Remove trailing comma
            record = frozenset(line.split(",")[3:])
            
            yield record
            
def fpgrowthFromFile(fname, minSupRatio, minConf):
    itemSetList, frequency = getFromFile(fname)
    minSup = len(itemSetList) * minSupRatio
    fpTree, headerTable = constructTree(itemSetList, frequency, minSup)
    
    if(fpTree == None):
        print('No frequent item set')
    else:
        freqItems = []
        mineTree(headerTable, minSup, set(), freqItems)
        return freqItems
    
if __name__ == "__main__":
    start_time = time.time()
    file2 = []
    optparser = OptionParser()
    optparser.add_option('-f', '--inputFile',
                         dest='inputFile',
                         help='CSV filename',
                         default=None)
    optparser.add_option('-s', '--minSupport',
                         dest='minSup',
                         help='Min support (float)',
                         default=0.5,
                         type='float')
    optparser.add_option('-c', '--minConfidence',
                         dest='minConf',
                         help='Min confidence (float)',
                         default=0.5,
                         type='float')

    (options, args) = optparser.parse_args()
    iterround = 0
    freqItemSet = fpgrowthFromFile(
        options.inputFile, options.minSup, options.minConf)
    
    
    
    minSu = options.minSup
    thefile = options.inputFile #get input data for saving file
    itemSetList, frequency = getFromFile(thefile)
    
    f2= open("step3_task1_%s_%.1f_result2.txt"%(thefile, minSu*100), "w+")
  
    f1= open("step3_task1_%s_%.1f_result1.txt"%(thefile, minSu*100), "w+")
    
    outputsets = [] # write the output results to a set(item, support) structure
    if freqItemSet!=None:
        for item in freqItemSet:
            itemCnt = 0
            for line in itemSetList:
                if line.issuperset(item):
                    itemCnt+=1
            outputsets.append((item, itemCnt/len(itemSetList)))
    
    
                
    
    cnt = 0 #count the freqsets
    for item, support in sorted(outputsets, key=lambda x: x[1]): 
        f1.write("%.1f\t%s\n" % (support*100, str(item)))
        cnt+=1
    
    f2.write(str(cnt)) #record the total mined in file 2
    total_time= time.time() - start_time # total computation time
    f2.write("The total computation time is : %s seconds"%total_time) #record the time
    # print(freqItemSet,"\n")
    print("The total computation time is :",total_time, " seconds")
    