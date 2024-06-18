import pygame
import pygame_gui
import sys
from button import Button
from utils import get_font

pygame.init()

# Screen setup
window_width, window_height = 1280, 720
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Menu")

# Background and font
BG = pygame.image.load("/Users/pongsakorn/Documents/draft999/assets/AllBlack.png")
manager = pygame_gui.UIManager((window_width, window_height))
text_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((650, 500), (300, 50)), manager=manager)
clock = pygame.time.Clock()

score = 0
name = ""
mode = 0

def starting_time():
    start_tt = pygame.time.get_ticks()
    return start_tt

def ending_tt():
    end_tt = pygame.time.get_ticks()
    return end_tt

def main_menu(name, score, mode):
    while True:
        window.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("BUZZ WIRE", True, "#FEC85A")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 150))

        PLAY_BUTTON = Button(image=None, pos=(640, 350), 
                            text_input="PLAY", font=get_font(75), base_color="#FEFFDE", hovering_color="Yellow")
        QUIT_BUTTON = Button(image=None, pos=(640, 675), 
                            text_input="QUIT", font=get_font(35), base_color="#FEFFDE", hovering_color="Red")                  
        
        NAME_TEXT = get_font(55).render("NAME:", True, "#FEC85A")
        NAME_RECT = NAME_TEXT.get_rect(center=(500, 525))
        
        window.blit(MENU_TEXT, MENU_RECT)
        window.blit(NAME_TEXT, NAME_RECT)
        
        SUBMIT_BUTTON = Button(image=None, pos=(1080, 525), 
                               text_input="SUBMIT", font=get_font(35), base_color="#FEFFDE", hovering_color="Green")

        for button in [PLAY_BUTTON, QUIT_BUTTON, SUBMIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(window)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if SUBMIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    name = text_input.get_text()  # Save the text input to the 'name' variable
                    print(name)
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    from play import Play
                    Play(window, manager, clock, name, score, mode)
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
            manager.process_events(event)

        UI_REFRESH_RATE = clock.tick(60) / 1000
        manager.update(UI_REFRESH_RATE)
        manager.draw_ui(window)

        pygame.display.update()
        
def main(name, score, mode):
    main_menu(name, score, mode)

if __name__ == "__main__":
    main(name, score, mode)




