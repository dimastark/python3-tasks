"""Module of GUI of Conway's Life"""
# TODO: Какой говнокод... Как же я раньше это все писал
# TODO: Надо сделать нормально. Как-нибудь...
import os
import sys
import time
from collections import namedtuple
from threading import Thread

import pygame as pg

import lifearch as l

THR = None
DELTA1 = 0
DELTA2 = 0
PWD = os.path.dirname(os.path.abspath(__file__))


class Button:
    """Button class for pygame"""
    def __init__(self, coord, size, text):
        """Make button"""
        self.coord = coord
        self.size = size
        self.text = text

    def draw_button(self, screen):
        """Draw a button"""
        mouse = pg.mouse.get_pos()
        if self.in_button(mouse):
            pg.draw.rect(screen, BLACK, self.coord + self.size, 2)
            draw_text(screen, self.text, self.coord[0]+5, self.coord[1]+5, self.size[1])
        else:
            draw_text(screen, self.text, self.coord[0]+10, self.coord[1]+10, self.size[1] - 10)

    def in_button(self, coord):
        """Return True if "coord" in button"""
        return self.coord[0]+self.size[0] > coord[0] > self.coord[0] \
        and self.coord[1]+self.size[1] > coord[1] > self.coord[1]


def drange(start, stop, step):
    """decimal range()"""
    ranger = start
    while ranger < stop:
        yield ranger
        ranger += step


def draw_text(screen, text, x_pos, y_pos, size):
    """Draws the specified text at the specified coordinates

    Args:
      screen: the display, where need draw
      text: text for drawing
      x_pos, y_pos: coordinates x and y on screen
      size: the size of text

    Note: The text is black
    """
    font_style = pg.font.SysFont("None", size)
    font_image = font_style.render(text, 0, BLACK)
    screen.blit(font_image, (x_pos, y_pos))


def draw_in(x_pos, y_pos, rang, screen):
    """Draw cells in coordinates"""
    rect = pg.Rect((x_pos, y_pos), (rang, rang))
    pg.draw.rect(screen, RED, rect, 0)
    pg.draw.rect(screen, BLACK, rect, 1)


def no_inderr(bord, *values):
    """Return Returns true if all values greater
    or equal than zero and less than the permissible boundaries

    Args:
      bord: limit for the values
      *values: values, that need to check
    """
    for value in values:
        if 0 > value or value >= bord:
            return False
    return True


def draw_life(screen, points, cell_size):
    """Draw all cells
        args:
            delta1: first delta
            delta2: second delta
            cell_size: size of cell
            points: field
    """
    for i in points:
        if points.cells[i][0] == 1:
            draw_in(i.x*cell_size+DELTA1, i.y*cell_size+DELTA2, cell_size, screen)
    new_d1 = DELTA1
    new_d2 = DELTA2
    while new_d1 > 0:
        new_d1 -= cell_size
    while new_d2 > 0:
        new_d2 -= cell_size
    for i in drange(new_d1, 600, cell_size):
        for j in drange(new_d2, 600, cell_size):
            rect = pg.Rect((i, j), (cell_size, cell_size))
            pg.draw.rect(screen, GREY, rect, 1)
    rect = pg.Rect((0, 600), (600, 50))
    pg.draw.rect(screen, WHITE, rect, 0)


def quit_event(event):
    """Closing app"""
    if event.type == pg.QUIT:
        pg.quit()
        sys.exit()


def readme_event(screen):
    """Draw readme"""
    back = Button((300, WIN_H+10), (150, 30), "Back to game")
    readme_loop = True
    while readme_loop:
        for event in pg.event.get():
            quit_event(event)
            if event.type == pg.MOUSEBUTTONDOWN:
                if back.in_button(pg.mouse.get_pos()):
                    readme_loop = False
        screen.fill((255, 255, 255))
        draw_readme(screen)
        back.draw_button(screen)
        pg.display.update()


def rew_event(screen, points, size):
    """Event for rew button"""
    start_time = time.clock()
    ticker = 0
    rew = Button((WIN_H-100, WIN_H+10), BUTTON_SIZE, ">")
    rew.draw_button(screen)
    not_click = True
    speed = 50
    while not_click:
        for event in pg.event.get():
            quit_event(event)
            if event.type == pg.KEYDOWN:
                points = keydown_event(screen, event, points, size, True)
            if event.type == pg.MOUSEBUTTONDOWN:
                if rew.in_button(pg.mouse.get_pos()):
                    if speed <= 300:
                        speed += 50
                        rew.text += '>'
                    else:
                        speed = 50
                        rew.text = '>'
                else:
                    not_click = False
        screen.fill(WHITE)
        if time.clock() - start_time > ticker:
            points.new_generation()
            ticker += 15 / speed
        draw_life(screen, points, size[0])
        rew.draw_button(screen)
        pg.display.update()
    return size


