import pygame

class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()

        self.playlist = [
            "Practice 09/music_player/music/track1.mp3",
            "Practice 09/music_player/music/track2.mp3"
        ]

        self.current_index = 0
        self.is_playing = False

    def play(self):
        pygame.mixer.music.load(self.playlist[self.current_index])
        pygame.mixer.music.play()
        self.is_playing = True
    
    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def next(self):
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.play()

    def prev(self):
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.play()

    def get_current_track(self):
        return self.playlist[self.current_index]
    
    def get_position(self):
        pos = pygame.mixer.music.get_pos()
        return pos // 1000