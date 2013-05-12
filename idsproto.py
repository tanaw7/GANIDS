"""
*  GANIDS (beta 0.9) - Genetic Algorithms for Deriving Network Intrusion Rules
*
*    Copyright (C) 2013 Tanapuch Wanwarang (Niklas) <nik.csec@gmail.com>
*
*                       http://nixorids.blogspot.com/
*
*    This program is free software: you can redistribute it and/or modify
*    it under the terms of the GNU General Public License as published by
*    the Free Software Foundation, either version 3 of the License, or
*    (at your option) any later version.
*
*    This program is distributed in the hope that it will be useful,
*    but WITHOUT ANY WARRANTY; without even the implied warranty of
*    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
*    GNU General Public License for more details.
*
*    You should have received a copy of the GNU General Public License
*    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

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
#fileName = 'mixed_pod_test.list'
#fileName = 'pscan.list'
fileName = 'bsm.list'

#for pod training
#fileName = 'w1_thu.list' 
#fileName = 'w4_mon.list'
#fileName = 'w4_tue.list'
#fileName = 'w4_wed.list' #done
#fileName = 'w5_tue.list'
#fileName = 'w5_thu.list' #uptil
#fileName = 'w6_tue.list'
#fileName = 'w6_thu.list'
#fileName = 'w7_tue.list'

#fileName = 'test_allpod.list'

#for nmap training
#fileName = 'w3_wed.list'
#fileName = 'w3_fri.list'

n_inds = 15 # Number of genes in each individual [shd not be modified]
n_pop = 4000 #400# Number of individuals in the whole population

if n_pop > 800:         # elites per attack type chosen for next gen
    elitesNo = n_pop/10#n_pop/100#10
else:
    elitesNo = n_pop/10#n_pop/100 
#CrossoverRate,individualMutationRate,GeneMutationRate,generationsToRun
CXPB, enterMutation, MUTPB, NGEN = 0.8, 1, 0.1, 200#400

wildcardWeight = 0.9#0.8#0.9 #chance that a gene initialized is a wildcard
wcw_switching = False
wcw_a = 0.4
wcw_b = 0.9
wcw_swapGen = 20

weightSupport, weightConfidence = 0.2,0.8#0.2, 0.8

wildcardPenalty = True #only apply in loop to increase variety of good results
wildcardPenaltyWeight = 0.000000000001#0.00000001#0.000001#
wildcard_allowance = 0 # 1 to 15 #currently not in used nor implemented yet

Result_numbers = n_pop#800 #800 #30
show_stats = True
show_elites = True
bestTopKnots = 10

#--Eliminator functions options
fitnessDiff_opt = True
fitnessDiff_value = 0.001
matchEliminate_opt = False
matchEliminate_AllowFields = 12 # in TopKnots filter

mutateElitesWildcards = True     #mutate elites genes when there are wildcards
mutateElitesWildcards_PB = 1 #result: better fitness
                               #good combination when wildcardWeight is high

baseWeaklings = n_pop/100 #with high wildcardWeight, it ensure the chance of finding
                   #the maximum fitness much faster

#------------------------------------------------------

# I ------Read DARPA audit files---*done*try put this in individuals--
auditData = []
#nosplit = []
for line in fileinput.input([fileName]):
    line = line.rstrip('\r\n') # strip off the newline of each record
    #nosplit.append(line)
    if len(line) > 0:
        line = re.sub(' +', ' ', line)
        array = line.split(" ")
# Now array looks like this
#['1', '01/23/1998', '16:56:48', '00:01:26', 'telnet', '1754', '23',
# '192.168.1.30', '192.168.0.20', '0', '-']

# Below we reconstruct the audit data to have chromosome-like structure.
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
            line.append(-1)
        #---Destination Port
        if array[6] != '-':
            line.append(int(array[6]))
        else:
            line.append(-1)
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

# return auditData #when put in a function

#END I--------------------------------------------------------------

# II -------find unique values in each field from audit data----
uniq_hour = set()
uniq_minute = set()
uniq_second = set()
uniq_protocol = set()
uniq_srcport = set()
uniq_desport = set()

uniq_srcip_1stoct = set()
uniq_srcip_2ndoct = set()
uniq_srcip_3rdoct = set()
uniq_srcip_4thoct = set()

uniq_desip_1stoct = set()
uniq_desip_2ndoct = set()
uniq_desip_3rdoct = set()
uniq_desip_4thoct = set()

uniq_attack = set()

for i in auditData:
    uniq_hour.add(i[0])
    uniq_minute.add(i[1])
    uniq_second.add(i[2])
    uniq_protocol.add(i[3])
    uniq_srcport.add(i[4])
    uniq_desport.add(i[5])
    uniq_srcip_1stoct.add(i[6])
    uniq_srcip_2ndoct.add(i[7])
    uniq_srcip_3rdoct.add(i[8])
    uniq_srcip_4thoct.add(i[9])
    uniq_desip_1stoct.add(i[10])
    uniq_desip_2ndoct.add(i[11])
    uniq_desip_3rdoct.add(i[12])
    uniq_desip_4thoct.add(i[13])
    #uniq_attack.add(i[14])
    if i[14] != '-':
        uniq_attack.add(i[14])

print uniq_attack

uniq_hour = list(uniq_hour)
uniq_minute = list(uniq_minute)
uniq_second = list(uniq_second)
uniq_protocol = list(uniq_protocol)
uniq_srcport = list(uniq_srcport)
uniq_desport = list(uniq_desport)
uniq_srcip_1stoct = list(uniq_srcip_1stoct)
uniq_srcip_2ndoct = list(uniq_srcip_2ndoct)
uniq_srcip_3rdoct = list(uniq_srcip_3rdoct)
uniq_srcip_4thoct = list(uniq_srcip_4thoct)
uniq_desip_1stoct = list(uniq_desip_1stoct)
uniq_desip_2ndoct = list(uniq_desip_2ndoct)
uniq_desip_3rdoct = list(uniq_desip_3rdoct)
uniq_desip_4thoct = list(uniq_desip_4thoct)
uniq_attack = list(uniq_attack)

uniq_all = [] # List containing all uniqe_values in all fields

uniq_all.append(uniq_hour)
uniq_all.append(uniq_minute)
uniq_all.append(uniq_second)
uniq_all.append(uniq_protocol)
uniq_all.append(uniq_srcport)
uniq_all.append(uniq_desport)
uniq_all.append(uniq_srcip_1stoct)
uniq_all.append(uniq_srcip_2ndoct)
uniq_all.append(uniq_srcip_3rdoct)
uniq_all.append(uniq_srcip_4thoct)
uniq_all.append(uniq_desip_1stoct)
uniq_all.append(uniq_desip_2ndoct)
uniq_all.append(uniq_desip_3rdoct)
uniq_all.append(uniq_desip_4thoct)
uniq_all.append(uniq_attack)

#return uniq_all #when put in a function

#END II----------------------------------------------------------------

#-III -----Generator, Generate population: Build randomizor
#-for each field in a chromosome---------------------------------------

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
# Attribute generator
toolbox.register("attr_bool", random.randint, 0, 1)

#---randomizor and chromosomizor

def randomizor(breakpoints,items):
    score = random.random() * breakpoints[-1]
    i = bisect.bisect(breakpoints, score)
    return items[i]

def chromosomizor(): #A function for building a chromosome.
    wcw = wildcardWeight
    an_individual = []
    for i, j in enumerate(uniq_all): # Using unique values from each field
        if i == (len(uniq_all)-1):
            wcw = 0.0 #we don't generate wildcard at attack field
        
        weight = {-1:wcw} #wcw
        for u in uniq_all[i]:
            #print len(uniq_all[i])
            # len()-1 because we don't need to count '-1' member
            if i == 14:
                weight[u] = (1 - wcw)/(len(uniq_all[i]))
            else:    
                weight[u] = (1 - wcw)/(len(uniq_all[i]))
        weight[-1] = wcw
        
        items = weight.keys()
        mysum = 0
        breakpoints = []
        for i in items:
            mysum += weight[i]
            breakpoints.append(mysum)

        #print weight
        an_individual.append(randomizor(breakpoints,items))

    return an_individual

def empty_chromosome():
    an_individual = []
    return an_individual

# Structure initializers
toolbox.register("attr_chromosomizor", chromosomizor)
toolbox.register("attr_empty_chromosome", empty_chromosome)
toolbox.register("individual", tools.initIterate,
                creator.Individual, toolbox.attr_chromosomizor)
toolbox.register("empty_individual", tools.initIterate,
                creator.Individual, toolbox.attr_empty_chromosome)

toolbox.register("population", tools.initRepeat,
                    list, toolbox.individual)

#END III -----------------------------------------------------------------

#-IV ------Evaluation Functions---------------------------
# imported evalFuncs.py

def evalSupCon(individual):
    Nconnect = float(len(auditData))
    matched_lines = 0.0
    wildcard = 0
    A = 0.0
    AnB = 0.0
    w1 = weightSupport #default 0.2
    w2 = weightConfidence #default 0.8
    for record in auditData:
        matched_fields = 0.0

        for index, field in enumerate(record, start=0):
            if (individual[index] == field) or (individual[index] == -1):
                matched_fields = matched_fields + 1.0
            if (individual[index] == -1):
                wildcard += 1
            if index == 13 and matched_fields == 14.0: 
                A += 1
            if index == 14 and matched_fields == 15.0:
                AnB += 1
                            #Wei Li's paper says that each field should have different
                            #Matching weight, I think it's true, this could be improved.
    #print 'A:', A,
    #print 'AnB:', AnB
    support = AnB / Nconnect
    if A > 0:
        confidence = AnB / A
    else:
        confidence = 0.0
    
    #print support
    #print confidence

    wildcard_deduct = wildcard * wildcardPenaltyWeight
    fitness = w1 * support + w2 * confidence

    if (wildcardPenalty == True) and (wildcard >= wildcard_allowance):
        if fitness > 0:
            fitness = fitness - wildcard_deduct

    if wildcard == 0 and fitness > 0:
        fitness = fitness - 0.001
    return fitness,
    #return [(fitness,), A, AnB]

#END IV -------------------------------------------------------

#-- V --- Selector (for elites) -------------------------------------
#Select 2 best individuals for each type of attack in generated old pop
#(So it select elites)
#len(uniq_attack) no. of attack types
#def selElites(pop):

attkUniqs = uniq_attack
#attkUniqs.remove('-')

def selElites(pop): #Selector function
    """ Needs **UPDATE**
