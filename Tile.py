class Tile(object):
    def __init__(self, notation):
        self.occupancy= False
        self.piececolor= "None"
        self.pieceID= "None"
        self.ghost = False
    
    def occupy(self):
        self.occupancy = True
                
    def unoccupy(self):
        self.occupancy= False
        self.piececolor= "None"
        self.pieceID="None"
        