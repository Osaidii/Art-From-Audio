import pygame
import sounddevice as sd
import numpy as np
import tkinter

# Create a hidden Tkinter window to get the screen dimensions
root = tkinter.Tk()
root.withdraw()
x, y = root.winfo_screenwidth(), root.winfo_screenheight()

# Initialize Pygame and set up the display
pygame.init()
screen = pygame.display.set_mode((x - (x / 20), y - (y / 20)), pygame.RESIZABLE)
pygame.display.set_caption("Art from Audio (Early Prototype)")
clock = pygame.time.Clock()
running = True


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #audio_data = sd.rec(int(44100 * 0.8), samplerate=44100, channels=1, dtype='float32')
    #sd.wait()
    
    #volume = np.linalg.norm(audio_data) * 10

    screen.fill((0, 0, 0))

    #pygame.draw.circle(screen, (255, 0, 0), (x // 2, y // 2), int(volume))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()