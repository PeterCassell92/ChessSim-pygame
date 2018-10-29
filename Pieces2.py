from operator import add
from operator import sub
import string

from meld.vc.svk import NULL
from Tile import Tile


def initBoard():
    global board
    global piecedict
    global wap, wbp, wcp, wdp, wep, wfp, wgp, whp
    global bap, bbp, bcp, bdp, bep, bfp, bgp, bhp
    global wqr, wqb, wqn, wqq, wkk, wkb, wkn, wkr
    global bqr, bqb, bqn, bqq, bkk, bkb, bkn, bkr
        #initialise board dictionary (each of the 64 squares that can be occupied) 
    board= {}

    i=1
    while i < 9:
        j = 1
        while j < 9:
            
            value = Tile(coordstoGrid(str(i), str(j)))
         
            board[coordstoGrid(str(i), str(j))] = value  
                    
            j += 1
        i += 1


    #these are tile objects

    #initialise spawning of each piece as Piece object with key attributes color side type
        
    wap = Pawn("W", 1)
    wbp = Pawn("W", 2)
    wcp = Pawn("W", 3)
    wdp = Pawn("W", 4)
    wep = Pawn("W", 5)
    wfp = Pawn("W", 6)
    wgp = Pawn("W", 7)
    whp = Pawn("W", 8)
    bap = Pawn("B", 1)
    bbp = Pawn("B", 2)
    bcp = Pawn("B", 3)
    bdp = Pawn("B", 4)
    bep = Pawn("B", 5)
    bfp = Pawn("B", 6)
    bgp = Pawn("B", 7)
    bhp = Pawn("B", 8)
    wqb = Bishop("W", "Q")
    wkb = Bishop("W", "K")
    bqb = Bishop("B", "Q")
    bkb = Bishop("B", "K")
    wqn = Knight("W", "Q")
    wkn = Knight("W", "K")
    bqn = Knight("B", "Q")
    bkn = Knight("B", "K")
    wqr = Rook("W", "Q")
    wkr = Rook("W", "K")
    bqr = Rook("B", "Q")
    bkr = Rook("B", "K")
    wqq = Queen("W")
    bqq = Queen("B")
    wkk = King("W")
    bkk = King("B")

    piecedict = [wqr, wqn, wqb, wqq, wkk, wkb, wkn, wkr, wap, wbp, wcp, wdp, wep, wfp, wgp, whp,\
                  bqr, bqn, bqb, bqq, bkk, bkb, bkn, bkr, bap, bbp, bcp, bdp, bep, bfp, bgp, bhp]

