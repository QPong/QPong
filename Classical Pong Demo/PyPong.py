######################################################################################################
#                                                                                                    #
#                  ,-.----.            ,-.----.                                                      #
#                  \    /  \           \    /  \                                                     #
#                  |   :    \          |   :    \                                                    #
#                  |   |  .\ :         |   |  .\ :   ,---.        ,---,                              #
#                  .   :  |: |         .   :  |: |  '   ,'\   ,-+-. /  |  ,----._,.                  #
#                  |   |   \ :    .--, |   |   \ : /   /   | ,--.'|'   | /   /  ' /                  #
#                  |   : .   /  /_ ./| |   : .   /.   ; ,. :|   |  ,"' ||   :     |                  #
#                  ;   | |`-', ' , ' : ;   | |`-' '   | |: :|   | /  | ||   | .\  .                  #
#                  |   | ;  /___/ \: | |   | ;    '   | .; :|   | |  | |.   ; ';  |                  #
#                  :   ' |   .  \  ' | :   ' |    |   :    ||   | |  |/ '   .   . |                  #
#                  :   : :    \  ;   : :   : :     \   \  / |   | |--'   `---`-'| |                  #
#                  |   | :     \  \  ; |   | :      `----'  |   |/       .'__/\_: |                  #
#                  `---'.|      :  \  \`---'.|              '---'        |   :    :    v1.0          #
#                    `---`       \  ' ;  `---`                            \   \  /                   #
#                                 `--`                                     `--`-'                    #
#                                                                                                    #
######################################################################################################

# PyPong 1.0
# Terry Ritchie
# 04/15/17

# ----------------------------------------------------------------------------------------------------
# - IMPORT LIBRARIES ---------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

import pygame  # pygame graphics engine
import random  # random number library
import os  # operating system library
#import winsound  # windows sound library
import sys  # system functions
from pygame.locals import *  # pygame constants

# ----------------------------------------------------------------------------------------------------
# - DEFINE CONSTANTS ---------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

SWIDTH = 768  # width of play screen
SHEIGHT = 576  # height of play screen
FPS = 480  # frames per second of game play
PSIZE = 10  # width/height of puck
PWIDTH = 10  # width of player paddles
PHEIGHT = 60  # height of player paddles
PSPEED = 480 // FPS  # speed of player paddles and puck
POFFSET = 20  # paddle distance from edge of screen
PLAYER1 = 0  # player one value
PLAYER2 = 1  # player 2 value
GAMEINPROGRESS = -1  # denotes game in progress
WHITE = (255, 255, 255)  # define constant colors
LGRAY = (192, 192, 192)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)

# ----------------------------------------------------------------------------------------------------
# - DEFINE VARIABLES ---------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

pxdir = 0.0  # puck x direction vector
pydir = 0.0  # puck y direction vector
puckx = 0.0  # puck x coordinate location
pucky = 0.0  # puck y coordinate location
p1x = 0.0  # player 1 x coordinate location
p1y = 0.0  # player 1 y coordinate location
p2x = 0.0  # player 2 x coordinate location
p2y = 0.0  # player 2 y coordinate location
pscore = []  # player scores
scoretext = []  # big numbers custom strings
missed = 0  # holds value of player that missed puck
ai = False  # True if playing the computer
numplayers = 0  # number of human players
font = 0  # font used within game
clock = 0  # clock FPS timer
screen = 0  # window surface
players_text = 0  # instruction texts
spacebar_text = 0
player1_text = 0


