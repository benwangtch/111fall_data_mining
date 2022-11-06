"""
Description     : Simple Python implementation of the Apriori Algorithm
Modified from:  https://github.com/asaini/Apriori
Usage:
    $python apriori.py -f DATASET.csv -s minSupport

    $python apriori.py -f DATASET.csv -s 0.15
"""

import sys
import time 
from itertools import chain, combinations
from collections import defaultdict
from optparse import OptionParser
def subsets(arr):
    """ Returns non empty subsets of arr, """
    return chain(*[combinations(arr, i + 1) for i, a in enumerate(arr)])


def returnItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet):
    """calculates the support for items in the itemSet and returns a subset
    of the itemSet each of whose elements satisfies the minimum support"""
    _itemSet = set()
    localSet = defaultdict(int)
    
    for item in itemSet:
        for transaction in transactionList:
            if item.issubset(transaction):
                freqSet[item] += 1
                localSet[item] += 1

    for item, count in localSet.items():
        support = float(count) / len(transactionList)

        if support >= minSupport:
            _itemSet.add(item)

    return _itemSet


def joinSet(itemSet, length):
    """Join a set with itself and returns the n-element itemsets"""
    return set(
        [i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length]
    )


def getItemSetTransactionList(data_iterator):
    transactionList = list()
    itemSet = set()
    for record in data_iterator:
        transaction = frozenset(record)
        
        transactionList.append(transaction)
        for item in transaction:
            
            itemSet.add(frozenset([item]))  # Generate 1-itemSets
            
    return itemSet, transactionList #itemset = 1-itemset transactionlist = every row in input


def runApriori(data_iter, minSupport):
    """
    run the apriori algorithm. data_iter is a record iterator
    Return both:
     - items (tuple, support)
    """
    itemSet, transactionList = getItemSetTransactionList(data_iter)

    freqSet = defaultdict(int)
    largeSet = dict()
    # Global dictionary which stores (key=n-itemSets,value=support)
    # which satisfy minSupport

    oneCSet= returnItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet)
    
    currentLSet = oneCSet
    k = 2
    iteration = 1
    while currentLSet != set([]):    
        largeSet[k - 1] = currentLSet
        currentLSet = joinSet(currentLSet, k)
        
        currentCSet= returnItemsWithMinSupport(
            currentLSet, transactionList, minSupport, freqSet
        )
        print(currentCSet)
        

        currentLSet = currentCSet
        
        k = k + 1
        iteration += 1

    def getSupport(item):
        """local function which Returns the support of an item"""
        return float(freqSet[item]) / len(transactionList)

    toRetItems = []
    for key, value in largeSet.items():
        
        toRetItems.extend([(tuple(item), getSupport(item)) for item in value]) # the list with all frequent itemsets
        
    for x, y in toRetItems:
        targetSet = set(x)
        freq = y
        isClosedfq = True
        for p, q in toRetItems:
            compareSet = set(p)
            comparingfreq = q
            if targetSet == compareSet:
                continue
            if  isImmediateSuperSet(targetSet, compareSet): # if is immediate superset
                if comparingfreq == freq: #and the frequent is the same, means it is not a closed frequent set
                    isClosedfq = False # set it to false
                    break
        if not isClosedfq: # kick the itemset which is not closed
            toRetItems.Remove(x)
    return toRetItems

def isImmediateSuperSet(smallSet, largeSet): # is immediate super set or not
    if largeSet.issuperset(smallSet):
        if len(largeSet) - len(smallSet) == 1:
            return True
    return False

def printResults(items, minSu, thefile):
    """prints the generated itemsets sorted by support """
    f1= open("step2_task2_%s_%.1f_result1.txt"%(thefile, minSu), "w+")
    cnt = 0

    for item, support in sorted(items, key=lambda x: x[1]):
        # print("item: %s , %.3f" % (str(item), support))
        f1.write("%.1f\t%s\n" % (support*100, str(item)))
        cnt+=1
    
    return cnt


def to_str_results(items):
    """prints the generated itemsets sorted by support"""
    i = []
    for item, support in sorted(items, key=lambda x: x[1]):
        x = "item: %s , %.3f" % (str(item), support)
        i.append(x)
    return i


def dataFromFile(fname):
    """Function which reads from the file and yields a generator"""
    with open(fname, "r") as file_iter:
        for line in file_iter:
            line = line.strip().rstrip(",")  # Remove trailing comma
            record = frozenset(line.split(",")[3:])
            
            yield record
# /home/ycwangtch/ssd1/111fall/111fall_data_mining/lab1

if __name__ == "__main__":
    start_time = time.time()
    optparser = OptionParser()
    optparser.add_option(
        "-f", "--inputFile", dest="input", help="filename containing csv", default='A.csv'
    )
    optparser.add_option(
        "-s",
        "--minSupport",
        dest="minS",
        help="minimum support value",
        default=0.1,
        type="float",
    )
    
    (options, args) = optparser.parse_args()

    inFile = None
    if options.input is None:
        inFile = sys.stdin
    elif options.input is not None:
        inFile = dataFromFile(options.input)
    else:
        print("No dataset filename specified, system with exit\n")
        sys.exit("System will exit")

    minSupport = options.minS
    minSu = options.minS*100
    thefile = options.input

    items = runApriori(inFile, minSupport)
    
    cnt = printResults(items, minSu, thefile) # total items
    total_time= time.time() - start_time # total computation time
    
    
    print("The total computation time is :",total_time, " seconds")