def scoutAll():
    global whitecheck
    global blackcheck
    global wsupportedpiece
    global bsupportedpiece

    whitecheck = []
    blackcheck = []
    wsupportedpiece = []
    bsupportedpiece = []
    wveccheck =[]
    bveccheck =[]
    for piece in piecedict:
        if piece.grid != "Taken":
            piece.scoutMoves()
            if piece.type != "p":
                for element in piece.possmoves:
                    if piece.color == "W":
                        if any(t == element for t in whitecheck):
                            pass
                        else:   
                            whitecheck.append(element)
                    if piece.color == "B":
                        if any(t == element for t in blackcheck):
                            pass
                        else:   
                            blackcheck.append(element)
                for element in piece.supportedpieces:
                    if piece.color == "W":
                        if any(t == element for t in whitecheck):
                            pass
                        else:   
                            whitecheck.append(element)
                    if piece.color == "B":
                        if any(t == element for t in blackcheck):
                            pass
                        else:   
                            blackcheck.append(element)
            if piece.type== "p":
                if piece.color == "W":
                    diag1 = map(add, [1,1],piece.position )
                    diag2 = map(add, [-1,1], piece.position)
                    if 0 < diag1[0] <= 8 and 0 <diag1[1] <= 8:
                                              
                        space = coordstoGrid(str(diag1[0]),str(diag1[1]))
                        
                        if any(t == space for t in whitecheck):
                            pass
                        else:   
                            whitecheck.append(space)
                    if 0 < diag2[0] <= 8 and 0 <diag2[1] <= 8:
                        
                        space = coordstoGrid(str(diag2[0]),str(diag2[1]))
                        

                        if any(t == space for t in whitecheck):
                            pass
                        else:   
                            whitecheck.append(space)
                if piece.color == "B":
                    diag1 = map(add, [1,-1],piece.position )
                    diag2 = map(add, [-1,-1], piece.position)
                    if 0 < diag1[0] <= 8 and 0 <diag1[1] <= 8:

                        space = coordstoGrid(str(diag1[0]),str(diag1[1]))

                        if any(t == space for t in blackcheck):
                            pass
                        else:   
                            blackcheck.append(space)
                    if 0 < diag2[0] <= 8 and 0 <diag2[1] <= 8:

                        space = coordstoGrid(str(diag2[0]),str(diag2[1]))

                        if any(t == space for t in blackcheck):
                            pass
                        else:   
                            blackcheck.append(space)

    if any(u == wkk.grid for u in blackcheck):
        print "White King in Check"
        wkk.check= True
        dbc =[] # direct black check
        checkers= 0
        allwposs =[]
        wveccheck =[]
        for piece in piecedict:
            if piece.color == "B": ##and piece.type != "p":
                    for i in piece.possmoves:
                        if i == wkk.grid:
                            checkers +=1
                            if piece.type != "n":

                                checkvec=  map(sub, wkk.position , piece.position)
                                checkLDV =findLDV(checkvec) #lowestdenominatorvector
                                checksquare = piece.position

                                if piece.type != "p":
                                    m = map(add, wkk.position, checkLDV)
                                    if 0< m[0] <=8 and 0 < m[1]  <=8:
                                        
                                        n= coordstoGrid(str(m[0]),str(m[1]))
                                        if any(s== n for s in wkk.possmoves):
                                            wveccheck.append(n)

                                
                                
                                while checksquare != wkk.position:
                                    dbc.append(coordstoGrid(str(checksquare[0]),str(checksquare[1])))
                                    checksquare = map(add, checksquare , checkLDV)

                                piece.possmoves.remove(i)
                                #print dbc
                            else:
                                dbc.append(piece.grid)
        for piece in piecedict:                
            if piece.color == "W" and piece.type != "k": ##and piece.type != "p":
                if checkers ==1:
                    i=0
                    while i < len(piece.possmoves) :
                        if any(s == piece.possmoves[i] for s in dbc):
                            allwposs.append(piece.possmoves[i])
                            i+=1
                        else:
                            del piece.possmoves[i]
                if checkers > 1:
                    piece.possmoves =[]



    else:
        wkk.check = False


    if any(u== bkk.grid for u in whitecheck):
        print "Black King in Check"
        bkk.check = True
        dwc =[]
        checkers = 0
        allbposs=[]
        bveccheck=[]
        for piece in piecedict:
            if piece.color == "W": ##and piece.type != "p":
                for i in piece.possmoves:
                    if i == bkk.grid:
                        checkers +=1
                        if piece.type != "n":

                            checkvec=  map(sub, bkk.position , piece.position)
                            checkLDV =findLDV(checkvec) #lowestdenominatorvector
                            checksquare = piece.position

                            if piece.type != "p":
                                    m = map(add, bkk.position, checkLDV)
                                    if 0< m[0] <=8 and 0 < m[1]  <=8:
                                        n= coordstoGrid(str(m[0]),str(m[1]))
                                        
                                        if any(s== n for s in bkk.possmoves):
                                            bveccheck.append(n)
                            
                            
                            while checksquare != bkk.position:
                                dwc.append(coordstoGrid(str(checksquare[0]),str(checksquare[1])))
                                checksquare = map(add, checksquare , checkLDV)
                                
                            piece.possmoves.remove(i)     
                        else:
                            dwc.append(piece.grid)          
                        
            if piece.color == "B" and piece.type != "k": ##and piece.type != "p":
                if checkers ==1:
                    i=0
                    while i < len(piece.possmoves) :
                        if any(s == piece.possmoves[i] for s in dwc):
                            allbposs.append(piece.possmoves[i])
                            i+=1
                        else:
                            del piece.possmoves[i]
                if checkers > 1:
                    piece.possmoves = []

        

    else:
        bkk.check= False



    bkk.scoutMoves()
    wkk.scoutMoves()

    whitecheck.extend(bveccheck)
    blackcheck.extend(wveccheck)
    bkdellist = []
    for elements in bkk.possmoves:

        for i in [i for i, x in enumerate(bkk.possmoves) if any(x== t for t in whitecheck)]:
            #print i
            if any(s == i for s in bkdellist):
                pass
            else:   
                bkdellist.append(i)
    #King cannot move into check

    for elements in sorted(bkdellist, reverse=True):
        del bkk.possmoves[elements]

    #Delete check elements from bkpossmoves

    wkdellist = []
    for elements in wkk.possmoves:

        for i in [i for i, x in enumerate(wkk.possmoves) if any(x== t for t in blackcheck)]:
            #print i
            if any(s == i for s in wkdellist):
                pass
            else:   
                wkdellist.append(i)
       
    for elements in sorted(wkdellist, reverse=True):
        del wkk.possmoves[elements]

    if bkk.check == True:    
        for element in bkk.possmoves:
            allbposs.append(element)
        if len(allbposs) == 0:
            print "CHECKMATE"
            bkk.mated =True
            
    if wkk.check == True:    
        for element in wkk.possmoves:
            allwposs.append(element)
        if len(allwposs) == 0:
            print "CHECKMATE"
            wkk.mated = True

            

