import pygame
from config import SOUNDS_FOLDER
import os

class SoundMaster():
    def __init__(self,):
        self.sounds = dict()

    def add_sound(self, name_handle, sound: str | pygame.mixer.Sound):
        
        if isinstance(sound, str):      #when sound is a string, we assume it is the name of the sound file
            sound = pygame.mixer.Sound(os.path.join(SOUNDS_FOLDER, sound))
        
        print("sound inside Class is:",sound)
        self.sounds[name_handle] = sound

    def get_sound(self, name_handle):
        return self.sounds.get(name_handle)

    