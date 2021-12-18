#Final Assignment
#Alexander Flores
#December 12, 2020

import random
import tkinter as tk


class Connect4(object):
    def __init__(self, width, height, window=None):
        self.width = width
        self.height = height
        self.window = window
        self.data = []

        for row in range(self.height):
            boardRow = []
            for col in range(self.width):
                boardRow += [' ']
            self.data += [boardRow]
#GUI        
        self.bdWidth = 400
        self.bdHeight = 400
        self.padding = 5
        self.footer = 50
        self.diamX = (self.bdWidth/self.width) - self.padding
        self.diamY = (self.bdHeight/self.height) - self.padding
        self.nonAi = 2
        self.line= None

        self.frame = tk.Frame(self.window)
        self.frame.pack()

        self.qButton = tk.Button(self.frame, text='Quit Game', 
                command=self.destroy)
        self.qButton.pack(side='right')

        self.sButton = tk.Button(self.frame, text='New Game',
                command=self.newGame)
        self.sButton.pack(side='right')

        self.scale = tk.Scale(self.frame, orient='horizontal', 
                length=200, from_=0, to=7, command= self.scaleChange)
        self.scale.pack(side='left')

        self.board = tk.Canvas(self.window, width=self.bdWidth + self.padding,
                height=self.bdHeight + self.padding + self.footer,
                background='blue', highlightbackground='black',
                highlightthickness=3)
        self.board.bind('<Button-1>', self.mouse)
        self.board.pack()

        self.circles = []
        self.colors = []
        y = self.padding
        for row in range(self.height):
            circleRow = []
            colorRow = []
            x = self.padding

            for col in range (self.width):
                circleRow += [self.board.create_oval(x, y, 
                    x + self.diamX, y + self.diamY, fill='white')]
                colorRow += ['white']
                x += self.diamX + self.padding

            self.circles += [circleRow]
            self.colors += [colorRow]
            y += self.diamY + self.padding

        self.message = self.board.create_text(self.footer,
                self.bdHeight + self.footer/2,
                text='CLICK A COLUMN TO START!', 
                anchor='w', font='Courier 20')


    def mouse(self,event):
        guiCol = int(event.x / (self.diamX + self.padding))
        guiRow = int(event.y / (self.diamY + self.padding))

        if self.ai != None:
            ox = 'x'
            z = self.guiPlayerMove(guiCol, guiRow, ox)
            self.guiBoard()
            self.window.update()
            
            if z != False:
                self.window.after(600, self.waitMsg())
                self.window.update()
                ox = 'o'
                self.guiPlayerMoveAi(guiCol, guiRow, ox)
                self.window.after(500, self.guiBoard())
        else:
            
            if self.nonAi == 2:
                ox = 'x'
                x = self.guiPlayerMove(guiCol, guiRow, ox)
                if x != False:
                    self.nonAi = 1
                self.guiBoard()
            else:
                ox = 'o'
                x = self.guiPlayerMove(guiCol, guiRow, ox)
                if x != False:
                    self.nonAi = 2
                self.guiBoard()
    
    
    def guiBoard(self): 
        t = self.updateB()
        for row in range(self.height):
            
            for col in range(self.width):
                changeColor = t[row][col]
                self.board.itemconfig(self.circles[row][col], 
                        fill=changeColor)


    def guiPlayerMove(self, col, row, ox):
        if self.allowsMove(col):
            self.addMove(col, ox)
                    
            if self.isFull():
                self.fullMsg()
                return False
                    
            if self.winsFor(ox):
                self.winsForMsg(ox)
                self.guiWinLine()
                return False
                
            self.colChoosenMsg(col, ox)

        else:
            ox = self.oxChange(ox)
            message = 'CHOOSE ANOTHER COL,' + ' ' + str(ox) + '.'
            self.board.itemconfig(self.message, text=message)
            return False
    

    def guiPlayerMoveAi(self, col, row, ox):
        aiMove = int(self.ai.nextMove(self))
        self.addMove(aiMove, ox)
                
        if self.isFull():
            self.fullMsg()
            return
                
        if self.winsFor(ox):
            self.winsForMsg(ox)
            self.guiWinLine()
            return
            
        self.colChoosenMsg(col, ox)
    

    def guiWinLine(self):
        x = (self.diamX+self.padding)
        y = (self.diamY+self.padding)
        if self.winDirection == 'horizontal':
            x1 = (x * self.x1) + 4
            x2 = (x * self.x2) + 3
            y1 = (y * self.y1) + 40
            y2 = (y * self.y1) + 40
            self.line = self.board.create_line(x1, y1, x2, y2, 
                    width=15, fill='yellow')
        
        if self.winDirection == 'vertical':
            x1 = (x * self.x1) + 33
            x2 = (x * self.x1) + 33 
            y1 = (y * self.y1) + 5
            y2 = (y * self.y2) + 1
            self.line = self.board.create_line(x1, y1, x2, y2, 
                    width=15, fill='yellow')

        if self.winDirection == 'diagonalTL':
            x1 = (x * self.x1) + 15
            x2 = (x * self.x2) - 9
            y1 = (y * self.y1) + 10
            y2 = (y * self.y2) - 5
            self.line = self.board.create_line(x1, y1, x2, y2, 
                    width=15, fill='yellow')
        
        if self.winDirection == 'diagonalTR':
            x1 = (x * self.x1)
            x2 = (x * self.x2)
            y1 = (y * self.y1)
            y2 = (y * self.y2)
            self.line = self.board.create_line(x1, y1, x2, y2, 
                    width=15, fill='yellow')


    def colChoosenMsg(self, col, ox):
        ox = self.oxChange(ox)
        if ox == 'BLACK':
            message = "YOU CLICKED COL %d, %s." % (col, ox)
            self.board.itemconfig(self.message, text=message)
        else:
            if self.ai != None:
                message = "AI(%s) PICKED COL %d." % (ox, col)
                self.board.itemconfig(self.message, text=message)
            else:
                message = "YOU CLICKED COL %d, %s." % (col, ox)
                self.board.itemconfig(self.message, text=message)

    
    def fullMsg(self):
        self.board.itemconfig(self.message, text='CATS GAME.')
    
    
    def winsForMsg(self, ox):
        ox = self.oxChange(ox)
        if ox == 'BLACK':
            message = 'BLACK PLAYER WON!'
            self.board.itemconfig(self.message, text=message)
        else:
            if self.ai != None:
                message = 'AI WON, TRY AGAIN?'
                self.board.itemconfig(self.message, text=message)
            
            else:
                message = 'RED PLAYER WON!'
                self.board.itemconfig(self.message, text=message)

    
    def waitMsg(self):
        self.board.itemconfig(self.message, text='WAITING ON AI...')

    
    def oxChange(self, ox):
        if ox == 'x':
            return 'BLACK'
        if ox == 'o':
            return 'RED'

    
    def destroy(self):
        self.window.destroy()


    def newGame(self):
        x = self.clear()
        if self.line != None:
            y = self.board.delete(self.line)
            self.window.after(100, y)
        
        message = 'CLICK A COLUMN TO START!'
        self.board.itemconfig(self.message, text=message)
        self.window.after(100, self.guiBoard())


    def scaleChange(self, num):
        newNum = int(num)
        self.ai = Player('o','Random', newNum)


    def __repr__(self):
        s = ''
        
        for row in range(self.height):
            s += '|'
            for col in range(self.width):
                s += self.data[row][col] + '|'
            s+= '\n'

        s += '--' *self.width + '-\n'
        for col in range (self.width):
            s += ' ' + str(col % 10)
        s += '\n'
        return s
    

    def addMove(self, col, ox):
        if self.allowsMove(col):
            
            for row in range(self.height):
                if self.data[row][col] != ' ':
                    self.data[row - 1][col] = ox
                    return True
            self.data[self.height - 1][col] = ox
            return True
        
        else:
            return False
        
    

    def delMove(self, col):
        for row in range(self.height):
            if self.data[row][col] != ' ':
                self.data[row][col] = ' '
                return 
    

    def allowsMove(self, col):
        if 0 <= col < self.width:
            return self.data[0][col] == ' '
        
        else:
            return False
    

    def clear(self):
        for row in range(self.height):
            
            for col in range(self.width):
                self.data[row][col] = ' '
    
    
    def isFull(self):
        flag = True  
        for row in range(self.height):
            
            for col in range(self.width):
                if self.data[row][col] == ' ':
                    flag = False
                    return flag
        
        return flag
    
    
    def winsFor(self, ox):
        for row in range(0, self.height):
            
            for col in range(0, self.width - 3):
                if self.data[row][col] == ox and \
                self.data[row][col+1] == ox and \
                self.data[row][col+2] == ox and \
                self.data[row][col+3] == ox:
                    self.x1 = col 
                    self.x2 = col+4
                    self.y1 = row
                    self.winDirection = 'horizontal'
                    return True
        
        for row in range(0, self.height - 3):
            
            for col in range(0, self.width):
                if self.data[row][col] == ox and \
                self.data[row+1][col] == ox and \
                self.data[row+2][col] == ox and \
                self.data[row+3][col] == ox:
                    self.x1 = col
                    self.y1 = row
                    self.y2 = row+4
                    self.winDirection = 'vertical'
                    return True
        
        for row in range(0, self.height - 3):
            
            for col in range(0, self.width - 3):
                if self.data[row][col] == ox and \
                self.data[row+1][col+1] == ox and \
                self.data[row+2][col+2] == ox and \
                self.data[row+3][col+3] == ox:
                    self.x1 = col
                    self.x2 = col+4
                    self.y1 = row
                    self.y2 = row+4
                    self.winDirection = 'diagonalTL'
                    return True
        

        for row in range(self.height-3):
            col = self.width - 1
            
            while col > 2:
                if self.data[row][col] == ox and \
                self.data[row+1][col-1] == ox and \
                self.data[row+2][col-2] == ox and \
                self.data[row+3][col-3] == ox:
                    self.x1 = col+1
                    self.x2 = col-3
                    self.y1 = row
                    self.y2 = row+4
                    self.winDirection = 'diagonalTR'
                    return True
                col -= 1
        
        return False
    
    
    def switch(self, ox):
        if ox == 'x':
            return 'o'
            
        else:
            return 'x'
    

    def playGameWith(self, aiPlayer=None):
        ox = 'x'
        counter = self.height * self.width
        turnCount = 0
        
        while counter > 0:
            print(self)
            print('Pick a column '+ str(ox) +':')
            if aiPlayer == None:
                x = int(input())
            else:
                if turnCount % 2 == 0:
                    x = int(input())
                    turnCount += 1
                
                else:
                    x = int(aiPlayer.nextMove(self))
                    print('\n' + str(x) +'\n')
                    turnCount += 1
        
            if self.allowsMove(x):
                self.addMove(x, ox)
                counter -= 1

                if self.isFull():
                    print(self)
                    print('Cats Game\n')
                    return

                if self.winsFor(ox):
                    print(self)
                    print('Winner is: ' + str(ox) + '\n')
                    return
                ox = self.switch(ox)
            
            else:
                print('\nColumn ' + str(x) +' Is An Invalid Column! ' \
                        + 'Try Again Player ' + str(ox) + '!\n')
                turnCount -= 1
    

    def playGui(self, playerClass=None):
        self.ai = playerClass

    def updateB(self):
        guiBoard = []
        for row in range(self.height):
            list1 = []
            for col in range(self.width):
                if self.data[row][col] == 'x':
                    list1 += ['black']
                elif self.data[row][col] == 'o':
                    list1 += ['red']
                else:
                    list1 += ['white']
            guiBoard += [list1]

        return guiBoard