# ----------------------------------------------------------------------------------------------------
# - DEFINE FUNCTIONS ---------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------
def Draw_Frame():  # draw the current play field                                           Draw_Frame()
    # ----------------------------------------------------------------------------------------------------

    sx = 0  # x coordinate of score digits
    sy = 50  # y coordinate of score digits
    clr = 0  # color of score digits

    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, (0, 19, SWIDTH, 10), 0)  # draw top and
    pygame.draw.rect(screen, WHITE, (0, SHEIGHT - 29, SWIDTH, 10), 0)  # bottom lines
    for y in range(40, SHEIGHT - 52, 30):  # draw dashed line
        pygame.draw.rect(screen, GRAY, (SWIDTH // 2 - 5, y, 10, 15), 0)
    for p in range(PLAYER1, PLAYER2 + 1):  # draw score digits
        if p == 0:
            sx = SWIDTH // 2 - 100
        else:
            sx = SWIDTH // 2 + 55
        if pscore[p] == 9:
            clr = WHITE
        else:
            clr = LGRAY
        Draw_Digit(sx, sy, pscore[p], clr)
    pygame.draw.rect(screen, WHITE, (p1x, p1y, PWIDTH, PHEIGHT), 0)  # draw paddles
    pygame.draw.rect(screen, WHITE, (p2x, p2y, PWIDTH, PHEIGHT), 0)
    if missed == GAMEINPROGRESS:  # if game in progress
        pygame.draw.rect(screen, WHITE, (puckx, pucky, PSIZE, PSIZE), 0)  # draw puck
        pygame.display.flip()  # and update screen
        clock.tick(FPS)


# ----------------------------------------------------------------------------------------------------
def Instructions():  # display game instructions to player                               Instructions()
    # ----------------------------------------------------------------------------------------------------

    global ai, numplayers, pscore  # need to modify these globals

    fcount = 0  # frame counter
    blink = True  # show "press spacebar" when True
    waiting = True  # wait for spacebar to be pressed
    numplayers = 0  # number of human players
    ready = 4  # countdown timer
    player2_text = font.render("SELECT (1) OR (2) PLAYERS NOW", True, WHITE)

    while ready > 0:
        Play_Round()  # draw frame
        if waiting:
            pygame.event.pump()  # clear keyboard buffer
            keys = pygame.key.get_pressed()  # get keys currently held down
            if keys[K_SPACE] and numplayers:  # spacebar key
                waiting = False
                fcount = FPS * 3 + 1  # countdown sequence value
            if keys[K_ESCAPE]:  # ESC key
                pygame.quit()
                sys.exit()
            if keys[K_1] and numplayers != 1:  # number 1 key
                numplayers = 1
                ai = True  # computer will be player 2
                #winsound.Beep(440, 55)
                #winsound.Beep(880, 55)
                player2_text = font.render("PLAYER 2: THE CPU HAS CONTROL", True, WHITE)
            if keys[K_2] and numplayers != 2:  # number 2 key
                numplayers = 2
                ai = False  # human will be player 2
                #winsound.Beep(440, 55)
                #winsound.Beep(880, 55)
                player2_text = font.render("PLAYER 2: UP ARROW / DOWN ARROW", True, WHITE)
            if numplayers > 0:  # show blinking "press spacebar"
                fcount += 1
                if fcount == FPS:
                    fcount = 0
                    blink = not (blink)
                if blink:
                    screen.blit(spacebar_text, [(SWIDTH - 178) // 2, SHEIGHT - 17])
            screen.blit(players_text, [(SWIDTH - 306) / 2, 2])
            screen.blit(player1_text, [(SWIDTH // 2 - 197) // 2, (SHEIGHT - 18) // 2])
            screen.blit(player2_text, [(SWIDTH // 2) + ((SWIDTH // 2) - 220) // 2, (SHEIGHT - 18) // 2])
        else:  # countdown sequence
            pscore[PLAYER1] = 0
            pscore[PLAYER2] = 0
            fcount -= 1
            if fcount % FPS == 0:  # keep track of each second elapsed
                #winsound.Beep(ready * 220, 55)
                ready -= 1
            Draw_Digit((SWIDTH - 45) // 2, (SHEIGHT - 75) // 2, ready, WHITE)
        pygame.display.flip()
        clock.tick(FPS)


# ----------------------------------------------------------------------------------------------------
def New_Game():  # new game initialization                                                   New_Game()
    # ----------------------------------------------------------------------------------------------------

    global p1x, p1y, p2x, p2y, missed, ai, numplayers  # need to modify these globals

    #winsound.Beep(440, 55)  # intro sounds
    #winsound.Beep(880, 55)
    missed = PLAYER2  # serve to player 2
    ai = False  # assume two human players
    numplayers = 0
    p1x = POFFSET  # reset paddle locations
    p1y = SHEIGHT // 2 - PHEIGHT // 2
    p2x = SWIDTH - POFFSET - PWIDTH
    p2y = SHEIGHT // 2 - PHEIGHT // 2


# ----------------------------------------------------------------------------------------------------
def Reset_Round():  # resets the condition for the next round of play                     Reset_Round()
    # ----------------------------------------------------------------------------------------------------

    global pxdir, pydir, puckx, pucky, missed  # need to modify these globals

    pucky = random.randrange(50, SHEIGHT - 50)  # random puck y coordinate
    pydir = ((random.random() - random.random()) / 2) * PSPEED  # and vertical direction
    if missed == PLAYER1:  # set puck heading toward player 1
        pxdir = -0.5 * PSPEED
        puckx = SWIDTH * .75
    else:  # set puck heading toward player 2
        pxdir = 0.5 * PSPEED
        puckx = SWIDTH * .25
    missed = GAMEINPROGRESS  # put game back into play


# ----------------------------------------------------------------------------------------------------
def Draw_Digit(dx, dy, d, c):  # draw a large digit to the screen                          Draw_Digit()
    # ----------------------------------------------------------------------------------------------------

    # dx = digit top left x coordinate
    # dy = digit top left y coordinate
    # d  = digit (0 - 9)
    # c  = digit color

    # The large digits are drawn as follows:
    #
    #              x
    #          ---------
    #          0   1   2
    #        +---+---+---+      +---+---+---+   If there is a character (non-space) in the text a
    #    | 0 | * | * | * |      | * | * | * |   square is drawn in that position. As the nested for
    #    |   +---+---+---+      +---+---+---+   statements progress a number is drawn from the text
    #    | 1 | * |   | * |      |   |   | * |   that describes where a square should be placed in
    #    |   +---+---+---+      +---+---+---+   each row.
    #  y | 2 | * |   | * |      | * | * | * |
    #    |   +---+---+---+      +---+---+---+
    #    | 3 | * |   | * |      |   |   | * |
    #    |   +---+---+---+      +---+---+---+
    #    | 4 | * | * | * |      | * | * | * |
    #    |   +---+---+---+      +---+---+---+
    #
    #      "0000 00 00 0000"  "333  3333  3333"
    #       |||---|||---|||    |||---|||---|||
    # Row->  0  1  2  3  4      0  1  2  3  4

    p = -1  # current position in text string
    for y in range(5):
        for x in range(3):
            p += 1  # increment text position
            if scoretext[d][0][p] != " ":  # if there is a character in text position draw square
                pygame.draw.rect(screen, c, [dx + x * 15, dy + y * 15, 15, 15], 0)


# ----------------------------------------------------------------------------------------------------
def Setup():  # creates the assets needed to play the game                                      Setup()
    # ----------------------------------------------------------------------------------------------------

    global scoretext, font, players_text, spacebar_text, pscore, clock, screen  # need to modify these
    global player1_text

    os.environ["SDL_VIDEO_CENTERED"] = "1"  # tell pygame to center the surface on desktop
    pygame.init()  # start pygame engine
    screen = pygame.display.set_mode((SWIDTH, SHEIGHT))  # create the surface window
    pygame.display.set_caption("PyPong!")  # give window a caption
    clock = pygame.time.Clock()  # start clock routines
    pscore.append([0])  # create player score list
    pscore.append([0])
    pscore[PLAYER1] = 0
    pscore[PLAYER2] = 0
    scoretext.append(["0000 00 00 0000"])  # create big number strings list
    scoretext.append(["  1  1  1  1  1"])
    scoretext.append(["222  22222  222"])
    scoretext.append(["333  3333  3333"])
    scoretext.append(["4 44 4444  4  4"])
    scoretext.append(["5555  555  5555"])
    scoretext.append(["6666  6666 6666"])
    scoretext.append(["777  7  7  7  7"])
    scoretext.append(["8888 88888 8888"])
    scoretext.append(["9999 9999  9999"])
    font = pygame.font.SysFont("Calibri", 16, False, False)
    players_text = font.render("SELECT (1) or (2) PLAYERS NOW : ESC TO EXIT", True, WHITE)
    spacebar_text = font.render("PRESS SPACEBAR TO PLAY", True, WHITE)
    player1_text = font.render("PLAYER 1: W = UP / S = DOWN", True, WHITE)


# ----------------------------------------------------------------------------------------------------
def Trajectory(playery):  # calculates angle of puck trajectory                            Trajectory()
    # ----------------------------------------------------------------------------------------------------

    # playery = player's y coordinate location

    return (((pucky - playery) + PSIZE - (PHEIGHT + PSIZE) // 2) / ((PHEIGHT + PSIZE) / 2)) / 2


# ----------------------------------------------------------------------------------------------------
def sgn(n):  # returns the sign of a number (-1, 0, or 1                                          sgn()
    # ----------------------------------------------------------------------------------------------------

    # n = any numeric value

    if n > 0:
        return 1
    elif n < 0:
        return -1
    else:
        return 0


# ----------------------------------------------------------------------------------------------------
def Play_Round():  # plays a round of PyPong                                               Play_Round()
    # ----------------------------------------------------------------------------------------------------

    global pxdir, pydir, puckx, pucky, p1x, p1y, p2x, p2y, pscore, missed, ai  # need to modify these

    for event in pygame.event.get():  # cycle through events
        if event.type == pygame.QUIT:  # leave game if window closed
            pygame.quit()
            sys.exit()
    pygame.event.pump()  # clear keyboard buffer
    keys = pygame.key.get_pressed()  # key all keys currently pressed
    if keys[K_ESCAPE]:  # ESC key
        pygame.quit()
        sys.exit()
    if keys[K_w]:  # W key
        p1y -= PSPEED
    if keys[K_s]:  # S key
        p1y += PSPEED
    if ai:  # computer controls player 2
        v_speed = ((1 + random.random()) / (PSPEED * 2)) * PSPEED
        if pxdir > 0:  # puck heading toward computer
            puck_location = pucky - p2y - PHEIGHT // 2 + PSIZE // 2
            if puck_location < 0:
                p2y -= v_speed
            elif puck_location > 0:
                p2y += v_speed
        else:  # puck heading toward player 1
            if int(p2y) > SHEIGHT // 2 - PHEIGHT // 2:
                p2y -= v_speed
            elif int(p2y) < SHEIGHT // 2 - PHEIGHT // 2:
                p2y += v_speed
    else:  # human controls player 2
        if keys[K_DOWN]:  # DOWN ARROW key
            p2y += PSPEED
        if keys[K_UP]:  # UP ARROW key
            p2y -= PSPEED
    if p1y <= 30:  # keep player 1 paddle within limits
        p1y = 30
    if p1y >= SHEIGHT - PHEIGHT - 30:
        p1y = SHEIGHT - PHEIGHT - 30
    if p2y <= 30:  # keep player 2 paddle within limits
        p2y = 30
    if p2y >= SHEIGHT - PHEIGHT - 30:
        p2y = SHEIGHT - PHEIGHT - 30
    if missed == GAMEINPROGRESS:  # is there a game in progress?
        puckx += pxdir  # update puck position
        pucky += pydir
        if pucky <= 30:  # keep puck in vertical limits
            pucky = 30
            pydir = -pydir
            #winsound.Beep(880, 55)
        elif pucky >= SHEIGHT - PSIZE - 30:
            pucky = SHEIGHT - PSIZE - 30
            pydir = -pydir
            #winsound.Beep(880, 55)
        if puckx <= p1x:  # player 1 missed puck
            pscore[PLAYER2] += 1
            missed = PLAYER1
            #winsound.Beep(220, 55)
        elif puckx >= p2x + PWIDTH:  # player 2 missed puck
            pscore[PLAYER1] += 1
            missed = PLAYER2
            #winsound.Beep(220, 55)
        else:
            if puckx <= p1x + PWIDTH:
                if pucky - p1y >= -PSIZE:
                    if pucky - p1y <= PHEIGHT:  # player 1 hit puck
                        puckx = p1x + PWIDTH
                        pxdir = -pxdir + (.025 * PSPEED)
                        pydir += Trajectory(p1y)  # update puck trajectory
                        if abs(pydir) > PSPEED:
                            pydir = sgn(pydir) * PSPEED
                        #winsound.Beep(440, 55)
            if puckx + PSIZE >= p2x:
                if pucky - p2y + PSIZE >= 0:
                    if pucky - p2y <= PHEIGHT:  # player 2 hit puck
                        puckx = p2x - PSIZE
                        pxdir = -pxdir - (.025 * PSPEED)
                        pydir += Trajectory(p2y)  # update puck trajectory
                        if abs(pydir) > PSPEED:
                            pydir = sgn(pydir) * PSPEED
                        #winsound.Beep(440, 55)
    Draw_Frame()  # draw screen


# ----------------------------------------------------------------------------------------------------
# - MAIN PROGRAM LOOP --------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

Setup()  # create game assets
while True:  # loop forever
    New_Game()  # set up a new game
    Instructions()  # display instructions to player(s)
    while pscore[PLAYER1] != 9 and pscore[PLAYER2] != 9:  # loop until one player scores 9
        Reset_Round()  # set up a new round of play
        while missed == GAMEINPROGRESS:  # loop while a round in progress
            Play_Round()  # play the round