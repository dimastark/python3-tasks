"""GIU for 'Colorize the map'"""
import pygame as pg
import itertools as it
from geometry import Point, painting_graph, brute_graph
from extras import checks, connect_countries, make_country
from generator import generate_pie, generate_tree, generate_setted
import sys
import os


WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
SIZE = 10


def create_parser():
    """Create parser of arguments

    Return ArgumentParser
    """
    from argparse import ArgumentParser, FileType

    parser = ArgumentParser(prog='4color',
                            description='Colorize the map in minimum colors',
                            epilog='(c) DimaStark 2015')
    parser.add_argument('-f', '--file', type=FileType(),
                        help='Name of file, where located the graph')
    parser.add_argument('-b', '--brute', action='store_const',
                        const=brute_graph,
                        default=painting_graph,
                        help='Algorithm of colorizing')
    parser.add_argument('-g', '--generate',
                        choices=['pie', 'tree', 'setted'],
                        help='Generate some struct to show in this program')
    return parser


def draw_readme(screen):
    """Draw readme text on screen

    Arguments:
        screen(int, int) - pygame screen
    """
    start = WINDOW_HEIGHT // 10
    linesize = WINDOW_WIDTH // 35
    y_pos = 3 * linesize
    draw_text(screen, (start, start - linesize), linesize, "THIS IS README")
    with open("readme.txt", encoding='utf-8') as file:
        for line in file:
            y_pos += linesize
            draw_text(screen, (start, y_pos), linesize, line[:-1])


