import pygame

class Sound():

    def bounce_sound(self):
        pygame.mixer.music.load('utils/data/4391__noisecollector__pongblipf-5.wav')
        pygame.mixer.music.play()

    def edge_sound(self):
        pygame.mixer.music.load('utils/data/4390__noisecollector__pongblipf-4.wav')
        pygame.mixer.music.play()

    def lost_sound(self):
        pygame.mixer.music.load('utils/data/4384__noisecollector__pongblipd4.wav')
        pygame.mixer.music.play(3)