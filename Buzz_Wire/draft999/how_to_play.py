import pygame
import sys
from button import Button
from utils import get_font
import game_loop
from main2 import starting_time
import hardgame


def How_to_play_Easy(window, manager, clock, name, score, mode):
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        window.fill("black")
        
        HTP_TEXT = get_font(75).render("HOW TO PLAY", True, "#FEC85A")
        HTP_RECT = HTP_TEXT.get_rect(center=(640, 125))
        window.blit(HTP_TEXT, HTP_RECT)

        FIRST_TEXT = get_font(20).render("1. Use your fingertip", True, "WHITE")
        FIRST_RECT = FIRST_TEXT.get_rect(center=(640, 250))
        window.blit(FIRST_TEXT, FIRST_RECT)
        
        FIRST_TEXT = get_font(20).render("2. If touching the wall game will restart", True, "WHITE")
        FIRST_RECT = FIRST_TEXT.get_rect(center=(640, 375))
        window.blit(FIRST_TEXT, FIRST_RECT)
        
        FIRST_TEXT = get_font(20).render("3. Score will depend on how fast you finish the game", True, "WHITE")
        FIRST_RECT = FIRST_TEXT.get_rect(center=(640, 500))
        window.blit(FIRST_TEXT, FIRST_RECT)
        
        FIRST_TEXT = get_font(20).render("4. Starting from the red box go to the goal at green box", True, "WHITE")
        FIRST_RECT = FIRST_TEXT.get_rect(center=(640, 600))
        window.blit(FIRST_TEXT, FIRST_RECT)
       
        PLAY_BACK = Button(image=None, pos=(100, 675), 
                            text_input="BACK", font=get_font(35), base_color="#F5FFF4", hovering_color="Orange")
        START_PLAY = Button(image=None, pos=(1180, 675), 
                            text_input="START", font=get_font(35), base_color="#F5FFF4", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(window)

        START_PLAY.changeColor(PLAY_MOUSE_POS)
        START_PLAY.update(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    from play import Play
                    Play(window, manager, clock, name, score, mode)
                if START_PLAY.checkForInput(PLAY_MOUSE_POS):
                    start_tt = starting_time()
                    game_loop.game_loop(window, manager, clock, name, mode, start_tt)
        pygame.display.update()
        
        
        
def How_to_play_Hard(window, manager, clock, name, score, mode):
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        window.fill("black")
        
        HTP_TEXT = get_font(75).render("HOW TO PLAY", True, "#FEC85A")
        HTP_RECT = HTP_TEXT.get_rect(center=(640, 125))
        window.blit(HTP_TEXT, HTP_RECT)

        FIRST_TEXT = get_font(20).render("1. Use your nosetip to play", True, "WHITE")
        FIRST_RECT = FIRST_TEXT.get_rect(center=(640, 250))
        window.blit(FIRST_TEXT, FIRST_RECT)
        
        FIRST_TEXT = get_font(20).render("2. Stay inside the curve to increase your score", True, "WHITE")
        FIRST_RECT = FIRST_TEXT.get_rect(center=(640, 375))
        window.blit(FIRST_TEXT, FIRST_RECT)
        
        FIRST_TEXT = get_font(20).render("3. This game will take 60 second", True, "WHITE")
        FIRST_RECT = FIRST_TEXT.get_rect(center=(640, 500))
        window.blit(FIRST_TEXT, FIRST_RECT)
       
        PLAY_BACK = Button(image=None, pos=(100, 675), 
                            text_input="BACK", font=get_font(35), base_color="#F5FFF4", hovering_color="Orange")
        START_PLAY = Button(image=None, pos=(1180, 675), 
                            text_input="START", font=get_font(35), base_color="#F5FFF4", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(window)

        START_PLAY.changeColor(PLAY_MOUSE_POS)
        START_PLAY.update(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    from play import Play
                    Play(window, manager, clock, name, score, mode)
                if START_PLAY.checkForInput(PLAY_MOUSE_POS):
                    hardgame.hardgame(window, manager, clock, name, mode)
        pygame.display.update()