"""
-------------------------------------------------------------------------------
START OF CLASS PLAYER.
"""

class Player:
    def __init__(self, ox, tbt, ply):
        self.ox = ox
        self.tbt = tbt
        self.ply = ply
        self.evenOdd = ''
        self.counter = 0
        self.plyEvenOdd = ''

    def evenOrOdd(self, ply):
        if self.ply % 2 == 0:
            return 'even'
        else:
            return 'odd'
    

    def subNum(self):
        if self.counter > 0:

            x = self.counter
            y = 100 - x
            return y
        
        return 100


    
    def testList(self, b, ox):
        colList = []
        
        for col in range(b.width):

            if b.allowsMove(col):
                b.addMove(col, ox)

                if b.winsFor(ox):
                    
                    if self.evenOdd == self.plyEvenOdd:
                        colList += [self.subNum()]

                    else:
                        colList += [0]
            
                else:
                    b.delMove(col)
                    ox = b.switch(ox)
                    b.addMove(col, ox)
                
                    if b.winsFor(ox):
                        
                        if self.evenOdd == self.plyEvenOdd:
                            colList += [0]
                        
                        else:
                            colList += [self.subNum()]
                
                    else:
                        colList += [50]
                    
                    ox = b.switch(ox)

                b.delMove(col)
            else:
                colList += [-1]
    
        return colList
    
    
    def scoresFor(self, b, ox, ply):
        scores = []
        self.plyEvenOdd = self.evenOrOdd(ply)
        for col in range(b.width):