def findLDV(vector):
    if vector[0] != 0 and vector[1] == 0:
            minvector = [x / abs(vector[0]) for x in vector]
            #print self.minvector
           
                
    elif abs(vector[1]) == abs(vector[0]) and vector[1] != 0 and vector[0] !=0:
        minvector = [x / abs(vector[1]) for x in vector]
  

    elif vector[1] != 0 and vector[0] ==0:
        minvector = [x / abs(vector[1]) for x in vector]

    return minvector
           



    
def coordstoGrid(xcoordinate, ycoordinate):
    characters = string.maketrans("12345678", "ABCDEFGH")
    text = xcoordinate.translate(characters)
    gridoutput= text + str(ycoordinate)
    return gridoutput

class Piece(object):

    def __init__(self):
       pass
    
    def getPosition(self):
        return self.position
    
    def getGrid(self):
        self.xpos = str(self.position[0])
        characters2 = string.maketrans("12345678", "ABCDEFGH")
        self.text2 = self.xpos.translate(characters2)
        self.grid= self.text2 + str(self.position[1])
        return self.grid
    
    def confirmInit(self):
        self.iD= '%s%s%s' %(self.color.lower(), self.side.lower(),self.type)
        board["%s" %(self.getGrid())].occupy()
        board["%s" %(self.getGrid())].piececolor=self.color
        board["%s" %(self.getGrid())].pieceID=self.iD
        self.hasmoved = False
        self.movevalidity = False
        #print board["%s" %(self.getGrid())].pieceID
     
    def confirmMove(self):
        if board["%s" %(self.getGrid())].occupancy == True:
            self.takePiece()
        
        board["%s" %(self.getGrid())].occupy()
        board["%s" %(self.getGrid())].piececolor=self.color
        board["%s" %(self.getGrid())].pieceID=self.iD
        self.movevalidity = True
        

        
        #changeturn()

        
    def confirmLeave(self):
        board["%s" %self.getGrid()].unoccupy()

    def simMove(self):
        pass

    def moveTo(self, destination):
        for elements in self.possmoves:
            if elements == destination:
                if self.type == "k":
                    if self.color == "W":
                        if destination == "C1" and self.hasmoved == False:
                            
                            board["A1"].unoccupy()
                            wqr.position = [4,1]
                            board["D1"].occupy()
                            board["D1"].piececolor=wqr.color
                            board["D1"].pieceID=wqr.iD
                            #wqr.movevalidity = True
                            wqr.hasmoved = True
                    if self.color == "W":
                        if destination == "G1" and self.hasmoved == False:
                            board["H1"].unoccupy()
                            wkr.position = [6,1]
                            board["F1"].occupy()
                            board["F1"].piececolor=wkr.color
                            board["F1"].pieceID=wkr.iD
                            #wkr.movevalidity = True
                            wkr.hasmoved = True
                    if self.color == "B":
                        if destination == "C8" and self.hasmoved == False:
                            board["A8"].unoccupy()
                            bqr.position = [4,8]
                            board["D8"].occupy()
                            board["D8"].piececolor=bqr.color
                            board["D8"].pieceID=bqr.iD
                            #bqr.movevalidity = True
                            bqr.hasmoved = True
                    if self.color == "B":
                        if destination == "G8" and self.hasmoved == False:
                            board["H8"].unoccupy()
                            bkr.position = [6,8]
                            board["F8"].occupy()
                            board["F8"].piececolor=bkr.color
                            board["F8"].pieceID=bkr.iD
                            #bkr.movevalidity = True
                            bkr.hasmoved = True

                self.confirmLeave()
                characters = string.maketrans("ABCDEFGH", "12345678")
                letcon = destination.translate(characters)
                self.position= [int(letcon[0]), int(letcon[1])]
                self.confirmMove()      
        scoutAll()

    def takePiece(self):
        for x in piecedict:
            if x. position == self.position and x.iD != self.iD:
                x.position = []
                x.grid = "Taken"
                print "%s was taken by %s" %(x.iD, self.iD)
    
    def checkObstruction(self):
      
        self.obcheck = self.position
        self.obstruction = False
        if self.vector[0] != 0 and self.vector[1] == 0:
            self.minvector = [x / abs(self.vector[0]) for x in self.vector]
            
            z=1
            while z <= abs(self.vector[0])-1:
                self.obcheck= map(add, self.obcheck, self.minvector)
                z += 1
                
                self.checkpos= coordstoGrid(str(self.obcheck[0]),str(self.obcheck[1]))
                #print self.checkpos
                #print board["%s" %(self.checkpos)].occupancy
                if board["%s" %(self.checkpos)].occupancy == True:
                    self.obstruction = True
                
        elif abs(self.vector[1]) == abs(self.vector[0]) and self.vector[1] != 0 and self.vector[0] !=0:
            self.minvector = [x / abs(self.vector[1]) for x in self.vector]
            # print self.minvector
            z=1
            while z <= abs(self.vector[1])-1:
                self.obcheck= map(add, self.obcheck, self.minvector)
                z += 1
                
                self.checkpos= coordstoGrid(str(self.obcheck[0]),str(self.obcheck[1]))
                #print self.checkpos
                #print board["%s" %(self.checkpos)].occupancy
                if board["%s" %(self.checkpos)].occupancy == True:
                    self.obstruction = True   

        elif self.vector[1] != 0 and self.vector[0] ==0:
            self.minvector = [x / abs(self.vector[1]) for x in self.vector]
            # print self.minvector
            z=1
            while z <= abs(self.vector[1])-1:
                self.obcheck= map(add, self.obcheck, self.minvector)
                z += 1
                
                self.checkpos= coordstoGrid(str(self.obcheck[0]),str(self.obcheck[1]))
                #print self.checkpos
                #print board["%s" %(self.checkpos)].occupancy
                if board["%s" %(self.checkpos)].occupancy == True:
                    self.obstruction = True
   
                
