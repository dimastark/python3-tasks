# -*- coding: utf-8 -*-
#!/usr/bin/python3

"""The GIU for application"""


from arch import GameBoard
from arch import no_inderr
import pygame as pg
import random as rnd
import time
import start
import sys
import scores as sc

WIN_W = WIN_H = 800
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
FIOL = (255, 0, 255)
GREY = (127, 127, 127)
PINK = (241, 156, 187)
AZURE = (0, 127, 255)
BLACK = (0, 0, 0)
COLORS = [WHITE, RED, YELLOW, GREEN, BLUE, FIOL, GREY, PINK, AZURE, BLACK]


class Button:
    """Button class for pygame"""
    def __init__(self, coord, size, text):
        '''Make button'''
        self.coord = coord
        self.size = size
        self.text = text

    def draw_button(self, screen):
        '''Draw a button'''
        mouse = pg.mouse.get_pos()
        if self.in_button(mouse):
            pg.draw.rect(screen, BLACK, self.coord + self.size, 3)
            draw_text(screen, self.text, self.coord[0]+5, self.coord[1]+5, 31)
        else:
            draw_text(screen, self.text, self.coord[0]+10, self.coord[1]+10, 22)

    def in_button(self, coord):
        '''Return True if "coord" in button'''
        return self.coord[0]+self.size[0] > coord[0] > self.coord[0] \
        and self.coord[1]+self.size[1] > coord[1] > self.coord[1]


def draw_text(screen, text, x_pos, y_pos, size):
    '''Draws the specified text at the specified coordinates

    Args:
      screen: the display, where need draw
      text: text for drawing
      x_pos, y_pos: coordinates x and y on screen
      size: the size of text

    Note: The text is black
    '''
    if no_inderr(WIN_H + 50, x_pos, y_pos):
        font_style = pg.font.SysFont("None", size)
        font_image = font_style.render(text, 0, BLACK)
        screen.blit(font_image, (x_pos, y_pos))


def draw_way(screen, way, rang):
    '''Draws the specified text at the specified coordinates

    Args:
      screen: the display, where need draw
      way: list of steps
      rang: size of platform
    '''
    for step in way[::-1]:
        time.sleep(rang/2000)
        coords = (((step[0]-1)*rang+3*rang/8, (step[1]-1)*rang+3*rang/8))
        rect = pg.Rect(coords, (rang/4, rang/4))
        pg.draw.rect(screen, random_color(), rect, 0)
        pg.draw.rect(screen, BLACK, rect, 1)
        pg.display.update()


def draw_next(screen, circles, colors, rang):
    '''Draws the specified text at the specified coordinates

    Args:
      screen: the display, where need draw
      circles: list next circles
      colors: list of colors
      rang: size of circle

    Note: The text is black
    '''
    for circle in circles:
        coords = (circle[0]*rang+rang/4, circle[1]*rang+rang/4)
        rect = pg.Rect(coords, (rang/2, rang/2))
        pg.draw.rect(screen, (colors[circle[2]]), rect, 3)
        draw_text(screen, str(circle[2]), coords[0]+rang/16, coords[1]+rang/16, 23)
    pg.display.update()


def draw_readme(screen):
    '''Draw readme text on screen'''
    draw_text(screen, "THIS IS README", 40, 40, 100)
    rdm = []
    try:
        file = open("readme.txt", encoding='utf-8')
    except IOError:
        rdm.append("HOW DARE YOU?")
    else:
        try:
            for line in file:
                rdm.append(line[:-1])
        finally:
            file.close()
    y_pos = 140
    for line in rdm:
        if y_pos > 850:
            break
        draw_text(screen, line, 40, y_pos, 30)
        y_pos += 30


def random_color():
    '''Generate random color'''
    r_spec = rnd.randrange(0, 256)
    g_spec = rnd.randrange(0, 256)
    b_spec = rnd.randrange(0, 256)
    return r_spec, g_spec, b_spec


def draw_field(screen, board, platform_rang):
    '''Draw board's field on screen

    Args:
      screen: display parameters
      platform_rang: size of block
    '''
    x_pos = y_pos = 0
    lines = str(board).split('\n')
    for line in lines:
        for char in line:
            rect = pg.Rect((x_pos, y_pos), (platform_rang, platform_rang))
            pg.draw.rect(screen, BLACK, rect, 4)
            pg.draw.rect(screen, COLORS[int(char)], rect, 0)
            if char != '0':
                draw_text(screen, char, x_pos+4, y_pos+4, 23)
            x_pos += platform_rang
        y_pos += platform_rang
        x_pos = 0