#condition for lowest ply
            if col == 0:
                self.counter += 1
            
            if  ply < 1:
                p = self.testList(b, ox)
                self.counter -= 1
                return max(p)
#start
            if b.addMove(col, ox) == False:
                scores += [-1]
                continue
            
            if b.winsFor(ox):
                scores += [self.subNum()]

            else:
                b.switch(ox)
                scores += [self.scoresFor(b, ox, ply-1)]
            b.delMove(col)
        
            if col == b.width - 1:
                self.counter -= 1
        
        if self.ply == ply:
            return scores
        return max(scores)
    
    
    def scoreBoard(self, b, ox, num):
#below is for 0 ply
        if num == 0:
            self.plyEvenOdd = self.evenOdd
            L = self.testList(b, ox)
#below is for greater ply
        else:
            L = b 
#below is priority picks then everything else        
        x = max(L)

        if 100 == x:
            return self.checkPos(L, x)
        
        else:
            
            if 0 in L:
                return self.checkPos(L, 0)
            
            return self.checkPos(L, x)
    

    def checkPos(self, L, x):
#tiebreaker
        f = self.bestSpots(L, x)
            
        if self.tbt == 'Left':
            return f[0]
            
        if self.tbt == 'Right':
            return f[-1]
            
        if self.tbt == 'Random':
            return random.choice(f)
    

    def bestSpots(self, scores, x):
#returns the position of the ai move
        newScores = []
        for i in range(len(scores)):
            
            if x == scores[i]:
                newScores.append(i)

        return newScores

    
    def nextMove(self, b):
        
        self.evenOdd = self.evenOrOdd(self.ply)
#checks 0 ply
        if self.ply <= 1:
            return self.scoreBoard(b, self.ox, 0)
        
#start of tree Probability
        x = self.testList(b, self.ox)
        if 100 in x or 0 in x:
            return self.scoreBoard(b, self.ox, 0)
        
        else:
            self.counter = -1
            L = self.scoresFor(b, self.ox, self.ply)
            return self.scoreBoard(L, self.ox, 1)


def main():
    #test = Connect4(7, 6)    
    #test.playGameWith(Player('o','Random', 3))
    
    root = tk.Tk()
    root.title('Connect4')
    c = Connect4(7,6, root)
    p = Player('o','Random', 0)
    c.playGui(p)
    root.mainloop()
if __name__ == '__main__':
    main()
