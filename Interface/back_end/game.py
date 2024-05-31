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
import typing
import gest
import matplotlib.pyplot as plt
import os as o
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger('matplotlib').setLevel(logging.WARNING)

class Game:
    """
    A class to encapsulate the Flappy Bird game.

    :ivar GAME_SCREEN: The main display surface for the game, set to fullscreen mode.
    :ivar W: The width of the display screen.
    :ivar H: The height of the display screen.
    :ivar FLOOR: The height of the floor in the game, calculated as 80% of the screen height.
    :ivar SPRITES: A dictionary holding the game's sprite images.
    :ivar AUDIO: A dictionary holding the game's audio files.
    :ivar FPS: The frames per second setting for the game.

    :method __init__: Initializes the game screen and loads the sprites and audio.
    :method display_welcome_game_screen: Displays the welcome screen for the game.
    :method display_main_game_screen: Displays the main screen for the game.
    :method check_out_of_bounds: Checks if player is out of bounds.
    :method generate_pipe: Displays and generates the next pipe.

    """
    def __init__(self) -> None:
        """
        Initialize game screen.

        :return: None
        """
        pygame.init()
        self.GAME_SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        screen_info = pygame.display.Info()
        self.W = screen_info.current_w
        self.H = screen_info.current_h

        self.FLOOR = self.H * 0.8 
        self.SPRITES = {}
        self.AUDIO = {}
        self.FPS = 40

        sprite_paths = {
            'numbers': [f'assets/sprites/{i}.png' for i in range(10)],
            'camera_pane': 'assets/sprites/camera_pane.png',
            'title': 'assets/sprites/title.png',
            'base': 'assets/sprites/base.png',
            'pipe': PIPE,
            'background': BACKGROUND,
            'bird': MIDFLAP,
            'gameover': GAMEOVER
        }

        audio_paths = {
            'die': 'assets/audio/die.wav',
            'hit': 'assets/audio/hit.wav',
            'point': 'assets/audio/point.wav',
            'wing': 'assets/audio/wing.wav'
        }

        self.SPRITES = {
            'numbers': [pygame.image.load(path).convert_alpha() for path in sprite_paths['numbers']],
            'camera_pane': pygame.image.load(sprite_paths['camera_pane']).convert_alpha(),
            'title': pygame.image.load(sprite_paths['title']).convert_alpha(),
            'base': pygame.image.load(sprite_paths['base']).convert_alpha(),
            'pipe': (
                pygame.transform.rotate(pygame.image.load(sprite_paths['pipe']).convert_alpha(), 180),
                pygame.image.load(sprite_paths['pipe']).convert_alpha()
            ),
            'background': pygame.image.load(sprite_paths['background']).convert(),
            'bird': pygame.image.load(sprite_paths['bird']).convert_alpha(),
            'gameover': pygame.image.load(sprite_paths['gameover']).convert_alpha()
        }

        self.AUDIO = {key: pygame.mixer.Sound(path) for key, path in audio_paths.items()}
    
    def display_welcome_game_screen(self, bird_sprites) -> None:
        """
        Display the welcome screen for the game.

        :param bird_sprites: array of sprite paths
        :return: None
        """
        bird_index = 0

        birdx = int((self.W - self.SPRITES['bird'].get_width()) / 2)
        birdy = int((self.H - self.SPRITES['bird'].get_height()) / 2)
        titlex = int((self.W - self.SPRITES['title'].get_width()) / 2)
        titley = int(self.H * 0.13)
        basex = 0
        clockie = pygame.time.Clock()
        logging.info('Welcome Game Screen Successfully Initialized')

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    return
                elif event.type == pygame.KEYDOWN and event.key== pygame.K_ESCAPE:
                    pygame.display.toggle_fullscreen()
                else:
                    bird_index += 1
                    bird_index %= 3
                    self.SPRITES['bird'] = pygame.image.load(bird_sprites[bird_index]).convert_alpha()

                    self.GAME_SCREEN.blit(self.SPRITES['background'], (0, 0))
                    self.GAME_SCREEN.blit(self.SPRITES['base'], (basex, self.FLOOR))
                    self.GAME_SCREEN.blit(self.SPRITES['bird'], (birdx, birdy))
                    self.GAME_SCREEN.blit(self.SPRITES['title'], (titlex, titley))

                    pygame.display.update()
                    clockie.tick(self.FPS)


    def display_main_game_screen(self,bird_sprites) -> None:
        """
        Main game loop for FlappyLingo.

        :param bird_sprites: array of sprite paths
        :return: None
        """
        gg = gest.States(5)
        cap = cv2.VideoCapture(4)
        hand = gest.MH(buffer_size=100)
        showvid = True

        bird_index = 0
        font = pygame.font.Font("assets/fonts/ka1.TTF", 30) 
        string_list = ["A", "hello", "B", "C", "where", "I love you", "me"]
        signLanguage = random.choice(string_list)
        text = font.render(signLanguage, True, (255, 255, 255)) 
        startingText = font.render("Make the sign", True, (255, 255, 255)) 
        lookLeftText = font.render("PAUSED look left", True, (255, 255, 255)) 
        score = 0
        endingText = font.render("WRONG SIGN", True, (255, 255, 255)) 
        birdx = int(self.W/2)+250
        birdy = int(self.H/2)-200
        basex = 0

        pipeNumero1 = self.generate_pipe()
        pipeNumero2 = self.generate_pipe()

        topPipes = [
            {'x': self.W+200, 'y':pipeNumero1[0]['y']},
            {'x': self.W+200+400, 'y':pipeNumero2[0]['y']},
        ]
        botPipes = [
            {'x': self.W+200, 'y':pipeNumero1[1]['y']},
            {'x': self.W+200+400, 'y':pipeNumero2[1]['y']},
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

        try:
            with open(high_score_file_path, "r") as file:
                high_score = int(file.read())
        except FileNotFoundError:
            high_score = 0

        while True:
            if score > high_score:
                high_score = score
            
            try:
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

                if showvid:
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
                if event.type==pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    paused = not paused
                elif event.type == pygame.KEYDOWN and event.key== pygame.K_ESCAPE:
                    pygame.display.toggle_fullscreen()

            boomHit = self.check_out_of_bounds(birdx, birdy, topPipes, botPipes) 
            if boomHit: 
                return     

            birdMIDDLE = birdx + self.SPRITES['bird'].get_width()/2
            for pipe in topPipes:
                pipeMIDDLE = pipe['x'] + self.SPRITES['pipe'][0].get_width()/2
                pipeHeight = self.SPRITES['pipe'][0].get_height()
                if 0<topPipes[0]['x']< 900:
                    birdy = pipeHeight + topPipes[1]['y'] + 60
                elif topPipes[0]['x']>1000:
                    birdy = pipeHeight + topPipes[0]['y'] + 60
                if not correctGest and pipeMIDDLE - 8 <= birdMIDDLE < pipeMIDDLE +4:
                    paused_text = text 
                    paused = True

                if pipeMIDDLE<= birdMIDDLE < pipeMIDDLE +4:
                    score +=1
                    logging.info('Current score: %s', score)
                    self.AUDIO['point'].play()

            if not paused:

                for upperPipe , lowerPipe in zip(topPipes, botPipes):
                    upperPipe['x'] += pipeVelX
                    lowerPipe['x'] += pipeVelX

                if 0<topPipes[0]['x']< 1000 and len(topPipes) < 2:
                    newpipe = self.generate_pipe()
                    topPipes.append(newpipe[0])
                    botPipes.append(newpipe[1])

                if topPipes[0]['x'] < 550:
                    topPipes.pop(0)
                    botPipes.pop(0)

                
                self.GAME_SCREEN.blit(self.SPRITES['background'], (0, 0))
                for upperPipe, lowerPipe in zip(topPipes, botPipes):
                    self.GAME_SCREEN.blit(self.SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
                    self.GAME_SCREEN.blit(self.SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

                self.GAME_SCREEN.blit(self.SPRITES['base'], (basex, self.FLOOR))
                self.GAME_SCREEN.blit(self.SPRITES['camera_pane'], (0, 0))
                self.GAME_SCREEN.blit(self.SPRITES['title'], (10,700))   

                NUMBERS = [int(x) for x in list(str(score))]
                smallwidth = 0
                for digit in NUMBERS:
                    smallwidth += self.SPRITES['numbers'][digit].get_width()
                toLEFT = (self.W - smallwidth)/2+300

                for digit in NUMBERS:
                    self.GAME_SCREEN.blit(self.SPRITES['numbers'][digit], (toLEFT, self.H*0.12))
                    toLEFT += self.SPRITES['numbers'][digit].get_width()
                bird_index = (bird_index + 1) % 3
                self.SPRITES['bird'] = pygame.image.load(bird_sprites[bird_index]).convert_alpha()
                self.GAME_SCREEN.blit(self.SPRITES['bird'], (birdx, birdy))
                high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))
                self.GAME_SCREEN.blit(high_score_text, (50, 400))
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
                toLEFT = (self.W - smallwidth)/2
                self.GAME_SCREEN.blit(startingText, (50,500))
                self.GAME_SCREEN.blit(paused_text, (50,600))

                self.GAME_SCREEN.blit(lookLeftText, (int(self.W/2)+200, 130))
                # print(hshape, " == ", signLanguage)
                
                if hshape == signLanguage:
                    paused = False
                    correctGest = True
                else :
                    wrongC+=1
                    if(wrongC >= 30):
                        self.AUDIO['die'].play()
                        center_x = (self.W - self.SPRITES['gameover'].get_width()) // 2
                        center_y = (self.H - self.SPRITES['gameover'].get_height()) // 2

                        for x in range(20):
                            self.GAME_SCREEN.blit(endingText, (center_x, center_y - 50))
                            self.GAME_SCREEN.blit(self.SPRITES['gameover'], (center_x, center_y))
                            pygame.display.update()
                        cap.release()
                        cv2.destroyAllWindows()
                        return
                    with open(high_score_file_path, "w") as file:
                        file.write(str(high_score))
            self.GAME_SCREEN.blit(resized_game_img, (50, 50))
            pygame.display.update()


    def check_out_of_bounds(self,birdx, birdy, topPipes, botPipes):
        """
        Check if the bird has collided with the pipes or gone out of bounds.

        :param birdx: The x-coordinate of the bird.
        :param birdy: The y-coordinate of the bird.
        :param topPipes: List of top pipe dictionaries with 'x' and 'y' coordinates.
        :param botPipes: List of bottom pipe dictionaries with 'x' and 'y' coordinates.
        :return: True if the bird is out of bounds or has collided with a pipe, False otherwise.
        """
        if birdy> self.FLOOR - 25  or birdy<0:
            self.AUDIO['die'].play()
            return True
        
        for peep in topPipes:
            pH = self.SPRITES['pipe'][0].get_height()
            if(birdy < pH + peep['y'] and abs(birdx - peep['x']) < self.SPRITES['pipe'][0].get_width()-2):
                return True

        for peep in botPipes:
            if (birdy + self.SPRITES['bird'].get_height() > peep['y']) and abs(birdx - peep['x']) < self.SPRITES['pipe'][0].get_width():
                return True

        return False


    def generate_pipe(self):
        """
        Generate a new pair of top and bottom pipes with random heights.

        :return: A list of dictionaries containing the 'x' and 'y' coordinates for the top and bottom pipes.
        """
        pipeHeight = self.SPRITES['pipe'][0].get_height()
        leftie = self.H/3
        yTWO = leftie + random.randrange(0, int(self.H - self.SPRITES['base'].get_height()  - 1.2 *leftie))
        pipeX = self.W
        yONE = pipeHeight - yTWO + leftie
        pipe = [
            {'x': pipeX, 'y': -yONE}, #upper Pipe
            {'x': pipeX, 'y': yTWO} #lower Pipe
        ]
        return pipe

if __name__ == "__main__":
    MIDFLAP = 'assets/sprites/orangebird-midflap.png'
    FLAPDOWN = 'assets/sprites/orangebird-downflap.png'
    FLAPUP = 'assets/sprites/orangebird-upflap.png'
    BACKGROUND = 'assets/sprites/background.png'
    PIPE = 'assets/sprites/pipe.png'
    GAMEOVER = 'assets/sprites/gameover.png'
    bird_sprites = [MIDFLAP, FLAPDOWN, FLAPUP]
    plt.switch_backend('Agg')
    logging.info('Starting FlappyLingo game')

    try:
        pygame.init()  # Initialize all pygame's modules
        logging.info('Pygame initialized successfully')

        clockie = pygame.time.Clock()
        pygame.display.set_caption('FlappyLingo')
        game = Game()

        logging.info('Game setup complete. Entering main loop.')

        while True:
            logging.debug('Displaying welcome game screen')
            game.display_welcome_game_screen(bird_sprites)
            
            logging.debug('Displaying main game screen')
            game.display_main_game_screen(bird_sprites)
    except Exception as e:
        logging.error('An error occurred: %s', e)
    finally:
        pygame.quit()
        logging.info('Pygame terminated')

   

    