class Rook(Piece):
      
    def __init__(self, color, side):
        self.color = color
        self.side = side
        self.type = "r"
        
        #if self.position == NULL:
        if self.color == "W":
            if self.side == "Q":
                self.initialposition = [1,1]
                                                
            elif self.side == "K":
                self.initialposition = [8,1]
            
        elif self.color == "B":
            if self.side == "Q":
                self.initialposition = [1,8]
                                
            elif self.side == "K":
                self.initialposition = [8,8]

        self.position = self.initialposition
        self.getGrid()
        self.confirmInit()
        
    def scoutMoves(self):
        self.supportedpieces=[]
        self.possmoves= []
        if self.grid != "Taken":
            i=1
            while i < 9:
                j = 1
                while j < 9:
                    
                    space = coordstoGrid(str(i),str(j))

                    
                    self.gridx=i
                    self.gridy=j
                    self.gridspace = [self.gridx, self.gridy]
                    self.vector = map(sub, self.gridspace, self.position)#print self.gridx        
                    self.checkObstruction()
                                   
                    if self.obstruction == False:
                        if self.gridx >= 1 and self.gridx <= 8:
                            if self.gridy >= 1 and self.gridy <= 8:
                            
                                
                                if self.vector[0] != 0 and self.vector[1] == 0:
                                    if board['%s' %(space)].piececolor != self.color:
                                        self.possmoves.append(space)
                                    elif board['%s' %(space)].piececolor == self.color:
                                        self.supportedpieces.append(space)
                                    #print "Valid rook move." # Rook moves to " + destination
                                elif self.vector[1] != 0 and self.vector[0] == 0:
                                    if board['%s' %(space)].piececolor != self.color:
                                        self.possmoves.append(space)
                                    elif board['%s' %(space)].piececolor == self.color:
                                        self.supportedpieces.append(space)
                                   # print "Valid rook move." # Rook moves to " + destination
                    j +=1
                i+=1            
        #print 'Position of Rook after attempted move ' + ', '.join(str(x) for x in self.position)
        
   
        #print self.grid
    

