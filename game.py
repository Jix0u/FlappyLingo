import cv2
import sys 
import pygame
import numpy as np

from gest import MH
from pygame.locals import * 


cap = cv2.VideoCapture(0) 
hand = MediaPipeHand(static_image_mode=False, max_num_hands=1)

FPS = 32
SCREEN = pygame.display.set_mode((289, 511))
PLAYER = 'images/player.png'
BACKGROUND = 'images/bg.png'
PIPE = 'images/pipe.png'

def wel():
    """
    Shows welcome images on the screen
    """

    playerx = int(289/5)
    playery = int((511 - spirts['player'].height())/2)
    while True:
        for event in pygame.event.get():

            if event.type==pygame.KEYDOWN and (event.key==pygame.K_SPACE or event.key == pygame.K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0), ['player'], ['bg'])    
                pygame.display.update()


def game():
     pvx = -4

    pvy = -9
    pmv = 10
    pmvv = -8
    pacy = 1

    pfa = -9
    pf = False

    score = 0
    playery = int(SCREENWIDTH/2)

    np = randp()
    np2 = randp()

    pp = [
        {'x': 580, 'y':np[0]['y']},
        {'x': 580+, 'y':np2[0]['y']},
    ]

    lp = [
        {'x': 580, 'y':np[1]['y']},
        {'x': 580, 'y':np2[1]['y']},
    ]


    while True:

        cap = cv2.VideoCapture(0)
        # print("hi ok")
        while cap.isOpened():
            success, image = cap.read()            
            if not success:
                print("Ignoring empty")
                continue
            # print("hi sigh")
            res = hands.run(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            hshape = ""

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if py > 0:
                    pvy = pfa
                    pf = True
                    gs['wing'].play()


        ct = col(playerx, playery, upperPipes, lowerPipes)
        if ct: 
            return     


            pvy += pacy

        if pf:
            pf = False            
        ph = gs['player'].get_height()
        py = py + min(playerVelY, ground - playery - ph)

        if 0<up[0]['x']<5:
            np = grp()
            up.append(np[0])
            lp.append(np[1])

        # if the pipe is out of the screen, remove it
        if up[0]['x'] < -gs['pipe'][0].get_width():
            up.pop(0)
            lp.pop(0)
        
        # Lets blit our sprites now
        sc.blit(gs['background'], (0, 0))
        for up, lp in zip(up, lp):
            sc.blit(gs['pipe'][0], (up['x'], up['y']))
            sc.blit(gs['pipe'][1], (lp['x'], lp['y']))

        sc.blit(gs['base'], (basex, g))
        scs.blit(gs['player'], (playerx, playery))
        dig = [int(x) for x in list(str(score))]
        w = 0
        for digit in myDigits:
            width += gs['num'][digit].gw()
        Xoffset = (200 - w)/2

        for digit in myDigits:
            sc.blit(gs['num'][digit], (of, 200*0.12))
            Xoffset += gs['num'][digit].gw()
        pygame.display.update()



def rand():

    pipe = [
        {'x': pipeX, 'y': -y1}, #upper Pipe
        {'x': pipeX, 'y': y2} #lower Pipe
    ]
    return pipe


if __name__ == "__main__":
    pygame.init() 
    pygame.display.set_caption('Flappy Bird')
    gs['numbers'] = ( 
        pygame.image.load('images/0.png').convert_alpha(),
        pygame.image.load('images/1.png').convert_alpha(),
        pygame.image.load('images/2.png').convert_alpha(),
        pygame.image.load('images/3.png').convert_alpha(),
        pygame.image.load('images/4.png').convert_alpha(),
    )

    gs['base'] =pygame.image.load('images/base.png').convert_alpha()
    gs['pipe'] =(pygame.transform.rotate(pygame.image.load(pp).convert_alpha(), 180), 
    pygame.image.load(pp).convert_alpha()
    )
    gs['background'] = pygame.image.load(bg).convert()
    gs['player'] = pygame.image.load(player).convert_alpha()

    gs['point'] = pygame.mixer.Sound('images/audio/point.wav')
    gs['point'] = pygame.mixer.Sound('images/audio/hello.wav')
    gs['point'] = pygame.mixer.Sound('images/audio/how are.wav')
    gs['point'] = pygame.mixer.Sound('images/audio/you.wav')
    gs['point'] = pygame.mixer.Sound('images/audio/what is up.wav')
    gs['point'] = pygame.mixer.Sound('images/audio/nice to meet you.wav')
    gs['point'] = pygame.mixer.Sound('images/audio/my name is.wav')
    gs['point'] = pygame.mixer.Sound('images/audio/goodbye.wav')





    while True:
        wel()
        game()

   

   

    