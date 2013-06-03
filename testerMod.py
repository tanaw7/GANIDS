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
#fileRules = 'rules_portsweep.rcd'
#fileRules = 'rules_neptune.rcd'
#fileRules = 'rules_teardrop.rcd'

#fileTest = 'test_w1mon.list'
#fileTest = 'w1_alltruth.list'
#fileTest = 'w2_alltruth.list'
fileTest = 'wm_alltruth.list'
#fileTest = 'test_w1_mon_truth.list' #pod
#fileTest = 'test_w1_tue_truth.list'
#fileTest = 'test_w1_wed_truth.list'
#fileTest = 'test_w1_thu_truth.list' #pod
#fileTest = 'test_w1_fri_truth.list'

#fileTest = 'test_pod207.list'

attackType = 'pod'
#attackType = 'portsweep'
#attackType = 'neptune'
#attackType = 'teardrop'
attackType_strLength = len(attackType)

attkInTestFile = 0.0
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

print "Rules from the training module:"
for i in rules:
    print i
# END I -----------------------------------------------------


# II ---Read test audit data file ---------------------------

print "** Loading test audit data, please be patient **"
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
        line.append(int(array[0]))

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
        if array[10][0:attackType_strLength] == attackType:
            attkInTestFile += 1

    auditData.append(line)

print "** Done loading test audit data **"
#for i, j in enumerate(auditData):
#    print i, j

# END II --------------------------------------------------------------


# III -----------------------Match function----------------------------


match_cc = 0
match_at = 0
rule_no = 0
def testMatchRule(rule): #input is a rule against data records
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

    #for record in auditData:
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

alerts = []

def testMatchData(dataRecord): #input is a test data record against rules
    global match_cc
    global match_at
    global rule_no

    rule_no += 1

    #Nconnect = float(len(auditData))
    matched_lines = 0
    matchRules = 0
    match_list = []

    #for record in auditData:
    for record in rules:
        matched_fields = 0
        for index, field in enumerate(record, start=0):
            if ((dataRecord[index] == field) or (record[index] == -1)) and index != 0:
                matched_fields = matched_fields + 1
                #print matched_fields
            #if (rule[index] == -1): #may not need
            #    wildcard += 1
            if index == 14 and matched_fields == 14: 
                matchRules += 1
                match_cc += 1
                #print "Matched Rules"
                #print match_cc
                match_list.append(record)

    if len(match_list) > 0:

        alerts.append(dataRecord)

        print "\n"
        print "-@ Test Data No. %s -@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@-@" % rule_no
        print dataRecord #[-1][0:3]
        
        print "Matched Rules below: "
        for i in match_list:
            print i
        print "Matched Rules No:", matchRules
    
    return "haha"

# END III ----------------------------------------------------------------------------

#print len(rules)
#print len(auditData)

#for i, j in enumerate(rules):
    #print "rule No.:", i 
#    testMatchRule(j)

print "\n\n\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#"
print "\nCommencing Test Module Simulation for %s attack\n" % attackType

for i, j in enumerate(auditData):
    #print "rule No.:", i 
    testMatchData(j)

falseAlert = 0
normalConnWrongIden = 0

print "\n\n\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#"
print "\nConnections flagged by false alerts: "
for i in alerts:
    if i[-1][0:attackType_strLength] != attackType:
        print i
        falseAlert += 1

print "\n\n\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#"
print "\nNormal Connections wrongly identified as attacks: "
for i in alerts:
    if i[-1] == '-':
        print i
        normalConnWrongIden += 1


if attkInTestFile > 0 :#and falseAlert > 0:

    testDataNo = len(auditData)
    normalConns = float(testDataNo - attkInTestFile)
    alerts_all = float(len(alerts))
    false_pos = float(falseAlert)
    true_pos = float(alerts_all - false_pos)
    false_neg = float(attkInTestFile - true_pos)
    true_neg = float(normalConns - falseAlert)

    accuracy = (true_pos + true_neg) / float(true_pos+false_pos+false_neg+true_neg)
    precision = true_pos / float(true_pos+false_pos)
    sensitivity = true_pos / float(true_pos+false_neg)
    specificity = true_neg / float(true_neg+false_pos)

    print "\n\n\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#"
    print true_pos, true_neg, false_pos, false_neg
    print "Summary of the simulation: \n"
    print "Attack Type: %s" % attackType
    print "Test Data records: %s\n" % testDataNo
    print "\nTotal Number of Attacks in Test Records: %s" % attkInTestFile
    print "All alerts: %s" % alerts_all
    print "L False Positive/False Alerts: %s, %.4f%%" % (false_pos, float(false_pos/testDataNo)*100)
    print "L False Negative/Undetected Attacks: %s, %.4f%% " % ( false_neg, float(false_neg/attkInTestFile)*100 )
    print "\nH True Positive/Detected Attacks: %s, %.4f%%" % (true_pos, float(true_pos/attkInTestFile)*100)
    print "H True Negative/Normal conn correctly identified: %s, %.4f%%" % ( true_neg, float(true_neg/normalConns)*100)

    print "\nMeasurements ----------------"
    print "accuracy: %s" % accuracy
    print "precision: %s" % precision
    print "sensitivity: %s" % sensitivity
    print "specificity: %s" % specificity
    print "\n\n"


elif attkInTestFile == 0 or falseAlert == 0: #needs fix

    alerts_all = float(len(alerts))
    false_pos = float(falseAlert)
    true_pos = float(alerts_all - false_pos)
    false_neg = (attkInTestFile - true_pos)    

    print "MEH!"
    print "\n\n\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#"
    print "Summary of the simulation: \n"
    print "There is no %s attack in this test file" % attackType
    print "Test Data records: %s\n" % len(auditData)
    print "\nTotal Number of Attacks in Test Records: %s" % attkInTestFile
    print "All alerts: %s" % alerts_all
    if alerts_all > 0:
        print "False Positive/False Alerts: %s, %.4f%%" % (false_pos, float(false_pos/alerts_all)*100)
    else:
        print "False Positive/False Alerts: %s, %.4f%%" % (0, 0)
    print "\nFalse Negative/Undetected Attacks: %s, %.4f%% " % (0, 0)
    print "True Positive/Detected Attacks: %s, %.4f%%\n\n" % (0, 0)


