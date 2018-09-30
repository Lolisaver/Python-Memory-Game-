import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP
from random import randint

CARD_LENGTH=5
CARD_HEIGHT=5

WIDTH = 90
HEIGHT = 40
MAX_X = WIDTH
MAX_Y = HEIGHT
TIMEOUT = 100
FORM_X = (CARD_LENGTH+1)*13+1
FORM_Y = (CARD_HEIGHT+1)*4+1
OFFSET_X=5
OFFSET_Y=3

CURSOR_OFFSET_X = OFFSET_X+1
CURSOR_OFFSET_Y = OFFSET_Y+1
CURSOR_MAX_X = 13
CURSOR_MAX_Y = 4
CURSOR_MIN_X = 1
CURSOR_MIN_Y = 1

class Form(object):
    def __init__(self, window, char):
        self.timeout = TIMEOUT
        self.window = window
        self.char = char

    def render(self):
        self.window.attron(curses.color_pair(2))
        for row in range(FORM_Y):
            for column in range(FORM_X):
                if row%6==0 or column%6==0:
                    self.window.addstr(OFFSET_Y+row, OFFSET_X+column, self.char)
        self.window.attron(curses.color_pair(3))

class Cursor(object):
    def __init__(self, window):
        self.timeout = TIMEOUT
        self.window = window
        self.x = CURSOR_OFFSET_X
        self.y = CURSOR_OFFSET_Y
        self.position = {
            'y':2,
            'x':4
        }
        self.movementMap = {
            KEY_UP: self.moveUp,
            KEY_DOWN: self.moveDown,
            KEY_LEFT: self.moveLeft,
            KEY_RIGHT: self.moveRight
        }
    def render(self):
        self.window.attron(curses.color_pair(1))
        for row in range(CARD_HEIGHT):
            for column in range(CARD_LENGTH):
                if row%4==0 or column%4==0:
                    self.window.addstr(CURSOR_OFFSET_Y+row+(self.position['y']-1)*(CARD_HEIGHT+1), CURSOR_OFFSET_X+column+(self.position['x']-1)*(CARD_LENGTH+1), "?")
        self.window.attron(curses.color_pair(3))
   
    def move(self, event):
        self.movementMap[event]()
    
    def moveUp(self):
        if self.position['y'] > CURSOR_MIN_Y:
            self.position['y'] -= 1 
    def moveDown(self):
        if self.position['y'] < CURSOR_MAX_Y:
            self.position['y'] += 1
    def moveLeft(self):
        if self.position['x'] > CURSOR_MIN_X:
            self.position['x'] -= 1
    def moveRight(self):
        if self.position['x'] < CURSOR_MAX_X:
            self.position['x'] += 1

    def update(self):
        last_body = self.body_list.pop(0)
        last_body.x = self.body_list[-1].x
        last_body.y = self.body_list[-1].y
        self.body_list.insert(-1, last_body)
        self.last_head_coor = (self.head.x, self.head.y)
        self.direction_map[self.direction]()


if __name__ == '__main__':
    curses.initscr()
    curses.beep()
    curses.beep()

    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_BLACK)
    
    window = curses.newwin(HEIGHT, WIDTH, 0, 0)
    window.timeout(TIMEOUT)
    window.keypad(1)
    curses.noecho()
    curses.curs_set(0)
    window.border(0)

    form = Form(window, '*')
    cursor = Cursor(window)
    
    while True:
        window.clear()
        window.border(0)
        form.render()
        cursor.render()

        event = window.getch()

        if event == 27:
            break

        if event in [KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT]:
            cursor.move(event)

        # if snake.head.x == food.x and snake.head.y == food.y:
        #     snake.eat_food(food)

        # if event == 32:
        #     key = -1
        #     while key != 32:
        #         key = window.getch()

        # snake.update()
        # if snake.collided:
        #     break


    curses.endwin()