def readme_event(screen):
    """Draw readme on screen

    Arguments:
        screen(int, int) - pygame screen
    """
    coords = (WINDOW_WIDTH // 2, WINDOW_HEIGHT + 10)
    size = (WINDOW_WIDTH // 4, 30)
    back = Button(coords, size, "Back")
    readme_loop = True
    while readme_loop:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if back.in_button(pg.mouse.get_pos()):
                    readme_loop = False
        screen.fill(Color.WHITE)
        draw_readme(screen)
        back.draw_button(screen)
        pg.display.update()


def draw_text(screen, coords, size, text):
    """Draws the specified text at the specified coordinates

    Arguments:
      screen(int, int): the display, where need draw
      text(str): text for drawing
      coords(int, int): coordinates x and y on screen
      size(int, int): the size of text

    Note: The text is black
    """
    font_style = pg.font.SysFont("Arial", size)
    font_image = font_style.render(text, 0, Color.BLACK)
    screen.blit(font_image, coords)


class Button:
    """Button class for pygame

    Parameters:
        coord(int, int) - x an y coordinates
        size(int, int) - size of button
        text(str) - button text
    """

    def __init__(self, coord, size, text):
        """Make button

        Arguments:
            coord(int, int) - x an y coordinates
            size(int, int) - size of button
            text(str) - button text
        """
        self.coord = coord
        self.size = size
        self.text = text

    def draw_button(self, screen):
        """Draw a button

        Args:
            screen(int, int): the display, where need draw
        """
        coords = self.coord[0] + 2, self.coord[1] + 2
        mouse = pg.mouse.get_pos()
        if self.in_button(mouse):
            pg.draw.rect(screen, Color.BLACK, self.coord + self.size, 2)
            draw_text(screen, coords, self.size[1] - 5, self.text)
        else:
            draw_text(screen, coords, self.size[1] - 15, self.text)

    def in_button(self, coord):
        """Return True if "coord" in button

        Arguments:
            coord(int, int) - x and y coordinates
        """
        in_x = self.coord[0] + self.size[0] > coord[0] > self.coord[0]
        in_y = self.coord[1] + self.size[1] > coord[1] > self.coord[1]
        return in_x and in_y


class Color:
    """Static class of colors"""
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    VIOLET = (255, 0, 255)
    GREY = (127, 127, 127)
    PINK = (241, 156, 187)
    AZURE = (0, 127, 255)

    @staticmethod
    def get_color_name_from_num(num):
        """Return color name according in order

        Arguments:
            num(int) - place in list of colors

        Return (str)
        """
        if num < 10:
            return ['WHITE', 'RED',
                    'YELLOW', 'GREEN',
                    'BLUE', 'VIOLET',
                    'GREY', 'PINK',
                    'AZURE', 'BLACK'][num]
        return str(num)

    @staticmethod
    def get_color_from_num(num):
        """Return color according in order

        Arguments:
            num(int) - place in list of colors

        Return (Color)
        """
        return eval("Color." + Color.get_color_name_from_num(num))

    @staticmethod
    def get_color(name):
        """Return color by name

        Arguments:
            name(str) - color name

        Return (Color)
        """
        return eval("Color." + name.toupper())


def draw_points(screen, points, color=Color.BLACK):
    """Draw 'Points' from points with 'color' color

    Arguments:
        screen(int, int) - pygame screen
        points(list (point) - points to draw
        color (int, int, int) - color in rgb format
        color is BLACK by default
    """
    width = 1
    if color != Color.BLACK:
        width = 0
    if len(points) > 1:
        polygon = []
        for point in points:
            center = (point.x * SIZE + SIZE // 2, point.y * SIZE + SIZE // 2)
            pg.draw.circle(screen, Color.BLACK, center, SIZE // 2, 1)
            polygon.append((point.x * SIZE + SIZE // 2, point.y * SIZE + SIZE // 2))
        pg.draw.polygon(screen, color, polygon, width)


def left_mouse_event(points):
    """Event, when click left button of mouse

    Arguments:
        points(list<Point>) - country points
    """
    x_pos, y_pos = pg.mouse.get_pos()
    x_s = int(x_pos // SIZE)
    y_s = int(y_pos // SIZE)
    point = Point(x_s, y_s)
    if WINDOW_WIDTH > x_pos and WINDOW_HEIGHT > y_pos:
        if point not in points:
            points.append(point)


def draw_colors(screen, countries, colors):
    """Draw countries with color

    Arguments:
        screen(int, int) - pygame screen
        countries(list<list<Sector>>) - all countries
        colors(list<(int, int, int)>) - correct colors to colorize
    """
    for counter in range(len(countries)):
        points = list(it.chain(*[i.points() for i in countries[counter]]))
        color = Color.get_color_from_num(colors[str(counter + 1)] + 1)
        draw_points(screen, points, color=color)


def colorizing_event(screen, countries, algorithm):
    """Painting countries event

    Arguments:
        countries(list<list<Sector>>) - all countries
        algorithm (func) - colorizing algorithm
    """
    back = Button((100, WINDOW_HEIGHT + 10), (150, 30), "Back")
    col_loop = True
    graph = connect_countries(countries)
    answ = algorithm(graph)
    while col_loop:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if back.in_button(pg.mouse.get_pos()):
                    col_loop = False
        screen.fill(Color.WHITE)
        back.draw_button(screen)
        draw_colors(screen, countries, answ)
        pg.display.update()


def making_event(screen, countries, points):
    """Making polygon event

    Arguments:
        screen (int, int) - pygame screen
        countries (list<list<Sector>>) - all countries
        points (list<Point>) - points to make polygon

    Return points and changed countries
    """
    make_loop = True
    while make_loop:
        screen.fill(Color.WHITE)
        MAKE_P.draw_button(screen)
        for counter in range(len(countries)):
            for sec in countries[counter]:
                draw_points(screen, [sec.start, sec.end])
        draw_points(screen, points)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                left_mouse_event(points)
                if pg.mouse.get_pressed()[0]:
                    x_pos, y_pos = pg.mouse.get_pos()
                    if MAKE_P.in_button((x_pos, y_pos)):
                        make_loop = False
                        countr = make_country(points)
                        if countr:
                            countries.append(countr)
                        if checks(countries):
                            countries = countries[:-1]
                        points = []
        pg.display.update()
    return points, countries


def parse_graph(content):
    """Parse graph from string

    Arguments:
        content(str) - string to parse

    Return graph
    """
    graph = {}
    lines = content[:content.rindex(',')].split('\n')
    for line in lines:
        key, values = line.split(':')
        value = [x for x in values.split(',') if x != '']
        if key in value:
            raise ValueError("Wrong graph format")
        graph[key] = value
    return graph


def console_work(namespace):
    """Batch mode

    Arguments:
        namespace(namespace) - arguments of command line
    """
    import pprint
    content = parse_graph(namespace.file.read())
    answer = namespace.brute(content)
    pprint.pprint(content)
    for num in range(1, len(answer) + 1):
        color_name = Color.get_color_name_from_num(answer[str(num)])
        print(str(num) + ': ' + color_name)


def save_event(graph):
    """Saving current 'graph' to file"""
    name = "save"
    counter = 0
    content = ""
    for key in graph:
        content += key + ":"
        if len(graph[key]) > 0:
            for item in graph[key]:
                content += str(item) + ','
        else:
            content += ','
        content += '\n'
    while os.path.exists(name + str(counter) + ".txt"):
        counter += 1
    try:
        with open(name + str(counter - 1) + ".txt", "r") as file:
            prev_cont = file.read()
    except FileNotFoundError:
        prev_cont = ''
    if prev_cont != content:
        with open(name + str(counter) + ".txt", "w") as file:
            file.write(content)



def on_mouse_button_down(screen, points, countries):
    """Mouse button down event

    Arguments:
        screen(int, int) - pygame screen
        points(list<Point>) - points to draw
        countries(list<list<Sector>>) - all counties

    Return changes
    """
    if pg.mouse.get_pressed()[0]:
        x_pos, y_pos = pg.mouse.get_pos()
        if BACK.in_button((x_pos, y_pos)):
            if countries:
                countries = countries[:-1]
        if README.in_button((x_pos, y_pos)):
            readme_event(screen)
        if SAVE.in_button((x_pos, y_pos)):
            if len(countries) > 0:
                save_event(connect_countries(countries))
        if START.in_button((x_pos, y_pos)):
            colorizing_event(screen, countries, painting_graph)
        if BRUTE.in_button((x_pos, y_pos)):
            colorizing_event(screen, countries, brute_graph)
        if MAKE_P.in_button((x_pos, y_pos)):
            points, countries = making_event(screen, countries, points)
    return points, countries


def on_key_down(key, countries):
    """Mouse button down event

    Arguments:
        key(str) - event.key
        countries(list<list<Sector>>) - all counties

    Return changes
    """
    mods = pg.key.get_mods()
    if mods & pg.KMOD_CTRL:
        if key == pg.K_s:
            save_event(connect_countries(countries))
        elif key == pg.K_z:
            countries = countries[:-1]
    return countries


def choose_action(choice):
    """Make work if choose generated struct"""
    com = {'pie': (generate_pie, [4, 51]), 'tree': (generate_tree, [0, 7]),
           'setted': (generate_setted, [4, 11])}
    action, bords = com[choice]
    while True:
        str_bords = str(bords[0]) + " < param < " + str(bords[1]) + ": "
        param = int(input("Input parameter in " + str_bords))
        if bords[0] < param < bords[1]:
            break
        else:
            print("Wrong parameters")
    return action(param)


BRUTE = Button((WINDOW_HEIGHT - 100, WINDOW_HEIGHT + 10), (90, 30), "Brute")
START = Button((WINDOW_HEIGHT - 200, WINDOW_HEIGHT + 10), (90, 30), "Colorize")
MAKE_P = Button((WINDOW_HEIGHT - 300, WINDOW_HEIGHT + 10), (90, 30), "Make")
BACK = Button((WINDOW_HEIGHT - 400, WINDOW_HEIGHT + 10), (90, 30), "Undo")
SAVE = Button((WINDOW_HEIGHT - 500, WINDOW_HEIGHT + 10), (90, 30), "Save")
README = Button((WINDOW_HEIGHT - 600, WINDOW_HEIGHT + 10), (90, 30), "Readme")
BUTTONS = [BRUTE, START, MAKE_P, BACK, README, SAVE]


def main():
    """Main entry for application"""
    parser = create_parser()
    namespace = parser.parse_args()
    if not namespace.file:
        countries = []
        if namespace.generate:
            countries = choose_action(namespace.generate)
        points = []
        loop = True
        screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT + 50), pg.DOUBLEBUF)
        pg.display.set_caption("Map")
        pg.init()
        while loop:
            screen.fill(Color.WHITE)
            for counter in range(len(countries)):
                for sec in countries[counter]:
                    draw_points(screen, [sec.start, sec.end])
            draw_points(screen, points)
            for button in BUTTONS:
                button.draw_button(screen)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    loop = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    points, countries = on_mouse_button_down(screen, points, countries)
                if event.type == pg.KEYDOWN:
                    countries = on_key_down(event.key, countries)
            pg.display.update()
        pg.quit()
    else:
        console_work(namespace)


if __name__ == "__main__":
    main()
