from idsproto import *

def weighted_choice(weights):
    totals = []
    running_total = 0

    for w in weights:
        running_total += w
        totals.append(running_total)

    rnd = random.random() * running_total
    for i, total in enumerate(totals):
        if rnd < total:
            return i


import bisect
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



#def uniq_randomizor(uniq_fields):
#	fields = len(uniq_fields)
#	for i in xrange(fields):



	#if random.random() >= 0.9/fields

#--- not needed yet
#toolbox.register("attr_255", random.randint, 0, 255)
#toolbox.register("attr_65535", random.randint, 0, 65535)
#toolbox.register("attr_hour", random.randint, 0, 65535)
#toolbox.register("attr_minute", random.randint, 0, 59)
#toolbox.register("attr_second", random.randint, 0, 59)
#toolbox.register("attr_wildcard", random.randint, -1, 1)

#def portu(uniq_srcport):
#    return uniq_srcport[random.randint(0, len(uniq_srcport)-1)]

#then this, so now we can use attr_port, ##try generalize this for all
#toolbox.register("attr_port", portu, uniq_srcport)