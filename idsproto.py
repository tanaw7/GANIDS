import random
import fileinput
import bisect
from time import time
from evalFuncs import *

from deap import base
from deap import creator
from deap import tools

start_time = time()

#------Modifiable values (notable ones)----------------
n_inds = 15 # Number of genes in each individual [shd not be modified]
n_pop = 1000 # Number of individuals in the whole population
#------------------------------------------------------

# I ------Read DARPA audit files---*done*try put this in individuals--
auditData = []
nosplit = []
for line in fileinput.input(['bsm.list']):
    line = line.rstrip('\r\n') # strip off the newline of each record
    nosplit.append(line)
    if len(line) > 0:
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
        line.append(int(array[5]))
        #---Destination Port
        line.append(int(array[6]))
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
    if i[14] != '-':
        uniq_attack.add(i[14])

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
#uniq_attack.remove('-')

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
    an_individual = []
    for i, j in enumerate(uniq_all): # Using unique values from each field
        wildcardWeight = 0.1 #chance that a gene generated is a wildcard
        weight = {-1:wildcardWeight}
        for u in uniq_all[i]:
            weight[u] = (1 - wildcardWeight)/len(uniq_all[i])

        items = weight.keys()
        mysum = 0
        breakpoints = []
        for i in items:
            mysum += weight[i]
            breakpoints.append(mysum)

        #print weight
        an_individual.append(randomizor(breakpoints,items))

    return an_individual

# Structure initializers
toolbox.register("attr_chromosomizor", chromosomizor)
toolbox.register("individual", tools.initIterate,
                creator.Individual, toolbox.attr_chromosomizor)

toolbox.register("population", tools.initRepeat,
                    list, toolbox.individual)

#END III -----------------------------------------------------------------

#-IV ------Evaluation Functions---------------------------
# imported evalFuncs.py

def evalSupCon(individual):
    Nconnect = len(auditData)
    matched_lines = 0.0
    wildcard = 0
    A = 0.0
    AnB = 0.0
    w1 = 0.2
    w2 = 0.8
    for line in auditData:
        matched_fields = 0.0

        for index, field in enumerate(line, start=0):
            if (individual[index] == field) or (individual[index] == -1):
                matched_fields = matched_fields + 1.0
            if (individual[index] == -1):
                wildcard += 1
        if matched_fields >= 14.0:
            A += 1
        if matched_fields == 15.0:
            AnB += 1
        #if matched_fields == 15.0:
        # matched_lines = matched_lines + 1.0
        # #print line

    #print 'A:', A
    #print 'AnB:', AnB
    support = AnB / Nconnect
    if A > 0:
        confidence = AnB / A
    else:
        confidence = 0.0
    wildcard_deduct = wildcard * 0.001
    fitness = w1 * support + w2 * confidence
    #if fitness >= 0:
    #    fitness = fitness - wildcard_deduct
    
    return fitness,

#END IV -------------------------------------------------------

#-- V --- Selector -------------------------------------
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
3. Evaluate individuals in each list and pick the best two
as elites of that attack types
4. Then append them back together to pass on as elites
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
        elitesSub.append(tools.selBest(i, 2))

    for i in elitesSub: #appending all elites to elitesAll list
        for j in i:
            elitesAll.append(j)

    return elitesAll #This will be returned to create part of new
                     #population

#def selRandiBestj(pop, random_ind, fittest_ind):

# return 0

#---------------------------------------------------------------

# Operator registering
toolbox.register("evaluate", evalSupCon) #Support-Confidence
toolbox.register("mate", tools.cxTwoPoints) #cxTwoPoints should work
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
toolbox.register("selectE", selElites) #this is not main selection
                                      #it is only elites selection

#toolbox.register("select", SOMENAME) #main selector needed
toolbox.register("select", tools.selRandom)

#del later
popza = toolbox.population(n=200)

#---del later, this was simulated to gain understanding
# more of map(), zip()
#ass = selElites(popza)
fitneys = list(map(toolbox.evaluate, popza))
for k, j in zip(popza, fitneys):
    k.fitness.values = j


