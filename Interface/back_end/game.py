#Assets from : https://github.com/samuelcust/flappy-bird-assets
#Ref Flappy bird code from : https://www.geeksforgeeks.org/how-to-make-flappy-bird-game-in-pygame/
#imports
from typing import Any
import cv2
import sys
import random
import pygame
import numpy as np
import mediapipe as mp
from pygame.locals import * 
import gest
import matplotlib.pyplot as plt
import os as o


# Global Variables
# W = 1440 #width
# H = 800 #height

GAME_SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_info = pygame.display.Info()
W = screen_info.current_w
H = screen_info.current_h

FLOOR = H * 0.8 #floor dimensions
SPRITES = {}
AUDIO = {}
FPS = 40
#asset sprites
MIDFLAP = 'assets/sprites/orangebird-midflap.png'
FLAPDOWN = 'assets/sprites/orangebird-downflap.png'
FLAPUP = 'assets/sprites/orangebird-upflap.png'
BACKGROUND = 'assets/sprites/background.png'
PIPE = 'assets/sprites/pipe.png'
GAMEOVER = 'assets/sprites/gameover.png'

# Load Classes for Hand Tracking
gg = gest.States(5)
cap = cv2.VideoCapture(4) # By default webcam is index 0
hand = gest.MH(buffer_size=100)
showvid = True
# high_score = 0
plt.switch_backend('Agg')
bird_sprites = [MIDFLAP, FLAPDOWN, FLAPUP]


