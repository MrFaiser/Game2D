import main
from main import *
from settings import *


def Option():

    hovered = False

    def __init__(self, text, pos):
        self.rect = None
        self.rend = None
        self.text = text
        self.pos = pos
        self.set_rect()
        self.draw()

    def draw(self):
        self.set_rend()
        screen.blit(self.rend, self.rect)

    def set_rend(self):
        self.rend = menu_font.render(self.text, True, self.get_color())

    def get_color(self):
        if self.hovered:
            return 255, 255, 255
        else:
            return 100, 100, 100

    def set_rect(self):
        self.set_rend()
        self.rect = self.rend.get_rect()
        self.rect.topleft = self.pos


    pygame.init()
    W, H = 480, 500
    screen = pygame.display.set_mode((W, H))
    menu_font = pygame.font.Font(None, 40)
    options =   {
                    (START_TEXT, (W / 4, H/2-50))      ,
                    (OPTION_TEXT, (W / 4, H/2))        ,
                    (QUIT_TEXT, (W / 4, H/2+50))
    }
    while True:
        pygame.event.pump()
        screen.fill((0, 0, 100))
        for option in options:
            if option.rect.collidepoint(pygame.mouse.get_pos()):
                option.hovered = True
                for ev in pygame.event.get():
                    if ev.type == pygame.MOUSEBUTTONDOWN:
                        if option.text == START_TEXT:
                            print("start")
                            #main.Game
                        elif option.text == OPTION_TEXT:
                            print("op")
                        elif option.text == QUIT_TEXT:
                            print("quit")
                            quit()
            else:
                option.hovered = False
            option.draw()

        pygame.display.update()


Option()