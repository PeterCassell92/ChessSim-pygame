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
    characters = str.maketrans("12345678", "ABCDEFGH")
    text = xcoordinate.translate(characters)
    gridoutput= text + str(ycoordinate)
    return gridoutput

def postoGrid(mylist):
    gridoutput = coordstoGrid(str(mylist[0]),str(mylist[1]))
    return gridoutput

def gridtoCoords(grid):
    griddy = grid
    characters = str.maketrans("ABCDEFGH", "12345678")
    letcon = griddy.translate(characters)
    pos = [int(letcon[0]), int(letcon[1])]
    return pos

def addIntArrays(arr1,arr2):
    result = map(lambda n1, n2: int(n1+n2), arr1, arr2)
    return list(result)

def subtractIntArrays(arr1,arr2):
    if len(arr1) != len(arr2):
        return
    else:
        subtractedArray = []
        for x in range(len(arr1)):
            subtractedArray.append(int(arr1[x] - arr2[x]))
        return subtractedArray

def oppColor(color):
    if color == "W":
        return "B"
    if color == "B":
        return "W"

def getPieceByGrid(pieces, grid):
    print(grid)
    for piece in pieces:
        if piece.grid != "Taken":
            if piece.getGrid() == grid.upper():
                return piece