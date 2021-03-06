from pickle import TRUE
import pygame
from pygame import mixer
pygame.init()

WIDTH = 1400
HEIGHT = 800

black = (0, 0, 0)
white = (255, 255, 255)
grey = (128, 128, 128)
on = (21, 244, 238)
gold = (212, 175, 55)
blue = (0, 255, 0)
dark_grey = (50, 50, 50)

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Drums')
label_font = pygame.font.Font('freesansbold.ttf', 32)
medium_font = pygame.font.Font('freesansbold.ttf', 24)

fps = 60
timer = pygame.time.Clock()
beats = 8
instruments = 6
boxes = []
clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]
bpm = 246 #246
playing = True
active_length = 0
active_beat = 0
beat_changed = True
kit = 1

# load in sounds
if kit == 1:
    hi_hat = mixer.Sound('./sounds/hi hat.WAV')
    clap = mixer.Sound('./sounds/clap.WAV')
    crash = mixer.Sound('./sounds/crash.WAV')
    kick = mixer.Sound('./sounds/kick.WAV')
    snare = mixer.Sound('./sounds/snare.WAV')
    tom = mixer.Sound('./sounds/tom.WAV')
    some = mixer.Sound('./sounds/some.WAV')

elif kit == 2:
    hi_hat = mixer.Sound('./sounds/kit2/hi hat.WAV')
    clap = mixer.Sound('./sounds/kit2/clap.WAV')
    crash = mixer.Sound('./sounds/kit2/crash.WAV')
    kick = mixer.Sound('./sounds/kit2/kick.WAV')
    snare = mixer.Sound('./sounds/kit2/snare.WAV')
    tom = mixer.Sound('./sounds/kit2/tom.WAV')

pygame.mixer.set_num_channels(instruments * 3)

def play_notes():
    for i in range(len(clicked)):
        if clicked[i][active_beat] == 1:
            if i == 0:
                hi_hat.play()
            if i == 1:
                snare.play()
            if i == 2:
                kick.play()
            if i == 3:
                crash.play()
            if i == 4:
                clap.play()
            if i == 5:
                some.play()
            if i == 6:
                some.play()

def draw_grid(clicked, beat):
    left_box = pygame.draw.rect(screen, grey, [0, 0, 200, HEIGHT - 200], 5)
    bottom_box = pygame.draw.rect(screen, grey, [0, HEIGHT - 200, WIDTH, 200], 5)
    colors = [grey, white, grey]
    boxes = []
    hi_hat_text = label_font.render('Hi Hat', True, white)
    screen.blit(hi_hat_text, (30, 30))
    snare_text = label_font.render('Snare', True, white)
    screen.blit(snare_text, (30, 130))
    kick_text = label_font.render('Bass', True, white)
    screen.blit(kick_text, (30, 230))
    crash_text = label_font.render('Crash', True, white)
    screen.blit(crash_text, (30, 330))
    clap_text = label_font.render('Clap', True, white)
    screen.blit(clap_text, (30, 430))
    floor_tom_text = label_font.render('Floor Tom', True, white)
    screen.blit(floor_tom_text, (30, 530))
    # some_text = label_font.render('Some', True, white)
    # screen.blit(some_text, (30, 630))

    for i in range(instruments):
        pygame.draw.line(screen, grey, (0, (i*100) + 100), (200, (i*100) + 100), 3)

    for i in range(beats):
        for j in range(instruments):
            if clicked[j][i] == -1:
                color = grey
            else:
                color = on
            rect = pygame.draw.rect(screen, color, [i * ((WIDTH - 200) // beats) + 205, (j * 100) + 5, ((WIDTH - 200) // beats) - 10, ((HEIGHT - 200) //instruments) - 10], 0, 3)
            
            pygame.draw.rect(screen, gold, [i * ((WIDTH - 200) // beats) + 200, (j * 100), ((WIDTH - 200) // beats), ((HEIGHT - 200) //instruments)], 5, 5)

            pygame.draw.rect(screen, black, [i * ((WIDTH - 200) // beats) + 200, (j * 100), ((WIDTH - 200) // beats), ((HEIGHT - 200) //instruments)], 2, 5)

            boxes.append((rect, (i, j)))

        active = pygame.draw.rect(screen, blue, [beat * ((WIDTH - 200) // beats) + 200, 0, ((WIDTH - 200) // beats), instruments * 100], 5, 3)
    return boxes

# GAME LOOP
run = True
while run:
    timer.tick(fps)
    screen.fill(black)
    boxes = draw_grid(clicked, active_beat)
    # lower menu buttons
    play_pause = pygame.draw.rect(screen, grey, [50, HEIGHT - 150, 200, 100], 0, 5)
    play_text = label_font.render('Play/Pause', True, white)
    screen.blit(play_text, (70, HEIGHT - 130))
    if playing:
        play_text2 = medium_font.render('Playing', True, dark_grey)
    else:
        play_text2 = medium_font.render('Paused', True, dark_grey)
    screen.blit(play_text2, (70, HEIGHT - 100))
        

    if beat_changed:
        play_notes()
        beat_changed = False



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            for i in range(len(boxes)):
                if boxes[i][0].collidepoint(event.pos):
                    coords = boxes[i][1]
                    clicked[coords[1]][coords[0]] *= -1
        
        if event.type == pygame.MOUSEBUTTONUP:
            if play_pause.collidepoint(event.pos):
                if playing:
                    playing = False
                elif not playing:
                    playing = True

    beat_length = 3600 // bpm

    if playing:
        if active_length < beat_length:
            active_length += 1
        else: 
            active_length= 0

            if active_beat < beats - 1:
                active_beat += 1
                beat_changed = True
            
            else:
                active_beat = 0
                beat_changed = True

    pygame.display.flip()

pygame.quit()
