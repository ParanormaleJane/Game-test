import pygame
from pygame import *

width = 800
height = 640
display = (width, height)
platform_width = 32
platform_height = 32
moution_speed = 10
player_width = 22
player_height = 32
color = "#888888"
power_jump = 10
gravitation = 0.55


class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.yono = 0
        self.kono = 0
        self.onGround = False
        self.startX = x
        self.startY = y
        self.image = Surface((player_width, player_height))
        self.image.fill(Color(color))
        self.rect = Rect(x, y, player_width, player_height)

    def update(self, left, right, up, platforms):
        if up:
            if self.onGround:
                self.kono = -power_jump
        if left:
            self.yono = -moution_speed

        if right:
            self.yono = moution_speed

        if not (left or right):
            self.yono = 0
            self.kono += gravitation

        self.onGround = False
        self.rect.y += self.kono
        self.collide(0, self.kono, platforms)

        self.rect.x += self.yono
        self.collide(self.yono, 0, platforms)

    def collide(self, yono, kono, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):

                if yono > 0:
                    self.rect.right = p.rect.left

                if yono < 0:
                    self.rect.left = p.rect.right

                if kono > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.kono = 0

                if kono < 0:
                    self.rect.top = p.rect.bottom
                    self.kono = 0


class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((platform_width, platform_height))
        self.image = image.load("Block_level_1.png")
        self.rect = Rect(x, y, platform_width, platform_height)


class Button:
    def __init__(self, position, size, clr=[100, 100, 100], cngclr=None, func=None, text='', font="Bonzai", font_size=40, font_clr=[0, 0, 0]):
        self.clr = clr
        self.size = size
        self.func = func
        self.surf = pygame.Surface(size)
        self.rect = self.surf.get_rect(center=position)

        if cngclr:
            self.cngclr = cngclr
        else:
            self.cngclr = clr

        self.font = pygame.font.SysFont(font, font_size)
        self.txt = text
        self.font_clr = font_clr
        self.txt_surf = self.font.render(self.txt, True, self.font_clr)
        self.txt_rect = self.txt_surf.get_rect(center=[wh//2 for wh in self.size])

    def draw(self, screen):
        self.mouseover()

        self.surf.fill(self.curclr)
        self.surf.blit(self.txt_surf, self.txt_rect)
        screen.blit(self.surf, self.rect)

    def mouseover(self):
        self.curclr = self.clr
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.curclr = self.cngclr

    def call_back(self, *args):
        if self.func:
            pygame.mixer.Sound.play(button_sound).set_volume(1)
            pygame.time.delay(300)
            return self.func(*args)


def game():
    pygame.init()
    screen = pygame.display.set_mode(display)
    pygame.display.set_caption("Enextine")
    background = pygame.image.load('Level_wall_1.jpg')
    hero = Player(55, 55)
    left = right = False
    up = False
    entities = pygame.sprite.Group()
    platforms = []
    entities.add(hero)
    level = [
        "-------------------------",
        "-                       -",
        "-                       -",
        "-                       -",
        "-            --         -",
        "-                       -",
        "--                      -",
        "-                       -",
        "-                   --- -",
        "-                       -",
        "-                       -",
        "-      ---              -",
        "-                       -",
        "-   -----------        -",
        "-                       -",
        "-                -      -",
        "-                   --  -",
        "-                       -",
        "-                       -",
        "-------------------------"]
    timer = pygame.time.Clock()

    while 1:
        timer.tick(60)
        for e in pygame.event.get():
            if e.type == QUIT:
                raise SystemExit
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYDOWN and e.key == K_SPACE:
                up = True
            if e.type == KEYUP and e.key == K_SPACE:
                up = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
        screen.blit(background, (0, 0))
        hero.update(left, right, up, platforms)
        entities.draw(screen)
        x = y = 0
        for row in level:
            for col in row:
                if col == "-":
                    pf = Platform(x, y)
                    entities.add(pf)
                    platforms.append(pf)

                x += platform_width
            y += platform_height
            x = 0
        pygame.display.update()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Enextine')
    font_score = pygame.font.SysFont('Bonzai.ttf', 26, bold=True)
    font_end = pygame.font.SysFont('Bonzai.ttf', 76, bold=True)
    img = pygame.image.load('8a36117830713c529bb94c295c5255b5.png')

    screen_size = (800, 800)
    size = 10
    bg = (0, 0, 0)
    font_size = 15
    font = pygame.font.Font(None, font_size)
    clock = pygame.time.Clock()
    button_sound = pygame.mixer.Sound('buton.mp3')
    fon_sound = pygame.mixer.Sound('ce8e6287c767e45.mp3')

    screen = pygame.display.set_mode(screen_size)
    screen.blit(img, (0, 0))

    crash = True
    while crash:
        start = Button((400, 400), (400, 100), [220, 220, 220], (147, 112, 219), game, 'start')
        Close = Button((400, 600), (400, 100), [220, 220, 220], (147, 112, 219), exit, 'exit')
        button_list = [start, Close]
        fon_sound.set_volume(0.1)
        fon_sound.play(-1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                def exit():
                    crash = False
            if event.type == pygame.QUIT:
                crash = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    crash = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    fon_sound.stop()
                    pos = pygame.mouse.get_pos()
                    for b in button_list:
                        if b.rect.collidepoint(pos):
                            b.call_back()

        for b in button_list:
            b.draw(screen)

        pygame.display.update()
        clock.tick(15)
