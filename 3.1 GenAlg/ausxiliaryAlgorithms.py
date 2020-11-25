import random
import copy
import math

def CreatePopulation(numPopulation, lista):
    
    population=[]
    for i in range(numPopulation):
        listCopy=copy.deepcopy(lista)
        listCopy.remove(lista[0])
        random.shuffle(listCopy)
        listCopy.insert(0,0)
        population.append(listCopy)

    return population

def Distance(p1, p2):    
    dist=math.sqrt((p2.x-p1.x)**2+(p2.y-p1.y)**2)
    return dist


