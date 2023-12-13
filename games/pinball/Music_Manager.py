import pygame

#music and sounds
class MusicManager():
    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.set_num_channels(2)
        self.music_channel = pygame.mixer.Channel(0)
        self.sound_channel = pygame.mixer.Channel(1)

        self.music_volume_100 = 100 #no floats, if used divide by 100
        self.sound_volume_100 = 100 #no floats, if used divide by 100
        self.general_volume = 4 # not an option for user, make everything more quiet

        self.music_channel.set_volume(self.music_volume_100 / 100 / self.general_volume)
        self.sound_channel.set_volume(self.sound_volume_100 / 100 / self.general_volume)

        self.sound_select = pygame.mixer.Sound("sounds/menu_select.mp3")
        self.music_amogus = pygame.mixer.Sound("sounds/Among_Us_Drip.mp3")

    def Play_Selection(self):
        self.sound_channel.play(self.sound_select)


    def Play_Music_In_Loop(self):
        self.music_channel.play(self.music_amogus, -1)


    def Music_Fadeout(self):
        self.music_channel.fadeout(8000)  # 1 sec fadeout

    #updates the volume to the ones given in the attributes of the class
    def Update_Volume(self):
        self.sound_channel.set_volume(self.sound_volume_100 / 100 / self.general_volume)
        self.music_channel.set_volume(self.music_volume_100 / 100 / self.general_volume)
