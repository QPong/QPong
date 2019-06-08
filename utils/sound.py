import pygame


class Sound:

    @staticmethod
    def bounce_sound():
        pygame.mixer.music.load('utils/data/sound/4391__noisecollector__pongblipf-5.wav')
        pygame.mixer.music.play()

    @staticmethod
    def edge_sound():
        pygame.mixer.music.load('utils/data/sound/4390__noisecollector__pongblipf-4.wav')
        pygame.mixer.music.play()

    @staticmethod
    def lost_sound():
        pygame.mixer.music.load('utils/data/sound/4384__noisecollector__pongblipd4.wav')
        pygame.mixer.music.play(3)
