import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP,KEY_ENTER
from deck import Deck
from timer import Timer


CARD_LENGTH=5
CARD_HEIGHT=5

WIDTH = 90  
HEIGHT = 35
TIMEOUT = 500
FORM_X = (CARD_LENGTH+1)*13+1
FORM_Y = (CARD_HEIGHT+1)*4+1
OFFSET_X=5
OFFSET_Y=7

CURSOR_OFFSET_X = OFFSET_X+1
CURSOR_OFFSET_Y = OFFSET_Y+1
CURSOR_MAX_X = 12
CURSOR_MAX_Y = 3
CURSOR_MIN_X = 0
CURSOR_MIN_Y = 0

CARDS_OFFSET_X = OFFSET_X+3
CARDS_OFFSET_Y = OFFSET_Y+2

BROWSE_SECONDS = 5
GAMETIME = 30

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

class Cards(object):
    def __init__(self, window, cards):
        self.timeout = TIMEOUT
        self.window = window
        self.cards = cards
        self.opened = [[0]*13,[0]*13,[0]*13,[0]*13]

    def render(self):
        self.window.attron(curses.color_pair(4))
        for y, row in enumerate(self.cards):
            for x, card in enumerate(row):
                if self.opened[y][x] == 1:
                    self.window.addstr(CARDS_OFFSET_Y+y*(CARD_HEIGHT+1), CARDS_OFFSET_X+x*(CARD_LENGTH+1), card['suit'])
                    self.window.addstr(CARDS_OFFSET_Y+y*(CARD_HEIGHT+1)+1, CARDS_OFFSET_X+x*(CARD_LENGTH+1), card['rank'])
    
    def openCard(self,y,x):
        self.opened[y][x] = 1
    def coverCard(self,y,x):
        self.opened[y][x] = 0
    def coverAllCards(self):
        self.opened = [[0]*13,[0]*13,[0]*13,[0]*13]
    def openAllCards(self):
        self.opened = [[1]*13,[1]*13,[1]*13,[1]*13]
    
    def getOpened(self):
        return self.opened
        
class Cursor(object):
    def __init__(self, window):
        self.timeout = TIMEOUT
        self.window = window
        self.x = CURSOR_OFFSET_X
        self.y = CURSOR_OFFSET_Y
        self.position = {
            'y':0,
            'x':0
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
                if row % 4 == 0 or column % 4 == 0:
                    self.window.addstr(CURSOR_OFFSET_Y + row +(self.position['y'])*(CARD_HEIGHT+1), CURSOR_OFFSET_X+column+(self.position['x'])*(CARD_LENGTH+1), "*")
   
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

    def setPostion(self,y,x):
        if y >= 0 and y < 4 and x >= 0 and x < 13: 
            self.position['y'] = y
            self.position['x'] = x

class Memory():
    def __init__(self): 
        
        curses.initscr()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
        
        self.window = curses.newwin(HEIGHT, WIDTH, 0, 0)
        self.window.timeout(TIMEOUT)
        self.window.keypad(1)
        curses.noecho()
        curses.curs_set(0)
        self.window.border(0)
        self.timer = Timer()
        self.deck = Deck()

    def run(self):
        
        sortedDeck = self.getsortedDeck()
        foundNum = 0
        record = 0
        pendingCheckedCards=[]
        status = 'end'

        form = Form(self.window, '*')
        cursor = Cursor(self.window)
        cards = Cards(self.window, sortedDeck)

        gameTime = BROWSE_SECONDS
        self.timer.reset()

        while True:
            position = cursor.getPostion()

            self.window.clear()
            self.window.border(0)
            form.render()
            cursor.render()
            cards.render()

            self.window.addstr(2, 5, 'Operations Introduction : ESC = QUIT, S = START, ENTER = OPEN ')
            self.window.addstr(3, 5, 'Best Recond : {}'.format(record))
            self.window.addstr(4, 5, 'Time : {}'.format(gameTime))
            self.window.addstr(5, 5, 'Found Cards : {}'.format(foundNum))

            key = self.window.getch()

            if status == 'end':
                if key == 115: 
                    status = 'before'
                    gameTime = BROWSE_SECONDS
                    self.timer.reset()
                    foundNum = 0
                    sortedDeck = self.getsortedDeck()
                    cards = Cards(self.window, sortedDeck)
                    cards.openAllCards()
                    cursor.setPostion(0,0)
            if status == 'before':
                if gameTime < 1:
                    status = 'start'
                    cards.coverAllCards()
                    gameTime = GAMETIME
                    self.timer.reset()
                else:
                    gameTime = BROWSE_SECONDS - int(self.timer.get())
            elif status == 'start':
                if gameTime < 1:
                    if foundNum > record:
                        record = foundNum
                    status = 'end'
                else:
                    gameTime = GAMETIME- int(self.timer.get())
                    if len(pendingCheckedCards) >= 2:
                        card1 = pendingCheckedCards.pop()
                        card2 = pendingCheckedCards.pop()
                        if card1['rank'] != card2['rank']:
                            cards.coverCard(card1['y'],card1['x'])
                            cards.coverCard(card2['y'],card2['x'])
                        else:
                            foundNum += 2
                    if key == KEY_ENTER or key == 10 or key == 13: 
                        openedCards = cards.getOpened()
                        if openedCards[position['y']][position['x']] == 0:
                            cards.openCard(position['y'],position['x'])
                            pendingCheckedCards.append({
                                'y':position['y'],
                                'x':position['x'],
                                'rank':sortedDeck[position['y']][position['x']]['rank']
                                })
                        
                    if key == 32:
                        cards.coverCard(position['y'],position['x'])

                    if key in [KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT]:
                        cursor.move(key)
            
            if key == 27: 
                break

        curses.endwin()

    def getsortedDeck(self):
        self.deck.reshuffle()
        cards=[[],[],[],[]]
        for id, card in enumerate(self.deck.cards):
            cards[id // 13].append(card)
        return cards
    
if __name__ == '__main__':
    game = Memory()
    game.run()