class Pawn(Piece):
      
    def __init__(self, color, rank):
        self.color = color
        self.rank =str(rank)
        self.type = "p"
        
        self.rank = coordstoGrid(str(rank),"")
       
        if self.color == "W":
                self.initialposition = [rank,2]
            
        elif self.color == "B":
                self.initialposition = [rank,7]
        self.possmoves = []
        self.position = self.initialposition    
        self.getGrid()
        self.side = self.rank
        #self.iD= '%s%s%s' %(self.color.lower(), self.rank.lower(), self.type)
        self.confirmInit()
#return
    def scoutMoves(self):
        self.possmoves= []
        self.supportedpieces = []
        if self.grid != "Taken":
            i=1
            while i < 9:
                j = 1
                while j < 9:
                   
                    space = coordstoGrid(str(i),str(j))

                    self.gridx=i
                    self.gridy=j
                    self.gridspace = [self.gridx, self.gridy]
                    self.vector = map(sub, self.gridspace, self.position)#print self.gridx    

                    #print space

                    self.checkObstruction()
                    #print self.gridy
                    #print 'Position of Pawn prior to attempted move was ' + self.grid
                    #print 'Vector of attempted move is ' + ', '.join(str(x) for x in self.vector)
                    
                    if self.obstruction == False:
                        if self.gridx >= 1 and self.gridx <= 8:
                            if self.gridy >= 1 and self.gridy <= 8:
                            
                                if self.color == "W":
                                    if self.vector == [0,1] and board['%s' %(space)].occupancy == False:
                                        if board['%s' %(space)].piececolor != self.color:
                                            self.possmoves.append(space)
                                        elif board['%s' %(space)].piececolor == self.color:
                                            pass
                                        
                                        #print "Valid pawn move." # Pawn moves to " + destination
                                    elif self.vector == [0,2] and self.position == self.initialposition and board['%s' %(space)].occupancy == False:
                                        if board['%s' %(space)].piececolor != self.color:
                                            self.possmoves.append(space)
                                        elif board['%s' %(space)].piececolor == self.color:
                                            pass
                                        #print "Valid pawn move." # Pawn moves to " + destination
                                    elif self.vector == [1,1] or self.vector == [-1,1]:
                                        if board['%s' %(space)].occupancy == True:
                                            if board['%s' %(space)].piececolor != self.color:
                                                self.possmoves.append(space)
                                            elif board['%s' %(space)].piececolor == self.color:
                                                self.supportedpieces.append(space)
                                           # print "Valid pawn move." # Pawn moves to " + destination 
                                        
                                elif self.color == "B":
                                    if self.vector == [0,-1] and board['%s' %(space)].occupancy == False:
                                        if board['%s' %(space)].piececolor != self.color:
                                            self.possmoves.append(space)
                                        elif board['%s' %(space)].piececolor == self.color:
                                            pass
                                        #print "Valid pawn move."# Pawn moves to " + destination
                                    elif self.vector == [0,-2] and self.position == self.initialposition and board['%s' %(space)].occupancy == False:
                                        if board['%s' %(space)].piececolor != self.color:
                                            self.possmoves.append(space)
                                        elif board['%s' %(space)].piececolor == self.color:
                                            pass
                                        #print "Valid pawn move." #Pawn moves to  + destination
                                    elif self.vector == [1,-1] or self.vector == [-1,-1]:
                                        if board['%s' %(space)].occupancy == True:
                                            if board['%s' %(space)].piececolor != self.color:
                                                self.possmoves.append(space)
                                            elif board['%s' %(space)].piececolor == self.color:
                                                self.supportedpieces.append(space)  
                                           # print "Valid pawn move." # Pawn moves to " + destination 
                                
                    j +=1
                i +=1                  
        
