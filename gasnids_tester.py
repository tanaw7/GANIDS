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
#fileName = 'w1_mon.list' # Training datasets file
#fileName = 'w1_tue.list'
#fileName = 'w1_wed.list'
#fileName = 'w1_wednesday.list'
#fileName = 'w1_thu.list'
#fileName = 'w1_fri.list'
#fileName = 'mixed.list'
#fileName = 'mixed_all.list' 
#fileName = 'tcpdump.list'
#fileName = 'w7_tcpdump.list'
#fileName = 'pscan.list'
#fileName = 'bsm.list'
fileName = 'rules.rcd'

n_inds = 15 # Number of genes in each individual [shd not be modified]
n_pop = 8000 #400# Number of individuals in the whole population

if n_pop > 800:         # elites per attack type chosen for next gen
    elitesNo = n_pop/20#n_pop/100#10
else:
    elitesNo = n_pop/100#n_pop/100 
#CrossoverRate,individualMutationRate,GeneMutationRate,generationsToRun
CXPB, enterMutation, MUTPB, NGEN = 0.9, 1, 0.1, 400#400

wildcardWeight = 0.9#0.8#0.9 #chance that a gene initialized is a wildcard
wcw_switching = False
wcw_a = 0.4
wcw_b = 0.9
wcw_swapGen = 10

weightSupport, weightConfidence = 0.2,0.8#0.2, 0.8

wildcardPenalty = True #only apply in loop to increase variety of good results
wildcardPenaltyWeight = 0.000000000001#0.00000001#0.000001#
wildcard_allowance = 0 # 1 to 15 #currently not in used nor implemented yet

Result_numbers = n_pop#800 #800 #30
show_stats = True
show_elites = True

mutateElitesWildcards = True     #mutate elites genes when there are wildcards
mutateElitesWildcards_PB = 1 #result: better fitness
                               #good combination when wildcardWeight is high

baseWeaklings = n_pop/100 #with high wildcardWeight, it ensure the chance of finding
                   #the maximum fitness much faster

#------------------------------------------------------

# I ------Read DARPA audit files---*done*try put this in individuals--
auditData = []
rules = []

for line in fileinput.input([fileName]):
    line = line.rstrip('\r\n') # strip off the newline of each record
    if len(line) > 0:
        array = line.split(" ")
        rules.append(array)
# Now array looks like this
#['1', '01/23/1998', '16:56:48', '00:01:26', 'telnet', '1754', '23',
# '192.168.1.30', '192.168.0.20', '0', '-']

# Below we reconstruct the audit data to have chromosome-like structure.
"""
        line = []
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
"""