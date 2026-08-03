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

    screen.fill((0, 0, 0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()