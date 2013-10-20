#--CONTROL PANEL---------------------------------------
#------Modifiable variables (notable ones)----------------

n_pop = 400 #400# Number of individuals in the whole population

if n_pop > 800:         # elites per attack type chosen for next gen
    elitesNo = n_pop/50#n_pop/100#10
else:
    elitesNo = n_pop/50#n_pop/100 

elitesNo = 2

sel_divisor = 1#4/3.0 #1 dividing factor for selection operator

#CrossoverRate,individualMutationRate,GeneMutationRate,generationsToRun
CXPB, enterMutation, MUTPB, NGEN = 0.8, 0.4, 0.25, 60#0.9, 0.9, 200#

wildcardWeight = 0.9#0.8#0.9 #chance that a gene initialized is a wildcard
wcw_switching = False
wcw_a = 0.4
wcw_b = 0.9
wcw_swapGen = 20

weightSupport, weightConfidence = 0.2,0.8#0.2, 0.8

wildcardPenalty = True #only apply in loop to increase variety of good results
wildcardPenaltyWeight = 0.00000000001#0.00000001#0.000001#
wildcard_allowance = 0 # 1 to 15 #currently not in used nor implemented yet

Result_numbers = n_pop#800 #800 #30
show_stats = True
show_elites = True
bestTopKnots = 4

#--Ace Comparison options
fitnessDiff_opt = True
fitnessDiff_value = 0.001
matchEliminate_opt = False
matchEliminate_AllowFields = 6 # in TopKnots filter (Threshold)

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
#fileName = 'w4_wed.list' 
#fileName = 'w5_tue.list'
#fileName = 'w5_thu.list' #uptil
#fileName = 'w6_tue.list'
#fileName = 'w6_thu.list'
#fileName = 'w7_tue.list'

#for portsweep training
#fileName = 'psw_w6_thu.list'

#for ipsweep training
#fileName = 'ipsw_w2_tue.list'
#fileName = 'ipsw_w3_wed.list'
#fileName = 'ipsw_w4_wed.list'
#fileName = 'ipsw_w34_w.list'

#for dict training
#fileName = 'dict_w6_thu.list'

#for neptune training
#fileName = 'nept_w1_wed.list'
#fileName = 'nept_w3_thu.list'
#fileName = 'nept_w4_tue.list'
#fileName = 'nept_w5_thu.list'

#for teardrop training
#fileName = 'teard_w4_tue.list'
#fileName = 'teard_w5_mon.list'

#fileName = 'test_allpod.list'

#for nmap training
#fileName = 'w3_wed.list'
#fileName = 'w3_fri.list'

#------------------------------------------------------