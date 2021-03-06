#!/usr/bin/python
from operator import add
from operator import sub
import os
import string
import sys

from gridfunctions import findLDV, coordstoGrid, postoGrid, gridtoCoords, oppColor, getPieceByGrid

from Pieces3 import initBoard, scoutAll
from chessapi import createGame, movePiece, moveAI, checkGameover

from Tile import Tile
from spriteclasses import BaseSprite, ImageSprite

import pygame
import random

initBoard()
scoutAll()

from Pieces3 import piecedict, board, wkk, bkk
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
light_blue = (173, 216, 230)
tint_blue = (162, 172, 182)

yellow = (200, 175, 0)
light_yellow = (254, 254,0)
display_width = 800
display_height = 800
FPS = 10
clock = pygame.time.Clock()

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Chess')
pygame.display.update()

button_width = display_width/8
button_height = display_height/12
tile_size = display_width /10
border = (display_width-(tile_size*8))/2


smallfont= pygame.font.SysFont(None, 25)
medfont= pygame.font.SysFont(None, 50)
largefont= pygame.font.SysFont(None, 80)

piecesfolder = os.getcwd()+ '/img/pieces/'

bking = pygame.image.load(piecesfolder + 'bking.png')
bqueen = pygame.image.load(piecesfolder + 'bqueen.png')
bpawn = pygame.image.load(piecesfolder + 'bpawn.png')
bbishop= pygame.image.load(piecesfolder + 'bbishop.png')
bknight=pygame.image.load(piecesfolder + 'bknight.png')
brook=pygame.image.load(piecesfolder + 'brook.png')
wking = pygame.image.load(piecesfolder + 'wking.png')
wqueen = pygame.image.load(piecesfolder + 'wqueen.png')
wpawn = pygame.image.load(piecesfolder + 'wpawn.png')
wbishop= pygame.image.load(piecesfolder + 'wbishop.png')
wknight = pygame.image.load(piecesfolder + 'wknight.png')
wrook = pygame.image.load(piecesfolder + 'wrook.png')

selected = ""
movevalidity = False

#API

gamestate = {
    "vsAI" : False,
    "AIColor": "B",
    "gameID" : "",
    "player": {
        "black": "Human",
        "white": "Human"
    },
    "turn": "W",
    "moveRecord": []
}


def gameIntro(gamestate):
    backgroundimg = ImageSprite(0 , 0, os.getcwd()+ '/img/other/chesspixelimg.png')
    chesstext = ImageSprite( 120, 75, os.getcwd()+ '/img/other/chessfont.png')
    introsprites = pygame.sprite.Group()
    introsprites.add(backgroundimg, chesstext)

    intro = True
    while intro:

        gameDisplay.fill(white)
        introsprites.draw(gameDisplay)
    
        for event in pygame.event.get():
                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit() #this is a better way of quitting a program than quit(). (library always exists)
                    elif event.key == pygame.K_c:
                        intro = False
                if event.type == pygame.QUIT :
                    pygame.quit()
                    sys.exit() #this is a better way of quitting a program than quit(). (library always exists)

        button("Start", (display_width/4-button_width/2), (4*display_height/6), button_width, button_height, light_green, green, "Play", gamestate)

        modeTxt = "Player vs AI" if gamestate.get('vsAI') else "Local Mutiplayer"
        button(modeTxt, (display_width/4-button_width/2), (4.8*display_height/6), button_width, button_height/2, light_yellow, yellow, "ToggleAI", gamestate)
        button("Quit",(display_width*3/4-button_width/2), (4*display_height/6),button_width, button_height, light_red, red, "Quit", gamestate)

        if gamestate.get("vsAI"):
            button(gamestate.get("AIColor"), ((display_width/4)-button_width/2), (5*display_height/6), button_width/2, button_height/2, light_blue, tint_blue, "ToggleAIColor", gamestate)

        pygame.display.update()
        clock.tick(5)
    return gamestate
        
def pause(gamestate):
    paused = True
    message_to_screen("Paused", black, -100, "large")
    message_to_screen("Press C to continue or Q to quit ", black, -30)
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit() #this is a better way of quitting a program than quit(). (library always exists)
                elif event.key == pygame.K_c:
                    paused = False
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit() #this is a better way of quitting a program than quit(). (library always exists)
        

        clock.tick(10)
    return gamestate

def toggleTurn(gamestate):
    if gamestate.get("turn") == "W":
        gamestate.update({"turn" : "B"})
    elif gamestate.get("turn") == "B":
        gamestate.update({"turn": "W"})
    return gamestate

