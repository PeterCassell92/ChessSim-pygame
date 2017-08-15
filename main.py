from operator import add
from operator import sub
import string
from meld.vc.svk import NULL
from Pieces2 import *
from Tile import Tile

import pygame
import random

global selected


pygame.init()

white= (255,255,255)
black= (0,0,0)
brown = (139,69,19)
dark_brown= (111,54,10)
dark_grey = (20,20,20)
light_grey = (150,150,150)
red = (180,0,0)
light_red = (254,30,30)
green = (34,155,0)
light_green = (0,255,0)
blue = (0,0,155)
yellow = (200, 175, 0)
light_yellow = (254, 254,0)
display_width = 800
display_height = 800
FPS = 10
clock = pygame.time.Clock()

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Chess')
#icon = pygame.image.load()
#pygame.display.set_icon(icon)
pygame.display.update()

button_width = display_width/8
button_height = display_height/12
tile_size = display_width /10
border = (display_width-(tile_size*8))/2


smallfont= pygame.font.SysFont(None, 25)
medfont= pygame.font.SysFont(None, 50)
largefont= pygame.font.SysFont(None, 80)

bking = pygame.image.load('bking.png')
bqueen = pygame.image.load('bqueen.png')
bpawn = pygame.image.load('bpawn.png')
bbishop= pygame.image.load('bbishop.png')
bknight=pygame.image.load('bknight.png')
brook=pygame.image.load('brook.png')
wking = pygame.image.load('wking.png')
wqueen = pygame.image.load('wqueen.png')
wpawn = pygame.image.load('wpawn.png')
wbishop= pygame.image.load('wbishop.png')
wknight = pygame.image.load('wknight.png')
wrook = pygame.image.load('wrook.png')

turn = "W"
selected = ""
movevalidity = False

def gameIntro():
    intro = True
    while intro:
        gameDisplay.fill(white)
        message_to_screen("Welcome to ChessSim", green, -100, "large")
        message_to_screen("Beginning with White take alternate turns to move pieces", black, -30)
        message_to_screen("The game will only accept legal chess moves", black, 10)
        message_to_screen("You win the game by checkmating your opponent", black, 50)
        #message_to_screen("Press C to Continue or Q to Quit", black, 150, "medium")

        for event in pygame.event.get():
                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()
                    elif event.key == pygame.K_c:
                        intro = False
                if event.type == pygame.QUIT :
                    pygame.quit
                    quit()

        


        
        #pygame.draw.rect(gameDisplay, yellow, ((display_width*2/4-button_width/2),(5*display_height/6), button_width,button_height))
        #pygame.draw.rect(gameDisplay, red, ((display_width*3/4-button_width/2),(5*display_height/6), button_width,button_height))

                #if (display_width/4-button_width/2) + button_width >= cur[0] > (display_width/4-button_width/2)  and (5*display_height/6) + button_height >= cur[1] > (5*display_height/6):
    #       pygame.draw.rect(gameDisplay, light_green, ((display_width/4-button_width/2),(5*display_height/6), button_width,button_height))
        #else:
        #   pygame.draw.rect(gameDisplay, green, ((display_width/4-button_width/2),(5*display_height/6), button_width,button_height))
        



        button("Start", (display_width/4-button_width/2), (5*display_height/6), button_width, button_height, light_green, green, "Play")
        button("Controls", (display_width*2/4-button_width/2), (5*display_height/6),button_width, button_height, light_yellow, yellow)
        button("Quit",(display_width*3/4-button_width/2), (5*display_height/6),button_width, button_height, light_red, red, "Quit")


        pygame.display.update()
        clock.tick(5)
def pause():
    paused = True
    message_to_screen("Paused", black, -100, "large")
    message_to_screen("Press C to continue or Q to quit ", black, -30)
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_c:
                    paused = False
            if event.type == pygame.QUIT :
                pygame.quit
                quit()

        #gameDisplay.fill(white)
        

        clock.tick(10)


def turndisplay(turn):
    if turn == "W":
        text = smallfont.render("It is White's turn", True, black)
    if turn == "B":
        text = smallfont.render("It is Black's turn", True, black)
    gameDisplay.blit(text, (0,0))

