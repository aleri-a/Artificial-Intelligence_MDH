#!/usr/bin/python           # This is server.py file

import socket  # Import socket module
import numpy as np
import time
from multiprocessing.pool import ThreadPool
import os



import copy

def receive(socket):
    msg = ''.encode()  # type: str

    try:
        data = socket.recv(1024)  # type: object
        msg += data
    except:
        pass
    return msg.decode()


def send(socket, msg):
    socket.sendall(msg.encode())


# VARIABLES
playerName = 'Aleksandra Ristic'
host = '127.0.0.1'
port = 30000  # Reserve a port for your service.
s = socket.socket()  # Create a socket object
pool = ThreadPool(processes=1)
gameEnd = False
MAX_RESPONSE_TIME = 50

print('The player: ' + playerName + ' starts!')
s.connect((host, port))
print('The player: ' + playerName + ' connected!')


move = '99'
while not gameEnd:

    asyncResult = pool.apply_async(receive, (s,))
    startTime = time.time()
    currentTime = 0
    received = 0
    data = []
    while received == 0 and currentTime < MAX_RESPONSE_TIME:
        if asyncResult.ready():
            data = asyncResult.get()
            received = 1
        currentTime = time.time() - startTime

    if received == 0:
        print('No response in ' + str(MAX_RESPONSE_TIME) + ' sec')
        gameEnd = 1

    if data == 'N':
        send(s, playerName)

    if data == 'E':
        gameEnd = 1

    if len(data) > 1:

        # Read the board and player turn
        board = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        playerTurn = int(data[0])
        i = 0
        j = 1
        while i <= 13:
            board[i] = int(data[j]) * 10 + int(data[j + 1])
            i += 1
            j += 2

        # Using your intelligent bot, assign a move to "move"
        #
        # example: move = '1';  Possible moves from '1' to '6' if the game's rules allows those moves.
        # TODO: Change this
        ################
        

#board: Information of the board.
# playerTurn: 1, you can empty from position 0 to 5 (1 to 6 in matlab). 2, you can empty form position 7 to 12 (8 to 13 in matlab).
# move: Which move will you make. Always from 1 to 6 independently from the playerTurn.



        def GetPossibleMoves(tabla, playerTurn):
            moves=[]
            steal=0
            if playerTurn==1:
                for index in range(0,6):
                    if tabla[index]!=0:
                        #steal=TryCatchOpossit(tabla,playerTurn,index)
                        if(steal>0):
                            tmp=(str(index),steal)
                        else:                      
                            tmp=(str(index),6-index-tabla[index])
                        moves.append(tmp)            
            else:
                for index in range(7,13):
                    if tabla[index]!=0:
                        #steal=TryCatchOpossit(tabla,playerTurn,index)
                        if(steal>0):
                            tmp=(str(index),steal)
                        else:                      
                            tmp=(str(index),6-index-tabla[index])                        
                        moves.append(tmp)
           
            moves.sort(key=lambda tup: tup[1])
            resMoves=[]
            for el in moves:
                resMoves.append(el[0])
            return resMoves 


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
            if End_of_game:
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


        

        
        def Evaluation(tabbla,plTn,Iam): 
           
            winner=CheckWinner(tabbla)
            points=0
            if Iam and winner==plTn:
                points+= 10000
            elif winner==ChangePlayer(plTn):
                points+= -10000
            elif winner==0:
                points+= 5000
            
            stones1=sum(tabbla[0:6])
            stones2=sum(tabbla[7:13])
            points=0

            #emptyCells=0
            #if plTn==1:
            #   for i in range(0,6):
            #       if(tabbla[i]==0):
            #           emptyCells+=1
            #else:
            #   for i in range(7,13):
            #       if(tabbla[i]==0):
            #           emptyCells+=1
            

            if(plTn==1):
                points+=tabbla[6]*100-tabbla[13]*100
                points+=stones1*10-stones2*10

            else:
                points+=tabbla[13]*100-tabbla[6]*100
                points+=stones2*10-stones1*10

            #points+=(6-emptyCells)*100
            if not Iam:
                points*=-1
            return points

       
        def TryCatchOpossit(tablala,plTn,myPos): #not using it 
            stones=tablala[myPos]
            newPos=(myPos+stones)%13-1
            mine=False
            if(plTn==1):
                if(newPos<=12 and newPos>=7):
                    mine=True
            else:
                if(newPos>=0 and newPos<=5):
                    mine=True
            if(mine and tablala[newPos]==0):
                opPos=13-newPos-1
                return tablala[opPos]
            return 0

                
            
           



       
         #playerAI - true, False, playerTn - 1,2
        def MinMax(board, depth, alpha, beta, playerAI,playerTn):
           
            if depth==0 or End_of_game(board):
                res= Evaluation(board,playerTn,playerAI) # 1-(0,5 pos), 2-(7,12 pos)
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
                       
                    eval=MinMax(newTable,depth-1,alpha,beta,nextAiPlayer,plTn)
                    if depth==3 and eval>maxEval :
                        global move 
                       
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



       
        heuristic=MinMax(board,3,float('-inf'),float('inf'),True,playerTurn)
        pomMove=int(move)
        if(pomMove<6):
            pomMove+=1
        else: 
            pomMove=(pomMove+6)%13+1
        move=str(pomMove)
        #print(heuristic, move)

       

        ################
        
        send(s, move)