class Bishop(Piece):
      
    def __init__(self, color, side):
        self.color = color
        self.side= side
        self.type = "b"
        
        #if self.position == NULL:
        if self.color == "W":
            if self.side == "Q":
                self.initialposition = [3,1]
                
            elif self.side == "K":
                self.initialposition = [6,1]
            
        elif self.color == "B":
            if self.side == "Q":
                self.initialposition = [3,8]
                
            elif self.side == "K":
                self.initialposition = [6,8]
        
        self.position = self.initialposition
        self.getGrid()
        #self.iD= '%s%sB' %(self.color, self.side)
        self.confirmInit()
#return
    def scoutMoves(self):
        self.possmoves= []
        self.supportedpieces = []
        if self.grid != "Taken":
            i=1
            while i < 9:
                j = 1
                while j < 9:
                    
                    space = coordstoGrid(str(i), str(j))

                    #self.text = space.lower().translate(characters2)
                    self.gridx=i
                    self.gridy=j
                    self.gridspace = [self.gridx, self.gridy]
                    self.vector = map(sub, self.gridspace, self.position)#print self.gridx
                    #self.getGrid()
                    self.checkObstruction()
                    #print self.gridy
                    #print 'Position of Bishop prior to attempted move was ' + self.grid
                    #print 'Vector of attempted move is ' + ', '.join(str(x) for x in self.vector)
                    
                    if self.obstruction == False:
                        if self.gridx >= 1 and self.gridx <= 8:
                            if self.gridy >= 1 and self.gridy <= 8:
                            
                                if self.vector[0] != 0 and self.vector[1] !=0:   
                                    if abs(self.vector[0]) == abs(self.vector[1]):
                                        if board['%s' %(space)].piececolor != self.color:
                                            self.possmoves.append(space)
                                        elif board['%s' %(space)].piececolor == self.color:
                                            self.supportedpieces.append(space)
                    j += 1
                i += 1
                                    

                            
                            
                           
                   
            #print "Destination occupied by piece of same color."
       
        #self.getGrid()
        #print 'Position of Bishop after attempted move is ' + self.grid
        #print "\r"      

class Queen(Piece):
      
    def __init__(self, color):
        self.color = color
        self.side = "Q"
        self.type = "q"
        
        #if self.position == NULL:
        if self.color == "W":
            self.initialposition = [4,1] 
                          
        elif self.color == "B":
            self.initialposition = [4,8]
        
        self.position = self.initialposition
        self.getGrid()
        
        #self.iD= '%sQ' %(self.color)
        self.confirmInit()