def selRandiBestj(pop, x, y):
    """
Select randomly x individuals,
choose y best individuals from them.
(x must be greater than y)
"""

    remPop = tools.selBest(selRandom(pop, x), y)

    return remPop



def main():
    #random.seed(64)
    pop = toolbox.population(n=n_pop) #CREATE POPULATION
    #for i in pop: #prints initial population
    # print pop.index(i)+1, i

    CXPB, MUTPB, NGEN = 1.0, 0.2, 100 #CXPB to be 1.0 if eval all
    
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

        k = g+1
        round_gen += 1
        print("-- Generation %i --" % k)

        # Initialize new population
        offspring = []
        
        # Select the next generation individuals
        elites = toolbox.selectE(pop) # select elites for next gen
        for i in elites:
            print i, i.fitness.values
        for i in elites:
            offspring.append(i) #add elites to the next gen
            #pop.remove(i) #remove elites from current gen

        offspring = toolbox.select(pop, len(pop))
                                       #, len(pop)) amount select not used
        # Clone the selected individuals
        #for i in offspring:
        # print i.fitness.values, # i,
        offspring = list(map(toolbox.clone, offspring))
        #print "\n"
        #for i in offspring:
        # print i, i.fitness.values
    
        # Apply crossover and mutation on the offspring
        random.shuffle(offspring)
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

    #    print "###", len(offspring)
        for i in elites:
            offspring.append(i)
    #    print "###", len(offspring)


        #for mutant in offspring:
        # if random.random() < MUTPB:
        # toolbox.mutate(mutant)
        # del mutant.fitness.values
    
        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        
        weaklings = tools.selWorst(offspring, 10)
        for i in weaklings:
            offspring.remove(i)

        print(" Evaluated %i individuals" % len(invalid_ind))
        
        # The population is entirely replaced by the offspring
        pop[:] = offspring
        
        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]
        
        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x*x for x in fits)
        std = abs(sum2 / length - mean**2)**0.5
        mx = float(max(fits))
        mxp = (mx*100) / n_inds

        print(" genes %s" % n_inds)
        print(" individuals %s" % n_pop)
        print(" Min %s" % min(fits))
        print(" Max %s" % max(fits))
        print(" mxp %.3f %%" % mxp)
        print(" Avg %s" % mean)
# print(" Std %s" % std)
        #print fitnesses

# for i in pop: #prints initial population
# print pop.index(i)+1, "fv=%s" % i.fitness.values, i

        #if max(fits) >= 0.8063:
        # break
    
# print("-- End of (as NGEN set) evolution --")
    print round_gen, "rounds"
    best_ind = tools.selBest(pop, 1)[0]
    print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))
    best30 = tools.selBest(pop, 10)
    for i in best30:
        print i, i.fitness.values

if __name__ == "__main__":
    main()

print "Took: ", time()-start_time, " seconds"

"""
I now roughly understand the evolution process.
-first initialize, the output of the loop, the destination pop
(meaning create an empty list)
-then copy the elites over to the destination pop
-then begin the loop
*question is, wouldn't the elites become useless
*and unrealistic?
*since it doesn't really represent the likely evolutionary process
*it's like just copy the ones(likely with fitness of 0.0) to
*the final destination.

**UPDATE**
I have found online that Elitism exists to prevent the chance
of losing high-fitness value individuals that have been found
So elites should be reserved[2ofHighestAttack] some slots in the
next generation. Elitism should be a loop process as well.


Check page 18, and pseudo code on page 27 again
and its description on page 28-29 as well before
begin to code. for now good night!


"""

    #---del later, this was simulated to gain understanding
    # more of map(), zip()
    #ass = selElites(pop)
    #fitneys = list(map(toolbox.evaluate, ass))
    #for k, j in zip(ass, fitneys):
    # k.fitness.values = j

    #for i in ass:
    # print i.fitness.uniqe_values