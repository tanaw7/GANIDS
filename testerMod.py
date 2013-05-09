import random           #for most of the things done here
import fileinput        #for reading an audit dataset
import bisect           #for mapping different weights for members in a list
import itertools        #for eliminating duplicate lists in a list
import re               #for multiple delimiters in dataset files
import copy             #for making an unshared copy
from time import time   #for counting the amount of time GANIDS runs


from deap import base
from deap import creator
from deap import tools

start_time = time()

#--CONTROL PANEL---------------------------------------
#------Modifiable variables (notable ones)----------------

#fileRules = 'rules.rcd'
#fileRules = 'rules_podfrTest.rcd'
fileRules = 'rules_pod.rcd'

#fileTest = 'test_w1mon.list'
fileTest = 'w1_alltruth.list'
#fileTest = 'w2_alltruth.list'
#fileTest = 'wm_alltruth.list'
#fileTest = 'test_pod207.list'
#------------------------------------------------------

auditData = []
rules = []

# I ---Read Rules Files-------------------------------------
for i, line in enumerate(fileinput.input([fileRules])):
    line = line.rstrip('\r\n') # strip off the newline of each record
    if len(line) > 0:
        line = re.sub(' +', ' ', line)
        array = line.split(" ") # returns a list containing each item in the record
        del array[-1]
        for idx, item in enumerate(array):
            if idx != 4 and idx != 15 or item == '-1':
                array[idx] = int(item) 
        rules.append(array)

for i in rules:
    print i
# END I -----------------------------------------------------


# II ---Read test audit data file ---------------------------
auditData = []
#nosplit = []
for line in fileinput.input([fileTest]):
    line = line.rstrip('\r\n') # strip off the newline of each record
    #nosplit.append(line)
    if len(line) > 0:
        line = re.sub(' +', ' ', line)
        array = line.split(" ")

        line = []
        #---identifier
        line.append(int(array[0])+1)

        #---Duration
        line.append(int(array[3][0:2])) #append hour as gene into chromosome
        line.append(int(array[3][3:5])) #append minute
        line.append(int(array[3][6:8])) #append second
        #---Protocal
        line.append(array[4])
        #---Source Port
        if array[5] != '-':
            line.append(int(array[5]))
        else:
            line.append(0)
        #---Destination Port
        if array[6] != '-':
            line.append(int(array[6]))
        else:
            line.append(0)
        #---Source IP
        ip = array[7].split(".")
        line.append(int(ip[0])) #1st octet
        line.append(int(ip[1])) #2nd octet
        line.append(int(ip[2])) #3rd octet
        line.append(int(ip[3])) #4th octet
        #---Destination IP
        ip = array[8].split(".")
        line.append(int(ip[0])) #1st octet
        line.append(int(ip[1])) #2nd octet
        line.append(int(ip[2])) #3rd octet
        line.append(int(ip[3])) #4th octet
        #---Attack type
        line.append(array[10])

    auditData.append(line)

#for i, j in enumerate(auditData):
#    print i, j

# END II --------------------------------------------------------------


# III -----------------------Match function----------------------------

match_cc = 0
match_at = 0
rule_no = 0
def testMatch(rule):
    global match_cc
    global match_at
    global rule_no

    rule_no += 1

    #Nconnect = float(len(auditData))
    matched_lines = 0
    wildcard = 0
    matchConn = 0
    matchAttk = 0
    match_list = []

    for record in auditData:
        matched_fields = 0
        for index, field in enumerate(record, start=0):
            if ((rule[index] == field) or (rule[index] == -1)) and index != 0:
                matched_fields = matched_fields + 1
                #print matched_fields
            #if (rule[index] == -1): #may not need
            #    wildcard += 1
            if index == 14 and matched_fields == 14: 
                matchConn += 1
                match_cc += 1
                #print "Matched Connection"
                #print match_cc
                match_list.append(record)
                #print "rule: ", rule
                #print "audit:", record
            if index == 14 and matched_fields == 15:
                matchAttk += 1
                match_at += 1
                #print "Matched Attack"
                #print match_at

    if len(match_list) > 0:
        print "\n"
        print "-@ rule %s -@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@" % rule_no
        print rule
        
        print "Matched Connections below: "
        for i in match_list:
            print i
        print "Matched Connections No:", matchConn
    
    return "haha"

# END III ----------------------------------------------------------------------------

#print len(rules)
#print len(auditData)

for i, j in enumerate(rules):
    #print "rule No.:", i 
    testMatch(j)



