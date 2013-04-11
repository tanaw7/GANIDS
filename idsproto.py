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
n_inds = 15 # Number of genes in each chromosome
n_pop  = 500 # Number of chromosomes in each genome
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
#      '192.168.1.30', '192.168.0.20', '0', '-']

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

# unique ports should be taken from the input auditData[] list
uniq_srcporttest = [ 22, 1023, 44, 550, 8080, -1] # example (-1 is a wildcard)
uniq_srcporttest[random.randint(0, len(uniq_srcporttest)-1)]
## the above would give these ports equal chance to be picked

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

#for i in uniq_all: #--- decide if we should add -1 to the uniq(s)
#    i.insert(0, -1)#--- or should we add it in the generator function


#END II----------------------------------------------------------------

#-III -----Generate population: Build randomizor for each field in a 
#-chromosome--------------------------------------------------------

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
# Attribute generator
toolbox.register("attr_bool", random.randint, 0, 1)

#---randomizor

#import bisect #moved to top

weight = {-1:0.1,21:0.45,22:0.45}
items = weight.keys()
mysum = 0
breakpoints = [] 
for i in items:
    mysum += weight[i]
    breakpoints.append(mysum)

def getitem(breakpoints,items):
    score = random.random() * breakpoints[-1]
    i = bisect.bisect(breakpoints, score)
    return items[i]

for i, j in enumerate(uniq_all):
    weight = {-1:0.1}
    for u in uniq_all[i]:
        weight[u] = 0.9/len(uniq_all[i])

    items = weight.keys()
    mysum = 0
    breakpoints = []
    for i in items:
        mysum += weight[i]
        breakpoints.append(mysum)

    print weight 
    print getitem(breakpoints,items)

#toolbox.register("attr_randomizor", )


# Structure initializers

toolbox.register("individual", tools.initRepeat, creator.Individual, 
    toolbox.attr_bool, n_inds)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

#-------Evaluation Functions---------------------------
# imported evalFuncs.py
#-------------------------------------------------------   

# Operator registering
toolbox.register("evaluate", evalhalf01)
toolbox.register("mate", tools.cxTwoPoints)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

def main():
    #random.seed(64)
    
    pop = toolbox.population(n=n_pop)
    for i in pop:
      print pop.index(i), i


    CXPB, MUTPB, NGEN = 0.5, 0.2, 5000
    
    print("Start of evolution")
    
    # Evaluate the entire population
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
    
    print("  Evaluated %i individuals" % len(pop))
    
    # Begin the evolution
    for g in range(NGEN):
        print("-- Generation %i --" % g)
        
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))
    
        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values
    
        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        
        print("  Evaluated %i individuals" % len(invalid_ind))
        
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

        print("  genes %s" % n_inds)
        print("  chromosomes %s" % n_pop)
        print("  Min %s" % min(fits))
        print("  Max %s" % max(fits))
        print("  mxp %.3f %%" % mxp)
        print("  Avg %s" % mean)
        print("  Std %s" % std)

        if max(fits) == n_inds:
            break
    
    print("-- End of (as NGEN set) evolution --")
    
    best_ind = tools.selBest(pop, 1)[0]
    print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))

if __name__ == "__main__":
    main()

print "Took: ", time()-start_time, " seconds"