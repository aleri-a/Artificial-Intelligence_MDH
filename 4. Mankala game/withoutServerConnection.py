import copy

move='99'

def CatchOpossit(tablala,plTn,myPos): #checking can i get smth 
    mySt=tablala[myPos]
    nextPos=(myPos+mySt)
    if(plTn==1):
        if(nextPos>12):
            nextPos+=1
    nextPos=nextPos%len(tablala)
    
    
    opPos=13-myPos-1
    catchedStones=0
    if(plTn==1):
        catchedStones+=tablala[opPos]+tablala[myPos]
    else:
        catchedStones+=tablala[opPos]+tablala[myPos]
    return catchedStones


def GetPossibleMoves(tabla, playerTurn):
    
    moves=[]
    if playerTurn==1:
        for index in range(0,6):
            if tabla[index]!=0:
                stonesOposit=0
                stonesOposit+=CatchOpossit(tabla,playerTurn,index)
                tmp=(str(index),(6-index-tabla[index])+stonesOposit*10)
                moves.append(tmp)            
    else:
        for index in range(7,13):
            if tabla[index]!=0:
                stonesOposit=0
                stonesOposit+=CatchOpossit(tabla,playerTurn,index)
                tmp=(str(index),(6-index-tabla[index])+stonesOposit*10)               
                moves.append(tmp)
    #order moves, na pocetku ce biti oni koji tacno toliko treba da stignu do cilja
    moves.sort(key=lambda tup: tup[1])
    resMoves=[]
    for el in moves:
        resMoves.append(el[0])
    return resMoves #vracam samo listu indeksa 


def ChangePlayer(plTurn):
    if plTurn==1:
        return 2
    else:
        return 1


def GetOpossitStones(tablala,myPos,plTn):
    opPos=13-myPos-1
    if(plTn==1):
        tablala[6]+=tablala[opPos]+tablala[myPos]
    else:
        tablala[13]+=tablala[opPos]+tablala[myPos]
    tablala[opPos]=0
    tablala[myPos]=0


    
    


def MyHole(pos,plTn):
    if(plTn==1):
        return pos in range(0,6)
    else:
        return pos in range(7,13)

def CheckEmptySide(tababla):
    if sum(tababla[0:6])==0:
        tababla[13]+=sum(tababla[7:13])
        tababla[7:13]=[0]*6
    elif sum(tababla[7:13])==0:
        tababla[6]+=sum(tababla[0:5])
        tababla[0:5]=[0]*6

def DoMove(table,mv,playerTn):
    stones=table[mv]                
    newTable=copy.deepcopy(table)
    newTable[mv]=0
    while stones>0:
        nextPos=(mv+1)%len(table)
        if(playerTn==1 and nextPos==13):
            nextPos=0
        elif(playerTn==2 and nextPos==6):
            nextPos=7
        
        newTable[nextPos]+=1
        if(stones==1 and MyHole(nextPos,playerTn) and newTable[nextPos]==1):
            GetOpossitStones(newTable,nextPos,playerTn)               
        stones-=1
        mv=nextPos
    
    CheckEmptySide(newTable)            
    if (playerTn==1 and nextPos==6) or (playerTn==2 and nextPos==13) :
        return (newTable,playerTn)
    else:
        return (newTable,ChangePlayer(playerTn))



def CheckWinner(tablela):
    if End_of_game(tablela):
        if tablela[6]>tablela[13]:
            return 1
        elif tablela[13]>tablela[6]:
            return 2
        else:
            return 0            
    return -1


def End_of_game(tababla): 
    if sum(tababla[0:6])==0 or sum(tababla[7:13])==0:        
        return True
    else:
        return False




def Evaluation(tabbla,plTn,Iam): #ocenjujem moju trenutnu tablu utility fjas HEURISTIC
    
    winner=CheckWinner(tabbla)
    if Iam and winner==plTn:
        return 100000
    elif winner==ChangePlayer(plTn):
        return -100000
    elif winner==0:
        return 50000
    
    stones1=sum(tabbla[0:6])
    stones2=sum(tabbla[7:13])
    points=0
    if(plTn==1):
        points+=tabbla[6]*1000-tabbla[13]*1000
        points+=stones1*100      

    else:
        points+=tabbla[13]*1000-tabbla[6]*1000
        points+=stones2*100


    if not Iam:
        points*=-1

    return points




    #playerAI je samo da znam jel sam ja ili komp (true, False), playerTn -da bih ispitala koje pozicije proveravam znaci 1,2
def MinMax(board, depth, alpha, beta, playerAI,playerTn):
    print("MIN-MAX fja, board: ",board, "alpha,beta :",alpha,beta, )
    if depth==0 or End_of_game(board):
        res= Evaluation(board,playerTn,playerAI) # 1-(0,5 polja), 2-(7,12)
        return res

    if playerAI:
        maxEval=float('-inf')
        moveve=GetPossibleMoves(board,playerTn)
        for a in moveve:
            (newTable, plTn)=DoMove(board,int(a),playerTn)
            if(playerTn==plTn):
                nextAiPlayer=True
            else: 
                nextAiPlayer=False
            if beta==4200:
                print("cekam drugi put")    
            eval=MinMax(newTable,depth-1,alpha,beta,nextAiPlayer,plTn)
            if depth==3 and eval>maxEval :
                global move 
                print("kraj tabela: ",newTable)
                move=a

            maxEval=max(maxEval,eval)
            alpha=max(alpha,eval)


            if beta<=alpha:
                break
        return maxEval
           

    else: 
        minEval=float('inf')
        moveve=GetPossibleMoves(board,playerTn)
        for a in  moveve:
            (newTable, plTn)=DoMove(board,int(a),playerTn)
            if(playerTn==plTn):
                nextAiPlayer=False
            else: 
                nextAiPlayer=True
            eval=MinMax(newTable,depth-1,alpha,beta,nextAiPlayer,plTn)
            minEval=min(minEval,eval)
            beta=min(beta,eval)
            if beta<=alpha:
                break
        return minEval





if __name__=='__main__':
    print("pozvacu min max, move pre toga je : ")
    #board=[0, 0, 0, 3, 1, 0, 0, 2, 0, 0, 3, 0, 0, 0]
    #board=[4, 4,4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
      # board=[3, 0, 1, 0, 0, 2, 2, 2, 0, 0, 3, 0, 0, 0]
    
    #board=[4, 4,4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0] #start, 
    #board=[4, 4,4, 0, 5, 5, 1, 5, 4, 4, 4, 4, 4, 0] #I igrado 3
    board=[5, 4,4, 0, 5, 5, 1, 5, 4, 4, 0, 5, 5, 1]  # II igrao 10
    
 
    heuristic= MinMax(board,3,float('-inf'),float('inf'),True,1)
    print("movee moj kraj: ",move)


