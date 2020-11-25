from FileInfo import CreateCities
import numpy as np
import matplotlib.pyplot as plt
import sys
import os


ITERATIONS=250
N_ANTS=40
EVAPORaTION_rate=0.25
ALPHA=4
BETA=3


#Ant Colony Optimization 

class ACO:
    def __init__(self,distances):
        self.distanceT=distances
        self.n_cities=len(distances[0])

        self.heuristicT=1/distances
        self.heuristicT[self.heuristicT==np.inf]=0
        self.pheromneT=np.ones((self.n_cities,self.n_cities))
        self.rute=np.zeros((N_ANTS,self.n_cities+1)) 


    def Make_Rute(self,rute, ant):
        tmp_h= np.array(self.heuristicT)

        for city in range(self.n_cities-1):
           
            cur_loc=int(rute[ant,city]-1)
            tmp_h[:,cur_loc]=0

           #Transition rule
            phePart=np.zeros(self.n_cities)
            heuPart=np.zeros(self.n_cities)

            phePart=np.power(self.pheromneT[cur_loc,:],ALPHA)
            heuPart=np.power(tmp_h[cur_loc,:],BETA)
            phePart=phePart[:,np.newaxis]
            heuPart=heuPart[:,np.newaxis]

            upPart=np.zeros(self.n_cities) 
            upPart=np.multiply(phePart,heuPart)
            downPart=np.sum(upPart)
           
            probability=upPart/downPart
            rulet=np.cumsum(probability)

            r=np.random.random_sample()
            newCity=np.nonzero(rulet>r)[0][0]+1
            rute[ant,city+1]=newCity

        rute[ant][self.n_cities]=1

        return rute


    def Rutes(self):
        self.rute[:,0]=1 

        for i in range(N_ANTS):
            self.rute=self.Make_Rute(self.rute,i)
        
        costPath=np.zeros((N_ANTS,1))
        for i in range(N_ANTS):
            summ=0
            for j in range(self.n_cities-1):  
                fromC=int(self.rute[i,j])-1
                toC=int(self.rute[i,j+1])-1
                summ+=self.distanceT[fromC][toC]
            costPath[i]=summ


        min_loc=np.argmin(costPath)
        min_cost=costPath[min_loc]
        best_route=self.rute[min_loc,:]
        
        #Evaporation
        self.pheromneT=(1-EVAPORaTION_rate)*self.pheromneT

        for i in range(N_ANTS):
            for j in range(self.n_cities):
                newPhe=1/costPath[i]
                fromC=int(self.rute[i,j])-1
                toC=int(self.rute[i,j+1])-1
                self.pheromneT[fromC,toC]+=newPhe

        return (min_cost,best_route)




if __name__=="__main__": 
    fileInfo=CreateCities() 

    global_min=np.inf
    print("\n________________________ACO_________________________________\n")
    
    aco=ACO(fileInfo.distance_table)
    global_route=np.zeros(aco.n_cities+1)
    progressNew=[]
    progressBest=[]
    for i in range(ITERATIONS):
       min_cost,best_route= aco.Rutes()
       progressNew.append(min_cost)
       if(i%10==0):  
            percents=100*i/ITERATIONS
            sys.stdout.write('%s%s\r' % ( percents, '%'))
            sys.stdout.flush()
       progressBest.append(global_min)    
           
       if(min_cost[0]<global_min):
           global_min=min_cost[0]
           global_route=best_route


    sys.stdout.write('%s%s\r' % ( 100, '%'))
    sys.stdout.flush()    
    plt.plot(progressNew)
    plt.plot(progressBest)
    plt.ylabel('Distance')
    plt.xlabel('Generation')
    #plt.annotate(global_route, (0,0), (-20, 0), xycoords='axes fraction', textcoords='offset points', va='top')
    #plt.figtext(0.8, 0, 'alpha = %.2f , beta = %.2f , rho = %.2f , population size: %d' % (ALPHA, BETA, EVAPORaTION_rate, N_ANTS), horizontalalignment='right')
    plt.legend(['Generation best','Global best'])
    
    plt.suptitle('alpha = %.2f , beta = %.2f , evaporation rate = %.2f ,num ants: %d' % (ALPHA, BETA, EVAPORaTION_rate, N_ANTS), fontsize=7)
    
    plt.title('Ant Colony Optimization')
    plt.show(True)
    print(global_min)
    print(global_route)
    