#return
    
    def scoutMoves(self):
        self.possmoves = []
        self.supportedpieces = []
        if self.grid != "Taken":
            i=1
            while i < 9:
                j = 1
                while j < 9:
                    
                    space = coordstoGrid(str(i),str(j))
                    #print space

                    self.gridx= i
                    self.gridy= j
                    self.gridspace = [self.gridx, self.gridy]
                    self.vector = map(sub, self.gridspace, self.position)#print self.gridx
                    #print space
                    #print self.vector
                    #self.getGrid()
                    self.checkObstruction()
                    
                    #print self.gridy
                    #print 'Position of Queen prior to attempted move was ' + self.grid
                    #print 'Vector of attempted move is ' + ', '.join(str(x) for x in self.vector)
                    
                    
                    if self.obstruction == False:
                        if self.gridx >= 1 and self.gridx <= 8:
                            if self.gridy >= 1 and self.gridy <= 8:
                            
                                if self.vector[0] != 0 and self.vector[1] !=0:   
                                    if abs(self.vector[0]) == abs(self.vector[1]):
                                        if board['%s' %(space)].piececolor != self.color:
                                            self.possmoves.append(space)
                                        elif board['%s' %(space)].piececolor == self.color:
                                            self.supportedpieces.append(space)
                                        #print "Valid queen move." # Rook moves to " + destination
                                    else:
                                        pass#print "Queen move invalid" 
                                elif self.vector[0] != 0 and self.vector[1] == 0:
                                    if board['%s' %(space)].piececolor != self.color:
                                        self.possmoves.append(space)
                                    elif board['%s' %(space)].piececolor == self.color:
                                        self.supportedpieces.append(space)
                                    #print "Valid Queen move." # Rook moves to " + destination
                                elif self.vector[1] != 0 and self.vector[0] == 0:
                                    if board['%s' %(space)].piececolor != self.color:
                                        self.possmoves.append(space)
                                    elif board['%s' %(space)].piececolor == self.color:
                                        self.supportedpieces.append(space)
                                    #print "Valid Queen move." # Rook moves to " + destination
                                else:
                                   pass #print "Queen move invalid"
                                
                               
                            else:
                                pass #print "Destination outside of chessboard." # Rook remains at " + ', '.join(str(x) for x in self.position)
                        else:
                            pass
                            #print "Destination outside of chessboard." # Rook remains at " + ', '.join(str(x) for x in self.position)
                    else:
                        pass
                        #print "Destination occupied by piece of same color."
                    self.getGrid()
                    #print 'Position of Queen after attempted move is ' + self.grid
                    #print "\r"
                    j += 1
                i += 1
    

class King(Piece):
      
    def __init__(self, color):
        self.color = color
        self.side = "K"
        self.type = "k"
        self.check = False   
        self.mated = False     
        #if self.position == NULL:
        if self.color == "W":
            self.initialposition = [5,1] 
                          
        elif self.color == "B":
            self.initialposition = [5,8]

        self.position = self.initialposition
        self.getGrid()
        #self.iD= '%sK' %(self.color)
        self.confirmInit()
#return
    def scoutMoves(self):
        global whitecheck
        global blackcheck
        #print blackcheck
        self.possmoves = []
        self.supportedpieces = []
        if self.grid != "Taken":
            i=1
            while i < 9:
                j = 1
                while j < 9:
                    
                    space = coordstoGrid(str(i), str(j))
                    #print space


                    self.gridx= i
                    self.gridy= j
                    self.gridspace = [self.gridx, self.gridy]
                    self.vector = map(sub, self.gridspace, self.position)
                    self.checkObstruction()
                            #print self.gridy
                    #print 'Position of King prior to attempted move was ' + self.grid
                    #print 'Vector of attempted move is ' + ', '.join(str(x) for x in self.vector)
                    
                    if self.obstruction == False:    
                        if self.gridx >= 1 and self.gridx <= 8:
                            if self.gridy >= 1 and self.gridy <= 8:
                                    if abs(self.vector[0]) <=1 and abs(self.vector[1]) <=1: 
                                        if board['%s' %(space)].piececolor != self.color:
                                            self.possmoves.append(space)
                                        elif board['%s' %(space)].piececolor == self.color:
                                            self.supportedpieces.append(space)
                                        #print "Valid King move." # Rook moves to " + destination
                                    elif self. color == "W" and self.hasmoved == False:
                                        if space == "G1" and wkr.hasmoved == False:
                                            if any(t == "F1" for t in blackcheck) or any(t == "G1" for t in blackcheck) or wkk.check == True:
                                                pass
                                            else:
                                                if board['%s' %(space)].piececolor != self.color:
                                                    self.possmoves.append(space)
                                                elif board['%s' %(space)].piececolor == self.color:
                                                    self.supportedpieces.append(space)

                                            #kingside castle
                                        if space == "C1" and wqr.hasmoved == False:
                                            if any(t == "D1" for t in blackcheck) or any(t == "C1" for t in blackcheck) or wkk.check == True or board["B1"].occupancy==True:
                                                pass
                                            else:
                                                if board['%s' %(space)].piececolor != self.color:
                                                    self.possmoves.append(space)
                                                elif board['%s' %(space)].piececolor == self.color:
                                                    self.supportedpieces.append(space)
                                            
                                            #queenside castle
                                    elif self.color == "B" and self.hasmoved == False:
                                        if space == "G8" and bkr.hasmoved == False:
                                            if any(t == "F8" for t in whitecheck) or any(t == "G8" for t in whitecheck) or bkk.check == True:
                                                pass
                                            else:
                                                if board['%s' %(space)].piececolor != self.color:
                                                    self.possmoves.append(space)
                                                elif board['%s' %(space)].piececolor == self.color:
                                                    self.supportedpieces.append(space)
                                            #kingside castle
                                        if space == "C8" and bqr.hasmoved == False:
                                            if any(t == "D8" for t in whitecheck) or any(t == "C8" for t in whitecheck) or bkk.check == True or board["B8"].occupancy==True:
                                                pass
                                            else:
                                                if board['%s' %(space)].piececolor != self.color:
                                                    self.possmoves.append(space)
                                                elif board['%s' %(space)].piececolor == self.color:
                                                    self.supportedpieces.append(space)
                                            #queenside castle
                    j +=1
                i+=1

                         
        