def motion_event(points, cell_size):
    """Event, when mouse move"""
    x_pos, y_pos = pg.mouse.get_pos()
    if pg.mouse.get_pressed()[0]:
        x_s = int((x_pos - DELTA1) // cell_size)
        y_s = int((y_pos - DELTA2) // cell_size)
        coords = COORDS(x=x_s, y=y_s)
        if points.cells.get(coords, (0, 0))[0] == 0 and no_inderr(600, x_pos, y_pos):
            points.add(l.Point(x_s, y_s))
            EDEN.text = "?(slow)"


def right_mouse_event(points, cell_size):
    """Event, when click right button of mouse"""
    x_pos, y_pos = pg.mouse.get_pos()
    x_s = int((x_pos - DELTA1) // cell_size)
    y_s = int((y_pos - DELTA2) // cell_size)
    coords = COORDS(x=x_s, y=y_s)
    if no_inderr(600, x_pos, y_pos):
        EDEN.text = "?(slow)"
        if points.cells.get(coords, (0, 0))[0] == 1:
            points.remove(x_s, y_s)
        else:
            points.add(l.Point(x_s, y_s))


def save_game(name, points):
    """Saving game
        args:
            name: save name
            points: field to save
    """
    if len(points.cells) > 0:
        with open(os.path.join(PWD, "saves.txt"), mode='w', encoding='utf-8') as file:
            file.write(str(name)+':')
            for key in points.cells:
                if points.cells[key][0] != 0:
                    file.write(str(key.x)+','+str(key.y)+'|')
            file.write('\n')


def delete_save(name):
    """Deleting the save
        args:
            name: save name
    """
    with open(os.path.join(PWD, "saves.txt"), mode='r', encoding='utf-8') as file:
        content = file.readlines()
    with open(os.path.join(PWD, "saves.txt"), mode='w', encoding='utf-8') as file:
        for line in content:
            if not line[0] == name:
                file.write(line)


def save_event(screen, points):
    """Event for 'SAVE' button"""
    not_key = True
    backspace = False
    while not_key:
        screen.fill(WHITE)
        draw_text(screen, "Assign button or press the backspace, to return", 10, 300, 20)
        pg.display.update()
        for _event in pg.event.get():
            quit_event(_event)
            if _event.type == pg.KEYDOWN:
                name = pg.key.name(_event.key)
                not_key = False
                if name == "backspace":
                    backspace = True
    if not backspace:
        if not load_event(name) and len(name) == 1:
            save_game(name, points)
        else:
            draw_text(screen,
                      "This name already exist, press again for rewrite or press other for return",
                      10, 350, 20)
            pg.display.update()
            not_press = True
            while not_press:
                for _event in pg.event.get():
                    quit_event(_event)
                    if _event.type == pg.KEYDOWN:
                        second_name = pg.key.name(_event.key)
                        not_press = False
                        if second_name == name:
                            delete_save(second_name)
                            save_game(second_name, points)
                        else:
                            save_event(screen, points)


def load_event(name):
    """Load the game with 'name'"""
    try:
        points = l.Life()
        with open(os.path.join(PWD, "saves.txt"), mode='r', encoding='utf-8') as file:
            for line in file:
                if line[0] == str(name):
                    points = copy_points(line.split(':')[1][:-2])
                    break
        if len(points.cells) > 0:
            return points
    except:
        return None


def copy_points(line):
    """Make Life str => Life conversation"""
    cells = line.split('|')
    dct = l.Life()
    for cell in cells:
        x_str, y_str = cell.split(',')
        x_pos = int(x_str)
        y_pos = int(y_str)
        dct.add(l.Point(x_pos, y_pos))
    return dct


def draw_readme(screen):
    """Draw readme text on screen"""
    start = 40
    linesize = 30
    draw_text(screen, "THIS IS README", start, start, linesize)
    rdm = [
        'The Conwey`s game "Life"',
        '- - - - - - - - - - - - - - - - - - - - - - -',
        'Rules:',
        '% Any live cell with fewer than two live neighbours',
        'dies, as if caused by under-population.',
        '% Any live cell with two or three live neighbours',
        'lives on to the next generation.',
        '% Any live cell with more than three live neighbours',
        'dies, as if by overcrowding.',
        '% Any dead cell with exactly three live neighbours',
        'becomes a live cell, as if by reproduction.',
        '',
        '(DimaStark) Dmitry Starkov 2015',
    ]
    y_pos = 3 * linesize
    for line in rdm:
        draw_text(screen, line, start, y_pos, linesize)
        y_pos += linesize


def moving(screen, points, size, parall):
    """Move the screen"""
    global DELTA1, DELTA2
    loop1 = True
    ticker1 = 0
    ticker2 = 0
    start_time = time.clock()
    while loop1:
        first = second = False
        if pg.key.get_pressed()[pg.K_LEFT] != 0:
            first = True
            DELTA1, ticker1, loop1 = dir_key((ticker1, start_time), DELTA1, size[1], 1)
        elif pg.key.get_pressed()[pg.K_RIGHT] != 0:
            first = True
            DELTA1, ticker1, loop1 = dir_key((ticker1, start_time), DELTA1, size[1], -1)
        if pg.key.get_pressed()[pg.K_UP] != 0:
            second = True
            DELTA2, ticker2, loop1 = dir_key((ticker2, start_time), DELTA2, size[1], 1)
        elif pg.key.get_pressed()[pg.K_DOWN] != 0:
            second = True
            DELTA2, ticker2, loop1 = dir_key((ticker2, start_time), DELTA2, size[1], -1)
        if not (first or second):
            loop1 = False
        if not parall:
            screen.fill(WHITE)
            draw_life(screen, points, size[0])
            pg.display.update()


def keydown_event(screen, event, points, size, parall):
    """Event, when key down"""
    global THR
    _ = pg.key.name(event.key)
    if _ != "left" and _ != "right" and _ != "up" and _ != "down" and not parall:
        new = load_event(_)
        if new:
            if len(new.cells) > 0:
                points = new
    else:
        if parall:
            if not THR:
                THR = Thread(target=moving, args=(screen, points, size, True))
                THR.start()
            elif not THR.is_alive():
                THR = Thread(target=moving, args=(screen, points, size, True))
                THR.start()
        else:
            moving(screen, points, size, False)
    return points


def dir_key(times, delta, rang, fact):
    """When press key of direction"""
    loop1 = True
    ticker = times[0]
    start_time = times[1]
    for event in pg.event.get():
        quit_event(event)
        if event.type == pg.KEYUP:
            keys = pg.key.get_pressed()
            if keys[pg.K_UP] == keys[pg.K_DOWN] == keys[pg.K_LEFT] == keys[pg.K_RIGHT] == 0:
                loop1 = False
    if time.clock() - start_time > ticker:
        delta += fact * 2
        ticker += 1 / (rang * 6)
    return delta, ticker, loop1


def eden_event(points):
    """Event for 'EDEN' button"""
    st_bool = str(points.is_eden())
    EDEN.text = st_bool


WIN_W = WIN_H = 600
BUTTON_SIZE = (90, 30)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
COORDS = namedtuple("Coords", ["x", "y"])
EVOL = Button((WIN_H-300, WIN_H+10), BUTTON_SIZE, "Eval")
CLEAR = Button((WIN_H-200, WIN_H+10), BUTTON_SIZE, "Clear")
REW = Button((WIN_H-100, WIN_H+10), BUTTON_SIZE, "Rewind")
README = Button((WIN_H-500, WIN_H+10), BUTTON_SIZE, "Readme")
SAVE = Button((WIN_H-400, WIN_H+10), BUTTON_SIZE, "Save")
EDEN = Button((WIN_H-600, WIN_H+10), BUTTON_SIZE, "?(slow)")
BUTTONS = [EVOL, CLEAR, REW, README, SAVE, EDEN]


def draw_all_buttons(screen, buttons):
    """Draw all 'buttons'"""
    for button in buttons:
        button.draw_button(screen)


def main():
    """The main entry point for the application"""
    global DELTA1, DELTA2
    DELTA1 = DELTA2 = 300
    points = l.Life()
    rang = 10
    cell_size = WIN_H / rang
    loop = True
    screen = pg.display.set_mode((WIN_W, WIN_H+50))
    pg.display.set_caption("Life")
    pg.init()
    while loop:
        size = (cell_size, rang)
        screen.fill(WHITE)
        draw_life(screen, points, cell_size)
        draw_all_buttons(screen, BUTTONS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                loop = False
            if event.type == pg.MOUSEMOTION:
                motion_event(points, cell_size)
            if event.type == pg.KEYDOWN:
                EDEN.text = "?(slow)"
                points = keydown_event(screen, event, points, size, False)
            if event.type == pg.MOUSEBUTTONDOWN:
                if pg.mouse.get_pressed()[0]:
                    x_pos, y_pos = pg.mouse.get_pos()
                    right_mouse_event(points, cell_size)
                    if CLEAR.in_button((x_pos, y_pos)):
                        EDEN.text = "False"
                        points = l.Life()
                        DELTA1 = DELTA2 = 300
                    if EVOL.in_button((x_pos, y_pos)):
                        EDEN.text = "False"
                        points.new_generation()
                    if README.in_button((x_pos, y_pos)):
                        readme_event(screen)
                    if REW.in_button((x_pos, y_pos)):
                        EDEN.text = "False"
                        size = rew_event(screen, points, size)
                    if SAVE.in_button((x_pos, y_pos)):
                        save_event(screen, points)
                    if EDEN.in_button((x_pos, y_pos)):
                        pass
                if event.button == 4:
                    if rang > 5:
                        rang -= 5
                        cell_size = WIN_H // rang
                        draw_life(screen, points, cell_size)
                if event.button == 5:
                    if rang < 75:
                        rang += 5
                        cell_size = WIN_H // rang
                        draw_life(screen, points, cell_size)
        pg.display.update()
    pg.quit()


if __name__ == "__main__":
    main()
