import pygame
import sys
import csv
import numpy as np
from button import Button
from utils import get_font
from main2 import window, BG
import play
from main2 import clock, manager, main

yScores = []

def again(name):
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        window.fill("black")

        PLAY_TEXT = get_font(45).render("This is the start screen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        window.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def write2database(name, score, mode):
    # easy one
    if mode == 1:
        with open("/Users/pongsakorn/Documents/draft999/data/easy.csv", 'a', newline="") as f:
            writer = csv.writer(f)
            writer.writerow([name, score])
    # hard one
    elif mode == 2:
        with open("/Users/pongsakorn/Documents/draft999/data/hard.csv", 'a', newline="") as f:
            writer = csv.writer(f)
            writer.writerow([name, score])

# Read high scores from database
def read2database(mode):
    # easy one
    if mode == 1:
        with open("/Users/pongsakorn/Documents/draft999/data/easy.csv", newline="") as f:
            reader = csv.reader(f)
            data = np.array([row for row in reader])
    # hard one
    elif mode == 2:
        with open("/Users/pongsakorn/Documents/draft999/data/hard.csv", newline="") as f:
            reader = csv.reader(f)
            data = np.array([row for row in reader])

    names = np.array(data[:, 0], dtype=str)
    scores = np.array(data[:, 1], dtype=int)
    argc = np.argmax(scores)

    return names[argc], scores[argc]

def finish(name, mode, score):
    global yScores

    # Store the score of this time in the array
    yScores.append(score)

    # Calculate the maximum value in the array
    yHighscore = max(yScores)

    # Write this time score to the database
    write2database(name, score, mode)

    # Read overall high scores from database
    high_name, highscore = read2database(mode)

    while True:
        window.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        FINISH_TEXT = get_font(100).render(str(name) + "  WIN!!", True, "#b68f40")
        FINISH_RECT = FINISH_TEXT.get_rect(center=(640, 100))

        SCORE_TEXT = get_font(50).render("SCORE " + str(score), True, "#b68f40")
        SCORE_RECT = SCORE_TEXT.get_rect(center=(640, 220))

        YHIGHSCORE_TEXT = get_font(50).render("YOUR HIGH SCORE " + str(yHighscore), True, "#b68f40")
        YHIGHSCORE_RECT = YHIGHSCORE_TEXT.get_rect(center=(640, 320))

        HIGHSCORE_TEXT = get_font(50).render("HIGH SCORE:" + high_name + "/" + str(highscore), True, "#b68f40")
        HIGHSCORE_RECT = HIGHSCORE_TEXT.get_rect(center=(640, 420))

        AGAIN_BUTTON = Button(image=pygame.image.load("/Users/pongsakorn/Documents/draft999/assets/Quit Rect.png"), pos=(250, 600), 
                            text_input="PLAY AGAIN", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
        NEW_BUTTON = Button(image=pygame.image.load("/Users/pongsakorn/Documents/draft999/assets/Quit Rect.png"), pos=(640, 600), 
                            text_input="NEW PLAYER", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("/Users/pongsakorn/Documents/draft999/assets/Quit Rect.png"), pos=(1030, 600), 
                            text_input="QUIT", font=get_font(50), base_color="#d7fcd4", hovering_color="White")

        window.blit(FINISH_TEXT, FINISH_RECT)
        window.blit(SCORE_TEXT, SCORE_RECT)
        window.blit(YHIGHSCORE_TEXT, YHIGHSCORE_RECT)
        window.blit(HIGHSCORE_TEXT, HIGHSCORE_RECT)

        for button in [AGAIN_BUTTON, NEW_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(window)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if AGAIN_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play.Play(window, manager, clock, name, score, mode)
                if NEW_BUTTON.checkForInput(MENU_MOUSE_POS):
                    yScores = []
                    main(name, score, mode)
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