class Knight(Piece):
      
    def __init__(self, color, side):
        self.color = color
        self.side= side
        self.type= "n"
        if self.color == "W":
            if self.side == "Q":
                self.initialposition = [2,1]
                
            elif self.side == "K":
                self.initialposition = [7,1]
            
        elif self.color == "B":
            if self.side == "Q":
                self.initialposition = [2,8]
                
                
            elif self.side == "K":
                self.initialposition = [7,8]
                
        self.position = self.initialposition
        self.getGrid()
        #self.iD= '%s%sN' %(self.color, self.side)
        self.confirmInit()
#return
    def scoutMoves(self):
    	self.possmoves = []
        self.supportedpieces = []
        if self.grid != "Taken":
            i=1
            while i < 9:
                j = 1
                while j < 9:
                    
                    space = coordstoGrid(str(i),str(j))
                    #print space


                    self.gridx= i
                    self.gridy= j
                    self.gridspace = [self.gridx, self.gridy]
                    self.vector = map(sub, self.gridspace, self.position)#print self.gridx
    	        #self.getGrid()
    	           
    	        
    	        #print self.gridy
    	        #print 'Position of Knight prior to attempted move was ' + self.grid
    	        #print 'Vector of attempted move is ' + ', '.join(str(x) for x in self.vector)
    	        
                    
                    if self.gridx >= 1 and self.gridx <= 8:
                        if self.gridy >= 1 and self.gridy <= 8:
                            
                            self.xk=2
                            self.yk=1
                            self.vec1= [self.xk,self.yk]
                            self.mir1= [-self.xk,self.yk]
                            self.vec2= [-self.yk,self.xk]
                            self.mir2= [-self.yk,-self.xk]
                            self.vec3= [-self.xk,-self.yk]
                            self.mir3= [self.xk,-self.yk]
                            self.vec4= [self.yk,-self.xk]
                            self.mir4= [self.yk,self.xk]
                            
                            self.alltransform= [self.vec1,self.mir1,self.vec2,self.mir2,self.vec3,self.mir3,self.vec4,self.mir4] 
                            #print self.vector
                            #print self.alltransform
                        
                            if any(t == self.vector for t in self.alltransform):
                                if board['%s' %(space)].piececolor != self.color:
                                    self.possmoves.append(space)
                                elif board['%s' %(space)].piececolor == self.color:
                                    self.supportedpieces.append(space)		                       # print "Valid knight move." # Rook moves to " + destination
                

                    j +=1
                i +=1 

#initBoard()

#scoutAll()