def point_click(screen, point_x, point_y, platform_rang):
    '''Point block, when clicked

       Args:
         screen: display parameters
         point_x, point_y: coordinates of click
         platform_rang: size of block
    '''
    if not -1 == point_x == point_y:
        rect = pg.Rect((point_x, point_y), (platform_rang, platform_rang))
        pg.draw.rect(screen, COLORS[rnd.randrange(1, 5)], rect, 4)


def game(rang, combo, count_colors):
    """The main entry point for the application"""
    platform_rang = WIN_H / rang
    reset = Button((500, 810), (90, 30), "Reset")
    scores = Button((600, 810), (90, 30), "Scores")
    readme = Button((700, 810), (90, 30), "Readme")
    loop = True
    click = False
    screen = pg.display.set_mode((WIN_W, WIN_H+50))
    pg.display.set_caption("Lines")
    board = GameBoard(rang, combo, count_colors)
    point_x = point_y = -1
    pg.init()
    while loop:
        screen.fill(COLORS[0])
        draw_field(screen, board, platform_rang)
        point_click(screen, point_x, point_y, platform_rang)
        draw_text(screen, "Score: " + str(board.get_score()), 20, 805, 40)
        reset.draw_button(screen)
        readme.draw_button(screen)
        scores.draw_button(screen)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                loop = False
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse = pg.mouse.get_pos()
                if reset.in_button(mouse):
                    pg.quit()
                    start.main()
                    sys.exit()
                if scores.in_button(mouse):
                    back = Button((600, 810), (150, 30), "Back to game")
                    scoreloop = True
                    scr = sc.get_scores()
                    while scoreloop:
                        for event in pg.event.get():
                            if event.type == pg.QUIT:
                                pg.quit()
                                sys.exit()
                            if event.type == pg.MOUSEBUTTONDOWN:
                                if back.in_button(pg.mouse.get_pos()):
                                    scoreloop = False
                        y_pos = 0
                        screen.fill(COLORS[0])
                        draw_text(screen, "Scores:", 30, y_pos, 50)
                        y_pos += 50
                        for line in scr:
                            if y_pos > 800:
                                break
                            draw_text(screen, line, 40, y_pos, 25)
                            y_pos += 20
                        back.draw_button(screen)
                        pg.display.update()
                    break
                if readme.in_button(mouse):
                    back = Button((600, 810), (150, 30), "Back to game")
                    readmeloop = True
                    while readmeloop:
                        for event in pg.event.get():
                            if event.type == pg.QUIT:
                                pg.quit()
                                sys.exit()
                            if event.type == pg.MOUSEBUTTONDOWN:
                                if back.in_button(pg.mouse.get_pos()):
                                    readmeloop = False
                        screen.fill(COLORS[0])
                        draw_readme(screen)
                        back.draw_button(screen)
                        pg.display.update()
                    break
                if not click:
                    (x_pos, y_pos) = pg.mouse.get_pos()
                    x_f = int(x_pos // platform_rang)
                    y_f = int(y_pos // platform_rang)
                    if board.get_value(x_f, y_f) != 0 and board.get_value(x_f, y_f):
                        point_x = x_f * platform_rang
                        point_y = y_f * platform_rang
                        click = True
                else:
                    (x_pos, y_pos) = pg.mouse.get_pos()
                    x_s = int(x_pos // platform_rang)
                    y_s = int(y_pos // platform_rang)
                    if board.get_value(x_s, y_s) != 0 and board.get_value(x_s, y_s):
                        x_f = x_s
                        y_f = y_s
                        point_x = x_f * platform_rang
                        point_y = y_f * platform_rang
                    else:
                        way = board.make_move((x_f, y_f), (x_s, y_s))
                        if way:
                            draw_way(screen, way, platform_rang)
                        click = False
                        point_x = -1
                        point_y = -1
        if board.adds:
            draw_next(screen, board.adds, COLORS, platform_rang)
        if str(board).count('0') == 0:
            loop = False
        if str(board).count('0') == rang*rang:
            board.stand_circles()
            board.add_circles(rang//3)
        pg.display.update()
    pg.quit()
    return board.get_score()
