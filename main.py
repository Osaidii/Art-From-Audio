import math
import pygame
import tkinter
import pyaudio

from pygame_widgets import Button

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

# Ininitialize the Buttons
button = Button(screen, width=screen.get_width() / 5, height=50)

def get_microphone_input_level():
    data = stream.read(CHUNK)
    rms = 0
    for i in range(0, len(data), 2):
        sample = int.from_bytes(data[i:i+2], byteorder='little', signed=True)
        rms += sample * sample
    rms = math.sqrt(rms / (CHUNK / 2))
    return rms

def draw_menu():
    pygame.draw.rect(screen, (100, 100, 100), [0, 0, screen.get_width(), screen.get_height() / 12])
    pygame.draw.line(screen, (255, 255, 255), (0, screen.get_height() / 12), (screen.get_width(), screen.get_height() / 12), int(screen.get_height() / 216))

def draw_vu(level):
    db = 20 * math.log10((level * 0.5) / 32768 + 1e-10)
    db = max (-40, min(0, db))
    blocks = int((db + 40) / 40 * 40)
    block_height = screen.get_height() / 40
    gap = 2
    x = screen.get_width() - (screen.get_width() / 50)
    for i in range(blocks):
        y = screen.get_height() - (i + 1) * (block_height + gap)
        if i < 20:
            color = (0, 200, 0)
        elif i < 32:
            color = (255, 255, 0)
        else:
            color = (255, 0, 0)
        pygame.draw.rect(screen, color, (x, y, 40, block_height))

display_level = 0

# Main Loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))
    draw_menu()
    level = get_microphone_input_level()
    if level < 300:
        level = 0
    print(level)
    if level > display_level:
        display_level = display_level * 0.3 + level * 0.7
    else:
        if level > 0:
            pass
        else:
            display_level = display_level * 0.85 + level * 0.05
    draw_vu(display_level)
    clock.tick(60)
    pygame.display.flip()

pygame.quit()