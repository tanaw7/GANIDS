def evalOneMax(individual):
    return sum(individual),

def evalZeroMax(individual):
   score = 0.0
   for i in individual:
      if i == 0:
         score += 1.0
   return score,

def evalTartan01(individual):
   score = 0.0
   for i in xrange(len(individual)):
      if (i%2 == 0 and individual[i] == 0) or (i%2 == 1 and individual[i] == 1):
         score = score + 1.0

   return score,

def evalhalf01(individual):
    score = 0.0
    for i in xrange(len(individual)):
        if (i <= len(individual)/2 - 1 and individual[i] == 0) or (i > len(individual)/2 - 1 and individual[i] == 1):
            score = score + 1.0

    return score,

def evaliIDS(individual):
  score = 0.0
  if individual[len(individual)-1] == '-':
    score += 1

  return score,

def evalIDS(individual):
  fitness = 0.5
  return fitness,