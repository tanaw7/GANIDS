#--CONTROL PANEL---------------------------------------
#------Modifiable variables (notable ones)----------------

n_pop = 2000 #400# Number of individuals in the whole population

if n_pop > 800:         # elites per attack type chosen for next gen
    elitesNo = n_pop/10#n_pop/100#10
else:
    elitesNo = n_pop/10#n_pop/100 
#CrossoverRate,individualMutationRate,GeneMutationRate,generationsToRun
CXPB, enterMutation, MUTPB, NGEN = 0.8, 1, 0.1, 200#400

wildcardWeight = 0.5#0.8#0.9 #chance that a gene initialized is a wildcard
wcw_switching = True
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

#------------------------------------------------------