def text_Objects(text, color, size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "medium":
        textSurface = medfont.render(text, True, color)
    elif size == "large":
        textSurface = largefont.render(text, True, color)
    return textSurface, textSurface.get_rect()

def text_to_button(msg, x, y, width, height, color = black, size="small"):
    textSurf, textRect = text_Objects(msg, color, size)
    textRect.center = (x + width/2), (y+height/2)
    gameDisplay.blit(textSurf,textRect)

def message_to_screen(msg, color,y_displace =0, size = "small"):
    #screen_text = font.render(msg, True, color)
    #gameDisplay.blit(screen_text, [display_width/4, display_height/2])
    
    textSurf, textRect = text_Objects(msg, color, size)
    textRect.center = (display_width/2), (display_height/2) + y_displace
    gameDisplay.blit(textSurf,textRect)
    
def button(msg, x, y, width, height, activecolor, inactivecolor, action = None):
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    #print click
    if x+width > cur[0] > x and y+height >cur[1]> y:
            pygame.draw.rect(gameDisplay, activecolor, (x,y, width,height))
            if click[0] == 1:
                if action == "Play":
                    gameLoop()
                if action == "Controls":
                    pass
                if action == "Quit":
                    pygame.quit
                    quit()
    else:
        pygame.draw.rect(gameDisplay, inactivecolor, (x,y, width,height))

    text_to_button(msg, x,y,width,height)

def square(coordinates , x, y, width, height, activecolor, inactivecolor):
    global selected
    global turn
    global whitecheck
    global blackcheck
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    #print click

    if x+width > cur[0] >= x and y+height >cur[1]>= y:
        pygame.draw.rect(gameDisplay, activecolor, (x,y, width,height))                   

        if click[0] == 1:
            for piece in piecedict:
                if piece.iD == board['%s' %(coordinates)].pieceID:
                    if piece.color == turn:
                        selected = coordinates

                        print "Selected %s" %(coordinates)
                        #print board['%s' %(coordinates)].piececolor
        if click[2] == 1 and selected != coordinates and selected != "":
            destinationselect = coordinates
            print 
            for piece in piecedict:
                if piece.iD == board['%s' %(selected)].pieceID:
                    piece.moveTo('%s' %(destinationselect))

                    #print piece.movevalidity
            for piece in piecedict:
                if piece.movevalidity == True:
                    #print "Move Validated"
                    if turn == "W":
                        turn = "B"
                        piece.hasmoved = True
                    elif turn == "B":
                        turn = "W"
                        piece.hasmoved = True
                    #print turn
                    selected = ""
                    piece.movevalidity = False
            
    else:
        pygame.draw.rect(gameDisplay, inactivecolor, (x,y, width,height))


    for piece2 in piecedict:
        #piece2.getGrid()
        #print piece2.grid
        if piece2.grid == selected:
            if any(t == coordinates for t in piece2.possmoves):
                #print board['%s' %(coordinates)].piececolor
                #print board['%s' %(selected)].piececolor
                if piece2.color == "W" and board['%s' %(coordinates)].piececolor == "B" :
                    pygame.draw.rect(gameDisplay, red, (x,y, width,height))
                elif piece2.color == "B" and board['%s' %(coordinates)].piececolor == "W" :
                    pygame.draw.rect(gameDisplay, red, (x,y, width,height))
                else:
                    pygame.draw.rect(gameDisplay, light_green, (x,y, width,height))

    if selected == coordinates:
        pygame.draw.rect(gameDisplay, yellow, (x+3,y+3, 74, 2))
        pygame.draw.rect(gameDisplay, yellow, (x+3,y+3, 2, 74))
        pygame.draw.rect(gameDisplay, yellow, (x+75,y+3, 2, 74))
        pygame.draw.rect(gameDisplay, yellow, (x+3,y+75, 74, 2))

    for piece in piecedict:
        if piece.iD == board['%s' %(coordinates)].pieceID:
            if piece.type == "k":
                if piece.color == "B":
                    gameDisplay.blit(bking,(x,y))
                else:
                    gameDisplay.blit(wking, (x,y))
            if piece.type == "q":
                if piece.color == "B":
                    gameDisplay.blit(bqueen,(x,y))
                else:
                    gameDisplay.blit(wqueen, (x,y))
            if piece.type == "p":
                if piece.color == "B":
                    gameDisplay.blit(bpawn,(x,y))
                else:
                    gameDisplay.blit(wpawn, (x,y))
            if piece.type == "n":
                if piece.color == "B":
                    gameDisplay.blit(bknight,(x,y))
                else:
                    gameDisplay.blit(wknight, (x,y))
            if piece.type == "b":
                if piece.color == "B":
                    gameDisplay.blit(bbishop,(x,y))
                else:
                    gameDisplay.blit(wbishop, (x,y))
            if piece.type == "r":
                if piece.color == "B":
                    gameDisplay.blit(brook,(x,y))
                else:
                    gameDisplay.blit(wrook, (x,y))


def gameLoop():

    selected= ""
    gameExit= False
    gameOver= False

    #wqq.showPotential()

    while not gameExit:
        if gameOver == True:
            message_to_screen("Game Over", red, -100, "large")
            message_to_screen(" Press C to continue or Q to quit", black, 50, "medium")
            pygame.display.update()

        while gameOver == True:
            #gameDisplay.fill(white)            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_q:
                        gameOver = False
                        gameExit = True
                    elif event.key == pygame.K_c:
                        gameLoop()
                if event.type == pygame.QUIT :
                    gameOver = False
                    gameExit = True



        for event in pygame.event.get():
            eventlog = event
           # print eventlog
            if eventlog.type == pygame.QUIT :
                gameExit = True
            if eventlog.type == pygame.KEYDOWN :
                if event.key == pygame.K_ESCAPE:
                    pause()
        
        gameDisplay.fill(blue)

        i=1
        while i < 9:
            j = 1
            while j < 9:
              
                if i % 2 ==0:
                    if j % 2 == 0:
                        tilecolor = white
                        activetilecolor = light_grey
                    else:
                        tilecolor = brown
                        activetilecolor = dark_brown
                else:
                    if j % 2 == 0:
                        tilecolor = brown
                        activetilecolor = dark_brown
                    else:
                        tilecolor = white
                        activetilecolor = light_grey
             
                square(coordstoGrid(str(i),str(j)), border+(tile_size*(i-1)), border+7*tile_size -(tile_size*(j-1)), tile_size,tile_size, activetilecolor, tilecolor)      
                j += 1
            i += 1
        
        turndisplay(turn)
        pygame.display.update()
        clock.tick(FPS)
gameIntro()

gameLoop()

pygame.quit
quit()