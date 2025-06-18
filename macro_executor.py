from pynput.keyboard import Controller, Key
import os

class MacroExecutor:
    def __init__(self):
        self.keyboard = Controller()

    def execute(self, gesture):
        if gesture == "Peace":
            self.keyboard.press(Key.media_play_pause)
            self.keyboard.release(Key.media_play_pause)
            print("Play/Pause (Peace)")
        elif gesture == "Circle Clockwise":
            self.keyboard.press(Key.media_volume_up)
            self.keyboard.release(Key.media_volume_up)
            print("Volume Up (Circle Clockwise)")
        elif gesture == "Circle Anti-Clockwise":
            self.keyboard.press(Key.media_volume_down)
            self.keyboard.release(Key.media_volume_down)
            print("Volume Down (Circle Anti-Clockwise)")
        elif gesture == "Open Palm Right":
            self.keyboard.press(Key.media_next)
            self.keyboard.release(Key.media_next)
            print("Next track (Open Palm Right)")
        elif gesture == "Open Palm Left":
            self.keyboard.press(Key.media_previous)
            self.keyboard.release(Key.media_previous)
            print("Previous track (Open Palm Left)")
        else:
            print(f"Executing macro for gesture: {gesture}")