def welcomeGAME_SCREEN() -> None:
    """
    Display the welcome screen for the game.

    :return: None
    """
    bird_index = 0

    birdx = int((W -SPRITES['bird'].get_width())/2)
    birdy = int((H - SPRITES['bird'].get_height())/2)
    titlex = int((W - SPRITES['title'].get_width())/2)
    titley = int(H*0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.type==KEYDOWN and event.key == K_UP:
                return
            else:
                bird_index += 1
                bird_index %= 3
                SPRITES['bird'] = pygame.image.load(bird_sprites[bird_index]).convert_alpha()
                GAME_SCREEN.blit(SPRITES['background'], (0, 0)) 
                GAME_SCREEN.blit(SPRITES['base'], (basex, FLOOR))
                GAME_SCREEN.blit(SPRITES['bird'], (birdx, birdy))    
                GAME_SCREEN.blit(SPRITES['title'], (titlex,titley ))  
                
                
                pygame.display.update()
                clockie.tick(FPS)


def mainGAME_SCREEN() -> None:
    """
    Main game loop for FlappyLingo.

    :return: None
    """
    bird_index = 0
    font = pygame.font.Font("assets/fonts/ka1.TTF", 30)  # You can change the font and size here
    string_list = ["A", "hello", "B", "C", "where", "I love you", "me"]
    signLanguage = random.choice(string_list)
    text = font.render(signLanguage, True, (255, 255, 255))  # Text, antialiasing, color
    startingText = font.render("Make the sign", True, (255, 255, 255)) 
    lookLeftText = font.render("PAUSED look left", True, (255, 255, 255)) 
    score = 0
    endingText = font.render("WRONG SIGN", True, (255, 255, 255)) 
    birdx = int(W/2)+250
    birdy = int(H/2)-200
    basex = 0

    # GAME_SCREEN pipes
    pipeNumero1 = PipeGenerator()
    pipeNumero2 = PipeGenerator()

    # TOP PIPES
    topPipes = [
        {'x': W+200, 'y':pipeNumero1[0]['y']},
        {'x': W+200+400, 'y':pipeNumero2[0]['y']},
    ]
    # BOT PIPES
    botPipes = [
        {'x': W+200, 'y':pipeNumero1[1]['y']},
        {'x': W+200+400, 'y':pipeNumero2[1]['y']},
    ]

    pipeVelX = -4

    paused = False
    paused_text = None 
    correctGest = False
    frame = 0
    wrongC = 0
    script_directory = o.path.dirname(o.path.abspath(__file__))
    data_folder_path = o.path.join(script_directory, "data_folder")
    high_score_file_path = o.path.join(script_directory,"high_score.txt")

    model = gest.Train(data_folder_path)

    # Load previous high score if available
    try:
        with open(high_score_file_path, "r") as file:
            high_score = int(file.read())
    except FileNotFoundError:
        # If the file doesn't exist, initialize high score to 0
        high_score = 0

    while True:
        if score > high_score:
            high_score = score
        
        # Hand tracking from image
        try:
            # Flip image for 3rd person view
            cap = cv2.VideoCapture(0)
            success, image = cap.read()
            if not success:
                print("Ignoring empty")
                continue
            res = hand.run(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            hshape = ""
            

            if hand.his:
                hshape = model.getshape(hand.his[-1])
                gg.run(hshape, hand.his[-1], hand.his)

                # Display the frame
                
                # print(f"state={gg.state}, click={gg.ic}, shape={hshape}")
            if showvid:
                # Overlaying the mediapipe "skeleton"
                # print("hi lmfaooooo")
                img = hand.drawlol(image, res, model)

                resized_game_img = np.fliplr(img)
                resized_game_img = np.rot90(resized_game_img)
                resized_game_img = cv2.cvtColor(resized_game_img, cv2.COLOR_BGR2RGB)
                surf = pygame.surfarray.make_surface(resized_game_img)
                DFLT_IMG_SZ = (500, 300)
                # Scale the image to your needed size
                resized_game_img = pygame.transform.scale(surf, DFLT_IMG_SZ)


            if cv2.waitKey(5) & 0xFF == 27:
                break

        except:        
            cv2.destroyAllWindows()
            hand.close()
            cap.release()
            print("\n>>> Error caught. Program closed gracefully. <<<\n")
            raise

        for event in pygame.event.get():
            if event.type==KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_p:
                paused = not paused


        #HIT SOMETHING
        boomHit = OutOfBounds(birdx, birdy, topPipes, botPipes) 
        if boomHit: 
            return     

        #check for score
        birdMIDDLE = birdx + SPRITES['bird'].get_width()/2
        for pipe in topPipes:
            pipeMIDDLE = pipe['x'] + SPRITES['pipe'][0].get_width()/2
            pipeHeight = SPRITES['pipe'][0].get_height()
            if 0<topPipes[0]['x']< 900:
                birdy = pipeHeight + topPipes[1]['y'] + 40
            if not correctGest and pipeMIDDLE - 8 <= birdMIDDLE < pipeMIDDLE +4:
                paused_text = text  # Set paused_text to the text you want to display
                paused = True

            if pipeMIDDLE<= birdMIDDLE < pipeMIDDLE +4:
                score +=1
                print(f"Your score is {score}") 
                AUDIO['point'].play()

        if not paused:

            # left goes the pipe
            for upperPipe , lowerPipe in zip(topPipes, botPipes):
                upperPipe['x'] += pipeVelX
                lowerPipe['x'] += pipeVelX

            # additional pipe
            if 0<topPipes[0]['x']< 1200 and len(topPipes) < 2:
                newpipe = PipeGenerator()
                topPipes.append(newpipe[0])
                botPipes.append(newpipe[1])

            # remove the pipe
            if topPipes[0]['x'] < 550:
                topPipes.pop(0)
                botPipes.pop(0)

            
            GAME_SCREEN.blit(SPRITES['background'], (0, 0))
            for upperPipe, lowerPipe in zip(topPipes, botPipes):
                GAME_SCREEN.blit(SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
                GAME_SCREEN.blit(SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

            GAME_SCREEN.blit(SPRITES['base'], (basex, FLOOR))
            GAME_SCREEN.blit(SPRITES['camera_pane'], (0, 0))
            GAME_SCREEN.blit(SPRITES['title'], (10,700))   

            NUMBERS = [int(x) for x in list(str(score))]
            smallwidth = 0
            for digit in NUMBERS:
                smallwidth += SPRITES['numbers'][digit].get_width()
            toLEFT = (W - smallwidth)/2+300

            for digit in NUMBERS:
                GAME_SCREEN.blit(SPRITES['numbers'][digit], (toLEFT, H*0.12))
                toLEFT += SPRITES['numbers'][digit].get_width()
            bird_index = (bird_index + 1) % 3
            SPRITES['bird'] = pygame.image.load(bird_sprites[bird_index]).convert_alpha()
            GAME_SCREEN.blit(SPRITES['bird'], (birdx, birdy))
            high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))
            GAME_SCREEN.blit(high_score_text, (50, 400))
            # clockie.tick(FPS)
        if correctGest:
            frame+=1
            paused_text = None
            signLanguage = random.choice(string_list)
            text = font.render(signLanguage, True, (255, 255, 255))
            wrongC = 0
        if frame >10:
            correctGest = False
            frame = 0


        if paused_text is not None:
            # GAME_SCREEN.blit(SPRITES['background'], (0, 0))
            toLEFT = (W - smallwidth)/2
            GAME_SCREEN.blit(startingText, (50,500))
            GAME_SCREEN.blit(paused_text, (50,600))

            GAME_SCREEN.blit(lookLeftText, (int(W/2)+200, 130))
            print(hshape, " == ", signLanguage)
            
            if hshape == signLanguage:
                paused = False
                correctGest = True
            else :
                wrongC+=1
                if(wrongC >= 30):
                    AUDIO['die'].play()
                    center_x = (W - SPRITES['gameover'].get_width()) // 2
                    center_y = (H - SPRITES['gameover'].get_height()) // 2

                    for x in range(20):
                        GAME_SCREEN.blit(endingText, (center_x, center_y - 50))
                        GAME_SCREEN.blit(SPRITES['gameover'], (center_x, center_y))
                        pygame.display.update()
                    cap.release()
                    cv2.destroyAllWindows()
                    return
                with open(high_score_file_path, "w") as file:
                    file.write(str(high_score))
        GAME_SCREEN.blit(resized_game_img, (50, 50))
        pygame.display.update()


def OutOfBounds(birdx, birdy, topPipes, botPipes) -> bool:
    """
    Check if the bird has collided with the pipes or gone out of bounds.

    :param birdx: The x-coordinate of the bird.
    :param birdy: The y-coordinate of the bird.
    :param topPipes: List of top pipe dictionaries with 'x' and 'y' coordinates.
    :param botPipes: List of bottom pipe dictionaries with 'x' and 'y' coordinates.
    :return: True if the bird is out of bounds or has collided with a pipe, False otherwise.
    """
    if birdy> FLOOR - 25  or birdy<0:
        AUDIO['die'].play()
        return True
    
    for peep in topPipes:
        pH = SPRITES['pipe'][0].get_height()
        if(birdy < pH + peep['y'] and abs(birdx - peep['x']) < SPRITES['pipe'][0].get_width()-2):
            return True

    for peep in botPipes:
        if (birdy + SPRITES['bird'].get_height() > peep['y']) and abs(birdx - peep['x']) < SPRITES['pipe'][0].get_width():
            return True

    return False

#pipes
def PipeGenerator() -> list[dict[str, Any]]:
    """
    Generate a new pair of top and bottom pipes with random heights.

    :return: A list of dictionaries containing the 'x' and 'y' coordinates for the top and bottom pipes.
    """
    pipeHeight = SPRITES['pipe'][0].get_height()
    leftie = H/3
    yTWO = leftie + random.randrange(0, int(H - SPRITES['base'].get_height()  - 1.2 *leftie))
    pipeX = W
    yONE = pipeHeight - yTWO + leftie
    pipe = [
        {'x': pipeX, 'y': -yONE}, #upper Pipe
        {'x': pipeX, 'y': yTWO} #lower Pipe
    ]
    return pipe


#main
if __name__ == "__main__":

    pygame.init() # Initialize all pygame's modules
    clockie = pygame.time.Clock()
    pygame.display.set_caption('FlappyLingo')
    SPRITES['numbers'] = ( 
        pygame.image.load('assets/sprites/0.png').convert_alpha(),
        pygame.image.load('assets/sprites/1.png').convert_alpha(),
        pygame.image.load('assets/sprites/2.png').convert_alpha(),
        pygame.image.load('assets/sprites/3.png').convert_alpha(),
        pygame.image.load('assets/sprites/4.png').convert_alpha(),
        pygame.image.load('assets/sprites/5.png').convert_alpha(),
        pygame.image.load('assets/sprites/6.png').convert_alpha(),
        pygame.image.load('assets/sprites/7.png').convert_alpha(),
        pygame.image.load('assets/sprites/8.png').convert_alpha(),
        pygame.image.load('assets/sprites/9.png').convert_alpha(),
    )
    SPRITES['camera_pane'] = pygame.image.load('assets/sprites/camera_pane.png').convert_alpha()
    SPRITES['title'] =pygame.image.load('assets/sprites/title.png').convert_alpha()
    SPRITES['base'] =pygame.image.load('assets/sprites/base.png').convert_alpha()
    SPRITES['pipe'] =(pygame.transform.rotate(pygame.image.load( PIPE).convert_alpha(), 180), pygame.image.load(PIPE).convert_alpha()
    )

    AUDIO['die'] = pygame.mixer.Sound('assets/audio/die.wav')
    AUDIO['hit'] = pygame.mixer.Sound('assets/audio/hit.wav')
    AUDIO['point'] = pygame.mixer.Sound('assets/audio/point.wav')
    AUDIO['wing'] = pygame.mixer.Sound('assets/audio/wing.wav')

    SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    SPRITES['bird'] = pygame.image.load(MIDFLAP).convert_alpha()
    SPRITES['gameover']  = pygame.image.load(GAMEOVER).convert_alpha()

    while True:
        welcomeGAME_SCREEN() 
        mainGAME_SCREEN() 
   

   

    