def turndisplay(turn):
    if turn == "W":
        # text = smallfont.render("It is White's turn", True, black)
        message_to_screen("White's Turn", white, -(display_height/2) +60, "medium")
    if turn == "B":
        # text = smallfont.render("It is Black's turn", True, black)
        message_to_screen("Black's Turn", white, -(display_height/2)+60, "medium")
        pygame.display.update()

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
     
    textSurf, textRect = text_Objects(msg, color, size)
    textRect.center = (display_width/2), (display_height/2) + y_displace
    gameDisplay.blit(textSurf,textRect)
    
def button(msg, x, y, width, height, activecolor, inactivecolor, action , gamestate):
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+width > cur[0] > x and y+height >cur[1]> y:
            pygame.draw.rect(gameDisplay, activecolor, (x,y, width,height))
            if click[0] == 1:
                if action == "ToggleAI":
                    gamestate.update({"vsAI": not (gamestate.get("vsAI")) })

                    print(" toggled AI. state now equals " + str(gamestate.get("vsAI")))

                if action == "Play":
                    if (gamestate.get("vsAI")): gamestate.update({'gameID' : createGame()})
                    print("ID= " + gamestate.get("gameID"))
                    gameLoop(gamestate)
                if action == "Quit":
                    pygame.quit()
                    sys.exit()
                if action == "ToggleAIColor":
                    gamestate.update({'AIColor': oppColor(gamestate.get('AIColor'))})
                    print("AI is playing " +gamestate.get('AIColor'))
    else:
        pygame.draw.rect(gameDisplay, inactivecolor, (x,y, width,height))

    text_to_button(msg, x,y,width,height)
    return gamestate

def square(coordinates , x, y, width, height, activecolor, inactivecolor, gamestate):
    global selected

    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+width > cur[0] >= x and y+height >cur[1]>= y:
        pygame.draw.rect(gameDisplay, activecolor, (x,y, width,height))                   

        if click[0] == 1:
            for piece in piecedict:
                if piece.iD == board['%s' %(coordinates)].pieceID:
                    if piece.color == gamestate.get("turn"):
                        selected = coordinates

                        print("Selected %s" %(coordinates))
                        
        if click[2] == 1 and selected != coordinates and selected != "":
            destinationselect = coordinates
            for piece in piecedict:
                if piece.iD == board['%s' %(selected)].pieceID:
                    piece.moveTo('%s' %(destinationselect))
               
            for piece in piecedict:
                if piece.movevalidity == True and selected !="":

                    if gamestate['vsAI'] == True:
                        movePiece(selected, destinationselect, gamestate['gameID'])
                    
                    toggleTurn(gamestate)

                    piece.hasmoved = True
                    
                    selected = ""
                    piece.movevalidity = False
            
    else:
        pygame.draw.rect(gameDisplay, inactivecolor, (x,y, width,height))


    for piece2 in piecedict:
        
        if wkk.mated == False and bkk.mated == False:
            if piece2.grid == selected:
                if any(t == coordinates for t in piece2.possmoves):
                   
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
    return gamestate

def gameLoop(gamestate):

    selected= ""
    gameExit= False
    gameOver= False
    while not gameExit:
        

        if gameOver == True:
            message_to_screen("Checkmate", red, -100, "large")
            message_to_screen(" Press Q to quit", black, 50, "medium")
            pygame.display.update()

        while gameOver == True:        
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_q:
                        gameOver = False
                        gameExit = True
                    elif event.key == pygame.K_c:
                        bkk.mated= False 
                        wkk.mated= False
                        initBoard()
                        scoutAll()
                        gameIntro(gamestate)
                if event.type == pygame.QUIT :
                    gameOver = False
                    gameExit = True

        for event in pygame.event.get():
            eventlog = event
            if eventlog.type == pygame.QUIT :
                gameExit = True
            if eventlog.type == pygame.KEYDOWN :
                if event.key == pygame.K_ESCAPE:
                    pause()
        if bkk.mated== True or wkk.mated == True:
            gameOver=True
        gameDisplay.fill(blue)

        #make an AI move if it is the AIs turn it is not a gameover condition
        if gamestate.get('vsAI') and (gamestate.get('turn') == gamestate.get('AIColor')) and (checkGameover(gamestate.get('gameID')) == 'game continues'):
            print(gamestate.get('gameID'))
            currentGrid, targetGrid = moveAI(gamestate.get('gameID'))

            aiselected = getPieceByGrid(piecedict, currentGrid)
            print("AI Selected " + aiselected.type)
            aiselected.moveTo(targetGrid.upper())
            toggleTurn(gamestate)

        #big messy block for drawing each square on the chessboard
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
             
                square(coordstoGrid(str(i),str(j)), border+(tile_size*(i-1)), border+7*tile_size -(tile_size*(j-1)), tile_size,tile_size, activetilecolor, tilecolor, gamestate)      
                j += 1
            i += 1
        
        turndisplay(gamestate.get("turn"))
        pygame.display.update()

        clock.tick(FPS)
    return gamestate

gameIntro(gamestate)

#gameLoop()

pygame.quit()
sys.exit()
