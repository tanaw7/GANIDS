from gafunc import *


def main():
    #random.seed(12) #uncommet this for testing
    pop = toolbox.population(n=n_pop) #CREATE POPULATION

    print("Start of evolution")
    
    # Evaluate the entire population
    fitnesses = list(map(toolbox.evaluate, pop)) #THIS LINE MUST BE UNDERSTOOD
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

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

            # Initialize new population
            offspring = []
            
            # Select the next generation individuals
            elites = toolbox.selectE(pop) # select elites for next gen

            offspring = toolbox.select(pop, int(len(pop)/sel_divisor))#len(pop))
            #print "LEN OFFFFF", len(offspring)
            # Clone the selected individuals
            offspring = list(map(toolbox.clone, offspring))

            # Apply crossover on the offspring individuals
            # first we shuffle list members positions.
            # Then we mate every two members next to one another
            random.shuffle(offspring) 
            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < CXPB:
                    toolbox.mate(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values

            # Apply mutation on the offsping individuals
            for idx, individual in enumerate(offspring):
                if random.random() < enterMutation: # no need bcuz MUTPB in def
                    mutor = toolbox.clone(individual) #variable initilization
                    mutor = toolbox.mutate(mutor)
                    #print "##MUT##", mutor
                    del mutor.fitness.values
                    offspring[idx] = mutor

            #invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            #fitnesses = map(toolbox.evaluate, invalid_ind)

    #-- VIII -- Optimizers --------------------------------------------------------


            
            #-- Ace Comparison
            elites = aceComparison(elites)

            for i in elites:
                offspring.append(i)

            mutatedElites = 0
            if mutateElitesWildcards == True:
                
                for ind in elites:
                    mutant = mutateWcardGene_rand(ind)
                    if mutant != ind:
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

    
#- End IX : Ends main()----------------------------------------------------------

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
        
        global topgun
        topgun = tools.selBest(space, 1)
        topgun = topgun[0] #THE BEST ONE of that attack type

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