The basic idea of this selector is to:
1. Accept the generated individuals
2. Categorize individuals into different attack type lists
3. Then append them back together to pass on as elites
for the next generation.
"""
    attkTypes = len(attkUniqs) # 4, Numbers of attacks in integer
    attkPop = []
    elitesSub = []
    elitesAll = []

    for i in xrange(attkTypes): #create lists within the attkPop list
        attkPop.append([]) #equals to the number of attkTypes

    for i in xrange(attkTypes):
        for j, k in enumerate(pop):
            if k[-1] == attkUniqs[i]: #if last field is the same attack
                attkPop[i].append(k) #type then add to the attkPop

    for i in attkPop:
        elitesSub.append(tools.selBest(i, elitesNo))


    for i in elitesSub: #appending all elites to elitesAll list
        i = list(i for i,_ in itertools.groupby(i)) #eliminate duplicate elites by attk type
        for j in i:
            elitesAll.append(j)

    #for i in elitesAll:
    #    i = list(i for i,_ in itertools.groupby(i))

    return elitesAll #This will be returned to create part of new
                     #population

###For main selector we uses deap default tools.selRandom

#END V ---------------------------------------------------------

#-- VI Crossover operator---------------------------------------
# Uses deap default tools.cxTwoPoints
#END VI---------------------------------------------------------

#-- VII Mutation operator---------------------------------------
unique_all_app = copy.deepcopy(uniq_all)
for i, field in enumerate(unique_all_app):
    if i != 14:
        field.append(-1)

def mutator(individaul):
    mutant = toolbox.empty_individual()
    for i, field in enumerate(individaul):
        unique_types = unique_all_app
        if random.random() < MUTPB:
            #print field, unique_types[i], "\n",
            #remove original value from pool
            #unique_types[i].remove(field)  
            field = random.choice(unique_types[i])
            #print field, unique_types[i],
        mutant.append(field)
    return mutant

def mutateWcardGene(individaul): #use to mutate wildcard genes of elites
    mutant = toolbox.clone(individaul)
    for i, field in enumerate(mutant):
        unique_types = uniq_all
        #print unique_types
        if (field == -1) and (random.random() < mutateElitesWildcards_PB):# and i != 3 and i != 4:
            mutant[i] = random.choice(unique_types[i])
            del mutant.fitness.values
            break
        del mutant.fitness.values
    return mutant

def mutateWcardGene_rand(individaul):
    mutant = toolbox.clone(individaul)
    wcard_field = []
    for i, field in enumerate(mutant):
        unique_types = uniq_all
        if (field == -1):
            wcard_field.append(i)
    #print wcard_field
    if random.random() < mutateElitesWildcards_PB and len(wcard_field) != 0:
        idx = random.choice(wcard_field)
        mutant[idx] = random.choice(unique_types[idx])
        del mutant.fitness.values
    #print mutant
    return mutant

def matchEliminate(ace, indi): #move function to elsewhere later

    matched_fields = 0
    for index, field in enumerate(indi, start=0):
        if (ace[index] == field):
            matched_fields = matched_fields + 1

    return (matched_fields >= matchEliminate_AllowFields)

#---------------------------------------------------------------

# Operator registering
toolbox.register("evaluate", evalSupCon) #Support-Confidence
toolbox.register("mate", tools.cxTwoPoints) #cxTwoPoints should work
toolbox.register("mutate", mutator)
toolbox.register("selectE", selElites) #this is not main selection
                                      #it is only elites selection

#toolbox.register("select", SOMENAME) #main selector needed
toolbox.register("select", tools.selRandom)

#del later
popza = toolbox.population(n=200)
indy = popza[0]

#---del later, this was simulated to gain understanding
# more of map(), zip()
#ass = selElites(popza)
fitneys = list(map(toolbox.evaluate, popza))
print fitneys[0]
print i
#for i, (k, j) in enumerate(zip(popza, (fitneys[i][0],))):
for k, j in zip(popza, fitneys):
    k.fitness.values = j

#w1,w2 = toolbox.empty_individual(), toolbox.empty_individual()
#for i in range(15):
#    w1.append(-1)
#    w2.append(-1)


def main():
    #random.seed(12) #uncommet this for testing
    pop = toolbox.population(n=n_pop) #CREATE POPULATION
    #for i in pop: #prints initial population
    # print pop.index(i)+1, i
    
    print("Start of evolution")
    
    # Evaluate the entire population
    fitnesses = list(map(toolbox.evaluate, pop)) #THIS LINE MUST BE UNDERSTOOD
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    #for i in pop:
    #    print i.fitness.values,

    print " "
    print(" Evaluated %i individuals" % len(pop))
    
    # Begin the evolution
    round_gen = 0
    for g in range(NGEN):
        try:
            k = g+1
            round_gen += 1

            global wildcardWeight
            if wcw_switching == True:
                if g%wcw_swapGen == 0:
                    wildcardWeight = wcw_b
                else:
                    wildcardWeight = wcw_a
            
            #print wildcardWeight

            # Initialize new population
            offspring = []
            
            # Select the next generation individuals
            elites = toolbox.selectE(pop) # select elites for next gen
            #if show_elites == True:
            #    for idx, i in enumerate(elites):
            #        print "%3d" % idx, "fv: %.6f" % i.fitness.values, i
            

            offspring = toolbox.select(pop, len(pop))
            # Clone the selected individuals
            offspring = list(map(toolbox.clone, offspring))

            # Apply crossover on the offspring individuals
            # first we shuffle list members positions.
            # Then we mate every two members next to one another
            random.shuffle(offspring)
            random.shuffle(offspring) 
            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < CXPB:
                    toolbox.mate(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values

            # Apply mutation on the offsping individuals
            for idx, individual in enumerate(offspring):
                if random.random() < enterMutation: # no need bcuz MUTPB in def
                    mutor = toolbox.clone(individual)
                    #print dir(mutor)
                    #print "##IND##", individual
                    mutor = toolbox.mutate(individual)
                    #print "##MUT##", mutor
                    del mutor.fitness.values
                    offspring[idx] = mutor

        #mutant = toolbox.clone(ind1)
        #ind2, = tools.mutGaussian(mutant, mu=0.0, sigma=0.2, indpb=0.2)
        #del mutant.fitness.values

    #-- VIII -- Optimizers --------------------------------------------------------

            supremes = []
            
            for i in uniq_attack:
                space = []
                jail = []
                #topgun = toolbox.empty_individual()
                for j in elites:
                    if j[-1] == i:
                        space.append(j)
                #space.sort()
                global ace
                ace = tools.selBest(space, 1)
                ace = ace[0] #THE BEST ONE of that attack type

                if fitnessDiff_opt == True:

                    for idx, ind in enumerate(space):            #it works now using jail[]
                    #    print idx ,ind.fitness.values, ind
                    #    print (ace.fitness.values[0] - ind.fitness.values[0]) <= fitnessDiff_value
                        if (((ace.fitness.values[0] - ind.fitness.values[0]) <= fitnessDiff_value) and (idx > 0)):
                            jail.append(ind)
                    #        print 1

                    for ind in jail:
                        space.remove(ind)


                if matchEliminate_opt == True:
                    jail = []
                    for idx, ind in enumerate(space):
                        if matchEliminate(ace, ind) and ind != ace:
                            jail.append(ind)

                    for ind in jail:
                        space.remove(ind)

                #space = tools.selBest(space, bestTopKnots)
                for i in space:
                    supremes.append(i)

            elites = supremes
#--------

        #    print "###", len(offspring)
            for i in elites:
                offspring.append(i)

            mutatedElites = 0

            if mutateElitesWildcards == True:
                
                for i in elites:
                    #print i
                    mutant = mutateWcardGene_rand(i)
                    if mutant != i:
                        mutatedElites += 1
                        #print mutant
                        offspring.append(mutant)
                        #print offspring[-1]

        #    print "###", len(offspring)

            weaklings = tools.selWorst(offspring, (baseWeaklings + len(elites) + mutatedElites))
            for i in weaklings:
                offspring.remove(i)

            #This could be used in the same way to eliminate individuals like weaklings but..
            #offspring = list(offspring for offspring,_ in itertools.groupby(offspring))

            n_lost = n_pop - len(offspring) #No. of individuals lost due to 
            for i in range(n_lost):         #duplication or weaklings weeded out
                new_ind = toolbox.individual()
                #print new_ind
                offspring.append(new_ind)   #we replace them

            # Evaluate the individuals with an invalid fitness
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = map(toolbox.evaluate, invalid_ind)
            #for i, (k, j) in enumerate(zip(popza, (fitneys[i][0],))):
            
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit


            
            
            #remove dulicates in offspring (not practical unless new indvs added)
            #offspring = list(offspring for offspring,_ in itertools.groupby(offspring))

    #- End VIII ---------------------------------------------------------------------

            # The population is entirely replaced by the offspring
            random.shuffle(offspring)
            pop[:] = offspring

    #-- IX --- Statistics and Each loop Outputs -------------------------------------

            # Gather all the fitnesses in one list and print the stats
            if show_stats == True:
                print("-- Generation %i --" % k)
                print(" Evaluated %i individuals" % len(invalid_ind))
                fits = [ind.fitness.values[0] for ind in pop]
                
                length = len(pop)
                mean = sum(fits) / length
                sum2 = sum(x*x for x in fits)
                std = abs(sum2 / length - mean**2)**0.5
                #mx = float(max(fits))
                #mxp = (mx*100) / n_inds

                print(" individuals: %s" % len(pop))
                print(" weaklings: %s" % len(weaklings))
                print(" elites: %s" % len(elites))
                print(" Mutated Elites: %s" % mutatedElites)
                print(" Audit data: %s lines" % len(auditData))
                #print(" Min %s" % min(fits))
                print(" Max %s" % max(fits))
                #print(" mxp %.3f %%" % mxp)
                print(" Avg %s" % mean)
                print(" Std %s \n" % std)
                if show_elites == True and elitesNo >= 6:
                    bestElites = tools.selBest(elites,20)
                    for idx, i in enumerate(bestElites):
                        print "%3d" % idx, "fv: %.14f" % i.fitness.values, i
                elif show_elites == True:
                    for idx, i in enumerate(elites):
                        print "%3d" % idx, "fv: %.14f" % i.fitness.values, i            
                print("------End Generation %s" % k)
                print "\n"
            #print fitnesses

        except KeyboardInterrupt:
            print "You hit Crt-C to prematurely exit the loop"
            break

    
#- End IX -------------------------------------------------------------------------

# for i in pop: #prints initial population
# print pop.index(i)+1, "fv=%s" % i.fitness.values, i

        #if max(fits) >= 0.8063:
        # break
    
# print("-- End of (as NGEN set) evolution --")
    #for ind in pop:
    #    del ind.fitness.values

    global wildcardPenalty
    #wildcardPenalty = False
    wildcardPenalty = True

    fitnesses = list(map(toolbox.evaluate, pop)) #re-evaluate fitness without wildcard penalty
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit  

    print "Best individuals are: " #% (best_ind, best_ind.fitness.values))
    bestInds = tools.selBest(pop, Result_numbers)

    for i, j in enumerate(bestInds):
        print "%3d" % i, "fv: %.14f" % j.fitness.values, j

    print "\n\n"
    #Remove duplicate individuals from the results
    #bestInds.sort()
    bestInds = tools.selBest(bestInds, len(bestInds))
    bestInds = list(bestInds for bestInds,_ in itertools.groupby(bestInds))
    print "Best individuals (duplications removed) are: "
    for i, j in enumerate(bestInds):
        print "%3d" % i, "fv: %.14f" % j.fitness.values, j

    #Show Best individuals by attack types
    bestAttkTypes = toolbox.selectE(bestInds)
    print "\n\n"
    print "Best individuals by attack types are: "
    for i, j in enumerate(bestAttkTypes):
        if j.fitness.values[0] > 0.0:
            print "%9s" % j[14][0:16], "%3d" % i, "fv: %.14f" % j.fitness.values, j
            #print "%3d" % i, "fv: %.14f" % j.fitness.values, j

    #topknots = bestAttkTypes #comment if topknot filter is used.
    
# TOPKNOTS Filter -------------------------------------------------------------------
    #uniq_attack
    topknots = []
    
    for i in uniq_attack:
        space = []
        jail = []
        for j in bestAttkTypes:
            if j[-1] == i:
                space.append(j)
        #space.sort()
        global topgun
        topgun = tools.selBest(space, 1)
        topgun = topgun[0] #THE BEST ONE of that attack type

        #print "\n\nBEFORE SPACE: "
        #for idx, i in enumerate(space):
        #    print idx, i.fitness.values, i

        #print "topgun of %s: " % topgun[-1], topgun
        #for idx, ind in enumerate(space):            #it works now using jail[]
        #    print idx ,ind.fitness.values, ind
        #    print (topgun.fitness.values[0] - ind.fitness.values[0]) <= 0.001
        #    if (((topgun.fitness.values[0] - ind.fitness.values[0]) <= 0.001) and (idx > 0)):
        #        jail.append(ind)
        #        print 1

        #for ind in jail:
        #    space.remove(ind)


        #jail = []
        #for idx, ind in enumerate(space):
        #    if matchEliminate(topgun, ind) and ind != topgun:
        #        jail.append(ind)

        #for ind in jail:
        #    space.remove(ind)


        #print "AFTER SPACE: "
        #for idx, i in enumerate(space):
        #    print idx, i.fitness.values, i

        space = tools.selBest(space, bestTopKnots)
        for i in space:
            topknots.append(i)
        
    print "\n\n"
    print "topknots individuals are: "
    for i, j in enumerate(topknots):
        if j.fitness.values[0] > 0.7:
            print "%9s" % j[14][0:16], "%3d" % i, "fv: %.14f" % j.fitness.values, j

 
# END TopKnots -------------------------------------------------------------------------------

    print "We ran", round_gen, "rounds"

    #Write result to rulesDump.rcd file
    rules = []
    rulesDumpFile = open('rulesDump.rcd', 'w+')
    for item in topknots:
        line = ""
        if item.fitness.values[0] > 0.7:
            for i in item:
                line = line.__add__(str(i) + ' ')
            
            rules.append(line)

    for idx, item in enumerate(rules):
        item = str(idx+1) + " " + item
        rulesDumpFile.write("%s\n" % item)
    rulesDumpFile.close()

if __name__ == "__main__":
    main()

print "Took: ", time()-start_time, " seconds"