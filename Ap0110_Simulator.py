import pygame, random, sys
from pygame.locals import *

# Establishing Values to Variables, Named Accordingly
WINDOWWIDTH = 600
WINDOWHEIGHT = 600
TEXTCOLOR = (255, 255, 255)
ALERT = (255,0,0)
BACKGROUNDCOLOR = (0, 0, 0)
FPS = 40
DEBRIS_SMALL = 10
DEBRIS_LARGE = 40
DEBRIS_MIN = 1
DEBRIS_MAX = 8
DEBRISRATE = 9
PLAYERMOVERATE = 5

screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT)) 


def drawText(text, font, surface, x, y,): # Sets up the display for the window/text display 
    text_object = font.render(text, 1, TEXTCOLOR)
    text_display = text_object.get_rect()
    text_display.topleft = (x, y)
    surface.blit(text_object, text_display)


def Final_Text(text2,font2,surface2,x2,y2):
    text_object2 = font2.render(text2,1, ALERT)
    text_display2 = text_object2.get_rect()
    text_display2.topleft = (x2,y2)
    surface2.blit(text_object2, text_display2)

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # Pressing Escapes Closes Out the Game
                    terminate()
                return

def collision(playerRect, debris):  # Creats a Function for Colliusion 
    for d in debris:
        if playerRect.colliderect(d['rect']):
            return True
    return False

def terminate():
    pygame.quit()
    sys.exit()


# Sets up Title, Window, and Time Intervals (Initializes Pygame)
pygame.init()
Time = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Ap0110_Simu')
pygame.mouse.set_visible(False)
crash_sound = pygame.mixer.Sound('implode.wav')
rocket_launch = pygame.mixer.Sound('The Ultimate Saturn V Launch Video with INCREDIBLE SOUND!!!.wav')
# Fonts For Title
font = pygame.font.SysFont(None, 48)


# Sets up Sprite Images
playerImage = pygame.image.load('saturnV.png')
playerImage2 = pygame.transform.scale(playerImage, (50, 30))
playerRect = playerImage2.get_rect()
Satellite = pygame.image.load('2png.png')
empty_space = pygame.image.load('2png.png')

# Start Screen With Text
drawText('Ap0110_Simulator', font, windowSurface, (WINDOWWIDTH / 5), (WINDOWHEIGHT / 3))
drawText('Mouse or Arrows to move', font, windowSurface, (WINDOWWIDTH / 5) - 35, (WINDOWHEIGHT / 3) + 50)
drawText('Press Z For Boost', font, windowSurface, (WINDOWWIDTH / 5) - 35, (WINDOWHEIGHT / 3) + 100)
drawText('Press X To Slow Down', font, windowSurface, (WINDOWWIDTH / 5) - 35, (WINDOWHEIGHT / 3) + 150)
drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 5) - 35, (WINDOWHEIGHT / 3) + 200)

pygame.display.update()
waitForPlayerToPressKey()

topScore = 0
while True:
    rocket_launch.play()
    # Establishes position and score at the beginning of the game
    debris = []
    score = 0
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseTHRUST = slowTHRUST = False
    Satelites_Counter = 0


    while True: # Loops the game to run until collision
        score += 1 # increase score by 1 for every second
        
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == ord('z'): # Turns On Reverese Thrusters
                    reverseTHRUST = True 
                if event.key == ord('x'): # Slows Down Propulsion on Rocket
                    slowTHRUST = True
                if event.key == K_LEFT or event.key == ord('a'):
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == ord('w'):
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown = True

            if event.type == KEYUP:
                if event.key == ord('z'):
                    reverseTHRUST = False
                    score = 0
                if event.key == ord('x'):
                    slowTHRUST = False
                    score = 0
                if event.key == K_ESCAPE:
                        terminate()
 
                if event.key == K_LEFT or event.key == ord('a'):
                    moveLeft = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = False
                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False

            if event.type == MOUSEMOTION:
                # Mouse Motion Will Be Detected Besides Key Presses
                playerRect.move_ip(event.pos[0] - playerRect.centerx, event.pos[1] - playerRect.centery)

        # New waves of Debris are added to continue the gameplay
        if not reverseTHRUST and not slowTHRUST:
            Satelites_Counter += 1
        if Satelites_Counter == DEBRISRATE:
            Satelites_Counter = 0
            DebrisSize = random.randint(DEBRIS_SMALL, DEBRIS_LARGE)
            Debris_New1 = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH-DebrisSize), 0 - DebrisSize, DebrisSize, DebrisSize),
                        'speed': random.randint(DEBRIS_MIN, DEBRIS_MAX),
                        'surface':pygame.transform.scale(Satellite, (DebrisSize, DebrisSize)),
                        }
            Debris_New2 = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH-DebrisSize), 0 - DebrisSize, DebrisSize, DebrisSize),
                        'speed': random.randint(DEBRIS_MIN, DEBRIS_MAX),
                        'surface':pygame.transform.scale(empty_space, (DebrisSize, DebrisSize)),
                        }

            debris.append(Debris_New1)
            debris.append(Debris_New2)
            
            

        # Move the Satrun V Rocket around the plane
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)

        # Move the mouse cursor to match the player.
        pygame.mouse.set_pos(playerRect.centerx, playerRect.centery)

        # Make the Space Debris Drop Down
        for d in debris:
            if not reverseTHRUST and not slowTHRUST:
                d['rect'].move_ip(0, d['speed'])
            elif reverseTHRUST:
                d['rect'].move_ip(0, 5)
            elif slowTHRUST:
                d['rect'].move_ip(0, 1)

         # Any Debris that fall out of the window are removed
        for d in debris[:]:
            if d['rect'].top > WINDOWHEIGHT:
                debris.remove(d)

        # Fills the Background
        windowSurface.fill(BACKGROUNDCOLOR)
      
        # Score is Shown
        drawText('Score: %s' % (score), font, windowSurface, 5, 0)
        

        # Draw the player's Sprite
        windowSurface.blit(playerImage2, playerRect)

        # Draw each of the satellites
        for d in debris:
            windowSurface.blit(d['surface'], d['rect'])

        pygame.display.update()

        # Check if any collision became eminent
        if collision(playerRect, debris):
            break

        Time.tick(FPS)

    # The Game Ends and the Abort Mission Screen Appears
    rocket_launch.stop()
    crash_sound.play()

    Final_Text('ABORT MISSION!', font , windowSurface, (WINDOWWIDTH / 4), (WINDOWHEIGHT / 3))
    Final_Text('Press a key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()

    crash_sound.stop()
