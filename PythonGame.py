import random
import sys
import pygame
from pygame.locals import *

FPS = 32
SCREENWIDTH = 942
SCREENHEIGHT = 728
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
PLAYER = 'bomber-sprite1.png'
BACKGROUND = 'back7702.jpg'
offset = 0
sec = 0
mint = 0

def welcomeScreen():
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    asteroid1x = int(SCREENWIDTH/2)
    asteroid1y = 0
    asteroid2x = int(SCREENWIDTH * 0.45)
    asteroid2y = int(SCREENHEIGHT - GAME_SPRITES['asteroid'][1].get_height())
    asteroid3x = int(asteroid1x + GAME_SPRITES['asteroid'][0].get_width())
    offset = int(1.2* GAME_SPRITES['player'].get_height())
    asteroid3y = int(SCREENHEIGHT - GAME_SPRITES['asteroid'][1].get_height() - offset - GAME_SPRITES['asteroid'][2].get_height())

    basex = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return

            else:
                SCREEN.blit(GAME_SPRITES['background'], (0,0))
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
                SCREEN.blit(GAME_SPRITES['asteroid'][0], (asteroid1x, asteroid1y))
                SCREEN.blit(GAME_SPRITES['asteroid'][1], (asteroid2x, asteroid2y))
                SCREEN.blit(GAME_SPRITES['asteroid'][2], (asteroid3x, asteroid3y))
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def randomAsteroidGeneration():
    playerHeight = GAME_SPRITES['player'].get_height()
    y_offset = random.randint(0,int(1.2*(SCREENHEIGHT - playerHeight)))
    ast = SCREENHEIGHT - y_offset - GAME_SPRITES['asteroid'][0].get_height()
    if ast > 0:
        ast1y = random.randint(0,ast)
    else:
        ast1y = ast 
    ast2y = random.randint(offset+playerHeight, SCREENHEIGHT + 10)
    ast3y = random.randint(0, SCREENHEIGHT)
    x_position = SCREENWIDTH + 10
    asteroidPosition = [
        {'x': x_position, 'y': ast1y},
        {'x': x_position, 'y': ast2y},
        {'x': x_position + SCREENWIDTH/2, 'y': ast3y}
    ]
    return asteroidPosition

    

def collisionTheory(playerx, playery, ast1, ast2, ast3):
    if playery > SCREENHEIGHT :
        playery = SCREENHEIGHT
        return False

    if playery < 0:
        playery = 0
        return False

    for x in ast1:
        astHeight = GAME_SPRITES['asteroid'][0].get_height()
        if(playery < astHeight + x['y'] and abs(playerx - x['x']) < GAME_SPRITES['asteroid'][0].get_width()):
            #print(f"1st asteroid")
            return True

    for x in ast2:
        if (playery + GAME_SPRITES['player'].get_height() > x['y'] and abs(playerx - x['x']) < GAME_SPRITES['asteroid'][1].get_width()):
            #print(f"2nd asteroid")
            return True

    for x in ast3:
        astHeight = GAME_SPRITES['asteroid'][2].get_height()
        if ((x['y'] < playery < x['y'] + astHeight) and abs(playerx - x['x']) < GAME_SPRITES['asteroid'][2].get_width()):
            #print(f"3rd asteroid")
            return True
    return False

def pythonGame():
    score1 = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENHEIGHT/2)
    ast_position1 = randomAsteroidGeneration()
    ast_position2 = randomAsteroidGeneration()
    ast1 = [
        {'x': SCREENWIDTH+200, 'y': ast_position1[0]['y']}
    ]
    ast2 = [
        {'x': SCREENWIDTH+200, 'y': ast_position1[1]['y']}
    ]
    posi_addition = max(GAME_SPRITES['asteroid'][0].get_width(), GAME_SPRITES['asteroid'][1].get_width())
    
    ast3 = [
        {'x': ast1[0]['x']+ posi_addition + 100, 'y': ast_position1[1]['y']}
    ]

    ast1.append({'x': ast3[0]['x'] + GAME_SPRITES['asteroid'][2].get_width() + 100 , 'y' : ast_position2[0]['y']})
    ast2.append({'x': ast3[0]['x'] + GAME_SPRITES['asteroid'][2].get_width() + 100 , 'y' : ast_position2[1]['y']})
    ast3.append({'x': ast1[1]['x']+ posi_addition + 100, 'y': ast_position2[1]['y']})

    
    astVelX = -8

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8 
    playerFlapped = False
    sec = 0
    mint = 0 

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True

        collision = collisionTheory(playerx, playery, ast1, ast2, ast3)
        sec += 1
        if(sec == 60):    
                sec = 0    
                mint += 1
        if collision:
            
            print(f"{mint}:{sec}")
            return
        
        

        
        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False

        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, SCREENHEIGHT - playery - playerHeight)

        for x,y,z in zip(ast1, ast2, ast3):
            x['x'] += astVelX
            y['x'] += astVelX
            z['x'] += astVelX

        if 0 < ast1[0]['x'] <5 :
            newAst = randomAsteroidGeneration()
            ast1.append(newAst[0])
            ast2.append(newAst[1])
            ast3.append(newAst[2])

        if ast1[0]['x'] < -GAME_SPRITES['asteroid'][0].get_width():
            ast1.pop(0)

        if ast2[0]['x'] < -GAME_SPRITES['asteroid'][1].get_width():
            ast2.pop(0)
        
        if ast3[0]['x'] < -GAME_SPRITES['asteroid'][2].get_width():
            ast3.pop(0)

        SCREEN.blit(GAME_SPRITES['background'], (0,0))

        for x,y,z in zip(ast1, ast2, ast3):
            SCREEN.blit(GAME_SPRITES['asteroid'][0], (x['x'], x['y']))
            SCREEN.blit(GAME_SPRITES['asteroid'][1], (y['x'], y['y']))
            SCREEN.blit(GAME_SPRITES['asteroid'][2], (z['x'], z['y']))
        
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))

        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__== "__main__":
    pygame.init()
    FPSCLOCK = pygame.time.Clock()

    GAME_SPRITES['asteroid'] = (
        pygame.image.load('asteroid11.png').convert_alpha(),
        pygame.image.load('asteroid21.png').convert_alpha(),
        pygame.image.load('asteroid31.png').convert_alpha()
    )

    #GAME_SPRITES['base'] = pygame.image.load('base123.jpg').convert_alpha()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert_alpha()

    while True:
        welcomeScreen()
        pythonGame()
