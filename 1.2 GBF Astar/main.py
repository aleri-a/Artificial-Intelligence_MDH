#A* abnd greedy-best first
# Malaga to Valladolid 
'''
Implementation:Order the nodes in the stack in decreasing order of desirability
greedy best ->f(n) = h(n)

A*->  f(n) = g(n) + h(n) 
pazi g(n) ti je duzina prethodnih puteva + duzina novi put
'''

from  queue import PriorityQueue
import time





class MyPriorityQueue(PriorityQueue):
    def _put(self, item):
        return super()._put((self._get_priority(item), item))

    def _get(self):
        return super()._get()
    def _get_priority(self, item):
        return int(item.fja)


class MyPriorityQueue2:
    def __init__(self):
        self.queue=[]

    def Put(self,element):
        self.queue.append(element)
        self.queue.sort(key=lambda x: int(x.fja), reverse=False)

    def Get(self):
        return self.queue.pop(0)


    def Empty(self):
        if(len(self.queue)==0):
            return True
        else:
             return False

    






class Neighbord:
    def __init__(self,parent,name,cost):
        self.cost=cost
        self.parrent=parent 
        self.name=name

    def printDetails(self):
        print (self.name)

class Node: 
    def __init__(self,parent,name,fja,cost):
        self.name=name 
        self.parent=parent 
        self.fja=fja
        self.cost=cost




def ReadFile():
    
    graph={ }
    heuristicTable ={ }
    f=open('input.txt','r') 
    pomNum=-1
    while(pomNum==-1 ):
        pomStr=f.readline()
        pomNum=pomStr.find("COMMENT:")

    start=pomStr.find("COMMENT:")+len("COMMENT:")+1
    end=pomStr.find(" ",start)
    num=""
    while(start<=end):
        num=num+pomStr[start]
        start+=1
    num=int(num)
    
    f.readline()
    f.readline()

    line=f.readline()
    while line !='\n': 
        if 'Salamanca Caceres' in line:
            print('here')
        words=line.replace("\t",' ').split(' ')
        words[2]=words[2][0:len(words[2])-1]#0:len(words[2])-1
        neig=Neighbord(words[0],words[1],words[2])
        if words[0] not in graph.keys():
            graph.setdefault(words[0],[]).append(neig)
        else:
            graph[words[0]].append(neig)

        neigThis=Neighbord(words[1],words[0],words[2])
        if words[1] not in graph.keys():
                graph.setdefault(words[1],[]).append(neigThis)
        else:
            graph[words[1]].append(neigThis)
       
        line=f.readline()     


    f.readline()
    f.readline()
    line=f.readline()
    while line !='':
        words=line.split(' ')
        if '\n' in words[1]:
            words[1]=words[1][0:len(words[1])-1]
        heuristicTable[words[0]]=words[1]
        line=f.readline()

    return graph,heuristicTable


def CheckRepetition(childsNode,parent): #da li ima prethodnike tj da se nevrti u krug     
    while(parent!=None):
        for ch in childsNode:
            if(parent.name==ch.name):
                childsNode.remove(ch)
        parent=parent.parent
    return childsNode
        


def GBF(graph,hTable,start,end):
    currNode=Node(None,start,int(hTable[start]),0)
    q = MyPriorityQueue2()  
    q.Put(currNode)
    while not q.Empty():
        elNode=q.Get()
       
        if elNode.name==end:
                return elNode
        childs=graph[elNode.name] 
        childs=CheckRepetition(childs,elNode)  
        for ch in childs: 
            child=Node(elNode,ch.name,int(hTable[ch.name]),int(ch.cost)+elNode.cost)
            q.Put(child)

   



def Astar(graph,hTable,start,end):
    currNode=Node(None,start,int(hTable[start]),0)
    q = MyPriorityQueue2()  
    q.Put(currNode)
    while not q.Empty():
        elNode=q.Get()
        
        if elNode.name==end:
                return elNode
        childs=graph[elNode.name] 
        childs=CheckRepetition(childs,elNode)  
        for ch in childs: 
            child=Node(elNode,ch.name,int(hTable[ch.name])+int(ch.cost)+elNode.cost,int(ch.cost)+elNode.cost)
            q.Put(child)
            
    print(q)


def printPath(start):
    print("Real path= ",start.cost)
    res=start.name    
    start=start.parent
    while start != None :
        res+=" "+start.name
        start=start.parent

    print(res)



graph, hTable=ReadFile()
print("_________GBF: ")
startT=time.time()
rez=GBF(graph,hTable,"Malaga","Valladolid")
endT=time.time()
gbfTime=endT-startT
print(gbfTime,"seconds")
printPath(rez)


print("_________ A* ")
startT=time.time()
rez=Astar(graph,hTable,"Malaga","Valladolid")
endT=time.time()
astTime=startT-endT
print(endT-startT,"seconds")
printPath(rez)

#print("A*/GBF =",float(astTime/gbfTime ))
