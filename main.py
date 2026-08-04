import math
from random import sample
import pygame
import sounddevice as sd
import numpy as np
import tkinter
import pyaudio


# Create a hidden Tkinter window to get the screen dimensions
root = tkinter.Tk()
root.withdraw()
x, y = root.winfo_screenwidth(), root.winfo_screenheight()

# Audio Initialization
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# Initialize Libraries and set up the display
pygame.init()
screen = pygame.display.set_mode((x - (x / 20), y - (y / 20)), pygame.RESIZABLE)
pygame.display.set_caption("Art from Audio (Early Prototype)")
clock = pygame.time.Clock()
running = True
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

def get_microphone_input_level():
    data = stream.read(CHUNK)
    rms = 0
    for i in range(0, len(data), 2):
        sample = int.from_bytes(data[i:i+2], byteorder='little', signed=True)
        rms += sample * sample
    rms = math.sqrt(rms / (CHUNK / 2))
    return rms

def draw_sine_wave(amplitude):
    screen.fill((0, 0, 0))
    points = []
    if amplitude > 10:
        for x in range(screen.get_width()):
            y = int((screen.get_height() / 2) + (amplitude * 0.5) * math.sin(x * 0.01))
            points.append((x, y))
    else:
        points.append((0, screen.get_height() / 2))
        points.append((screen.get_width(), screen.get_height() / 2))
    pygame.draw.lines(screen, (255, 255, 255), False, points, 2)
    pygame.display.flip()

def draw_vu(level):
    screen.fill((0, 0, 0))
    db = 20 * math.log10(level / 32768 + 1e-10)
    db = max (-40, min(0, db))
    blocks = int((db + 40) / 40 * 40)
    block_height = screen.get_height() / 40
    gap = 2
    x = screen.get_width() // 2 - 20
    for i in range(blocks):
        y = screen.get_height() - (i + 1) * (block_height + gap)
        if i < 20:
            color = (0, 200, 0)
        elif i < 32:
            color = (255, 255, 0)
        else:
            color = (255, 0, 0)
        pygame.draw.rect(screen, color, (x, y, 40, block_height))
    pygame.display.flip()

amplitude = 100

# Main Loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    level = get_microphone_input_level()
    draw_vu(level)
    clock.tick(60)

pygame.quit()