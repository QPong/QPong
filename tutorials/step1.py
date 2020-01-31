"""

Step 1: Minimal Pygame program

"""

import pygame

def main():
    
    # initialize the pygame module
    pygame.init()

    # set screen size
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('QPong')

    running = True
    while running:
        for event in pygame.event.get():
            # exit main loop when you click the 'X' button of the window
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == '__main__':
    main()