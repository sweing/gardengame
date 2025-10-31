"""
Sound and music management system
"""
import pygame
from config import (
    SOUND_FILES, BACKGROUND_MUSIC, DEFAULT_VOLUME,
    MUSIC_VOLUME_MULTIPLIER, AMBIENT_VOLUME_MULTIPLIER
)


class SoundManager:
    """Manages all game sounds with graceful fallback if files are missing"""
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.music_playing = False
        self.muted = False
        self.volume = DEFAULT_VOLUME
        self.current_ambient = None  # Track current ambient sound

        # Try to load each sound
        for name, path in SOUND_FILES.items():
            try:
                sound = pygame.mixer.Sound(path)
                sound.set_volume(self.volume)
                self.sounds[name] = sound
                print(f"Loaded sound: {name}")
            except:
                # Sound file not found - that's okay, we'll just skip it
                self.sounds[name] = None
                print(f"Sound not found (optional): {path}")

        # Try to load background music
        try:
            pygame.mixer.music.load(BACKGROUND_MUSIC)
            pygame.mixer.music.set_volume(self.volume * MUSIC_VOLUME_MULTIPLIER)
            print("Loaded background music")
        except:
            print("Background music not found (optional)")

    def play(self, sound_name):
        """Play a sound effect"""
        if self.muted:
            return

        if sound_name in self.sounds and self.sounds[sound_name]:
            self.sounds[sound_name].play()

    def play_music(self, loops=-1):
        """Start background music (loops infinitely by default)"""
        if self.muted or self.music_playing:
            return

        try:
            pygame.mixer.music.play(loops)
            self.music_playing = True
        except:
            pass

    def stop_music(self):
        """Stop background music"""
        pygame.mixer.music.stop()
        self.music_playing = False

    def toggle_mute(self):
        """Toggle sound on/off"""
        self.muted = not self.muted
        if self.muted:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
        return self.muted

    def set_volume(self, volume):
        """Set volume (0.0 to 1.0)"""
        self.volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.volume * MUSIC_VOLUME_MULTIPLIER)
        for sound in self.sounds.values():
            if sound:
                sound.set_volume(self.volume)

    def play_ambient(self, sound_name):
        """Play an ambient sound on loop"""
        if self.muted or sound_name == self.current_ambient:
            return

        # Stop current ambient if different
        if self.current_ambient and self.sounds.get(self.current_ambient):
            self.sounds[self.current_ambient].stop()

        # Start new ambient
        if sound_name in self.sounds and self.sounds[sound_name]:
            self.sounds[sound_name].play(loops=-1)  # Loop infinitely
            self.sounds[sound_name].set_volume(self.volume * AMBIENT_VOLUME_MULTIPLIER)
            self.current_ambient = sound_name

    def stop_ambient(self):
        """Stop current ambient sound"""
        if self.current_ambient and self.sounds.get(self.current_ambient):
            self.sounds[self.current_ambient].stop()
            self.current_ambient = None
