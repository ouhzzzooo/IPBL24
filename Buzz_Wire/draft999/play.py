import pygame
import sys
from button import Button
from utils import get_font

def Play(window, manager, clock, name, score, mode):
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        window.fill("black")
        
        PLAY_TEXT = get_font(75).render("LEVEL", True, "#FEC85A")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 125))
        window.blit(PLAY_TEXT, PLAY_RECT)
        
        EASY_BUTTON = Button(image=None, pos=(640, 325), 
                            text_input="EASY", font=get_font(60), base_color="#F5FFF4", hovering_color="Green")
        
        HARD_BUTTON = Button(image=None, pos=(640, 475), 
                            text_input="HARD", font=get_font(60), base_color="#F5FFF4", hovering_color="Red")

        PLAY_BACK = Button(image=None, pos=(640, 675), 
                            text_input="BACK", font=get_font(35), base_color="#F5FFF4", hovering_color="Orange")
        
        EASY_BUTTON.changeColor(PLAY_MOUSE_POS)
        EASY_BUTTON.update(window)

        HARD_BUTTON.changeColor(PLAY_MOUSE_POS)
        HARD_BUTTON.update(window)

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    from main2 import main
                    main()
                if EASY_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    from how_to_play import How_to_play_Easy
                    mode = 1
                    How_to_play_Easy(window, manager, clock, name, score, mode)
                if HARD_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    from how_to_play import How_to_play_Hard
                    mode = 2
                    How_to_play_Hard(window, manager, clock, name, score, mode)

        pygame.display.update()
