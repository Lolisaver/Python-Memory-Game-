import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP,KEY_ENTER
from random import randint
from deck import Deck
from timer import timer


CARD_LENGTH=5
CARD_HEIGHT=5

WIDTH = 90  
HEIGHT = 30
MAX_X = WIDTH
MAX_Y = HEIGHT
TIMEOUT = 400
FORM_X = (CARD_LENGTH+1)*13+1
FORM_Y = (CARD_HEIGHT+1)*4+1
OFFSET_X=5
OFFSET_Y=3

CURSOR_OFFSET_X = OFFSET_X+1
CURSOR_OFFSET_Y = OFFSET_Y+1
CURSOR_MAX_X = 12
CURSOR_MAX_Y = 3
CURSOR_MIN_X = 0
CURSOR_MIN_Y = 0

CARDS_OFFSET_X = OFFSET_X+3
CARDS_OFFSET_Y = OFFSET_Y+2

class Form(object):
    def __init__(self, window, char):
        self.timeout = TIMEOUT
        self.window = window
        self.char = char

    def render(self):
        self.window.attron(curses.color_pair(3))
        for row in range(FORM_Y):
            for column in range(FORM_X):
                if row%6==0 or column%6==0:
                    self.window.addstr(OFFSET_Y+row, OFFSET_X+column, self.char)
        # self.window.attron(curses.color_pair(1))

class Cards(object):
    def __init__(self, window, cards):
        self.timeout = TIMEOUT
        self.window = window
        self.cards = cards
        self.visiable = [[1]*13,[1]*13,[1]*13,[1]*13]

    def render(self):
        self.window.attron(curses.color_pair(4))
        for y, row in enumerate(self.cards):
            for x, card in enumerate(row):
                if self.visiable[y][x] == 1:
                    self.window.addstr(CARDS_OFFSET_Y+y*(CARD_HEIGHT+1), CARDS_OFFSET_X+x*(CARD_LENGTH+1), card['suit'])
                    self.window.addstr(CARDS_OFFSET_Y+y*(CARD_HEIGHT+1)+1, CARDS_OFFSET_X+x*(CARD_LENGTH+1), card['rank'])
        # self.window.attron(curses.color_pair(1))
    
    def openCard(self,y,x):
        self.visiable[y][x]=1
    def coverCard(self,y,x):
        self.visiable[y][x]=0

    def coverAllCards(self):
        self.visiable = [[0]*13,[0]*13,[0]*13,[0]*13]
        
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
        self.window.attron(curses.color_pair(2))
        for row in range(CARD_HEIGHT):
            for column in range(CARD_LENGTH):
                if row%4==0 or column%4==0:
                    self.window.addstr(CURSOR_OFFSET_Y+row+(self.position['y'])*(CARD_HEIGHT+1), CURSOR_OFFSET_X+column+(self.position['x'])*(CARD_LENGTH+1), "*")
        # self.window.attron(curses.color_pair(1))
   
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
    def getPostion(self):
        return self.position

if __name__ == '__main__':

    deck = Deck()
    counter = 0
    openedCardsNum=[]
    memoryCards=[[],[],[],[]]
    for id, card in enumerate(deck.cards):
        memoryCards[id//13].append(card)

    curses.initscr()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)

    window = curses.newwin(HEIGHT, WIDTH, 0, 0)
    window.timeout(TIMEOUT)
    window.keypad(1)
    curses.noecho()
    curses.curs_set(0)
    window.border(0)

    form = Form(window, '*')
    cursor = Cursor(window)
    cards = Cards(window,memoryCards)
    timer = timer()

    openedCards = []

    while True:
        gameTime = int(timer.getTime())
        position = cursor.getPostion()
        window.clear()
        window.border(0)
        form.render()
        cursor.render()
        cards.render()

        window.addstr(1, 5, 'Time : {}'.format(gameTime))
        window.addstr(2, 5, 'Position : {x},{y}'.format(x=position['x'],y=position['y']))
        # window.addstr(3, 5, 'Chose cards : {}'.format(openedCards))

        key = window.getch()

        #game 
        if gameTime == 2:
            cards.coverAllCards()

        if len(openedCards) >= 2:
            card1 = openedCards.pop()
            card2 = openedCards.pop()
            if card1['rank'] != card2['rank']:
                cards.coverCard(card1['y'],card1['x'])
                cards.coverCard(card2['y'],card2['x'])

        #event
        if key == KEY_ENTER or key == 10 or key == 13: #enter
            cards.openCard(position['y'],position['x'])

            openedCards.append({
                'y':position['y'],
                'x':position['x'],
                'rank':memoryCards[position['y']][position['x']]['rank']
                })
            if len(openedCards) >1:
                if openedCards[0]['x'] == position['x'] and openedCards[0]['y'] == position['y']:
                    openedCards.pop()
        if key == 32:
            cards.coverCard(position['y'],position['x'])

        if key == 27: #esc
            break

        if key in [KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT]:
            cursor.move(key)

    curses.endwin()
