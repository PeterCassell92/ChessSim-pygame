import string

def findLDV(vector):
    if vector[0] != 0 and vector[1] == 0:
            minvector = [x / abs(vector[0]) for x in vector]           
                
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

def postoGrid(List):
    gridoutput = coordstoGrid(str(List[0]),str(List[1]))
    return gridoutput

def gridtoCoords(grid):
    griddy = grid
    characters = string.maketrans("ABCDEFGH", "12345678")
    letcon = griddy.translate(characters)
    pos = [int(letcon[0]), int(letcon[1])]
    return pos
