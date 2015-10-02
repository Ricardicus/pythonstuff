# This is a Snake game in multiplayer!
# Runs on a Python2.x interpreter with the Tkinter library installed

# -*- coding: UTF-8 -*- 
import random
from Tkinter import *

def mousePressed(event):
    # Mouse event handler
    canvas = event.widget.canvas
    redrawAll(canvas)

def keyPressed(event):
    # Key event handler!
    canvas = event.widget.canvas
    canvas.data["ignoreNextTimerEvent"] = True # for better timing
    # first process keys that work even if the game is over
    if (event.char == "q"):
        gameOver(canvas)
    elif (event.char == "r"):
        init(canvas)
    elif (event.char == "p"):
        canvas.data["inDebugMode"] = not canvas.data["inDebugMode"]
    # now process keys that only work if the game is not over
    if (canvas.data["isGameOver"] == False):
        if (event.keysym == "Up"):
            if(canvas.data["snake1Drow"] != 1):
                moveSnake1(canvas, -1, 0)
        elif (event.keysym == "Down"):
            if(canvas.data["snake1Drow"] != -1):
                moveSnake1(canvas, +1, 0)
        elif (event.keysym == "Left"):
        	if(canvas.data["snake1Dcol"] != 1):
           		moveSnake1(canvas, 0,-1)
        elif (event.keysym == "Right"):
        	if(canvas.data["snake1Dcol"] != -1):
        		moveSnake1(canvas, 0,+1)
        elif (event.char == "w"):
            if(canvas.data["snake2Drow"] != 1):
           		moveSnake2(canvas, -1, 0)
        elif (event.char == "s"):
        	if(canvas.data["snake2Drow"] != -1):
        		moveSnake2(canvas, +1, 0)
        elif (event.char == "a"):
        	if(canvas.data["snake2Dcol"] != 1):
        		moveSnake2(canvas, 0,-1)
        elif (event.char == "d"):
        	if(canvas.data["snake2Dcol"] != -1):
        			moveSnake2(canvas, 0,+1)
    redrawAll(canvas)

def moveSnake1(canvas, drow, dcol):
    # Moving the snake drow nbr of rows and dcol nbr of cols in the matrix stored in canvas. 
    # canvas is storing position information
    canvas.data["snake1Drow"] = drow # storing direction for the next timer event
    canvas.data["snake1Dcol"] = dcol
    snakeBoard = canvas.data["snakeBoard"]
    rows = len(snakeBoard)
    cols = len(snakeBoard[0])
    headRow = canvas.data["headRow1"]
    headCol = canvas.data["headCol1"]
    newHeadRow = headRow + drow
    newHeadCol = headCol + dcol
    newHeadCol = newHeadCol % cols
    newHeadRow = newHeadRow % rows
    if (((snakeBoard[newHeadRow][newHeadCol] > 0) and (snakeBoard[newHeadRow][newHeadCol] < 100)) or (snakeBoard[newHeadRow][newHeadCol] > 100)):
        # This means that the snake ran into something!
        gameOver(canvas,1 )
    elif(snakeBoard[newHeadRow][newHeadCol] < 0):
        # Snake eating food!
        snakeBoard[newHeadRow][newHeadCol] = 1 + snakeBoard[headRow][headCol]
        canvas.data["headRow1"] = newHeadRow
        canvas.data["headCol1"] = newHeadCol
        canvas.data["points1"] += 1
        placeFood(canvas)
    else:
        # Normal forward move
        snakeBoard[newHeadRow][newHeadCol] = 1 + snakeBoard[headRow][headCol]
        canvas.data["headRow1"] = newHeadRow
        canvas.data["headCol1"] = newHeadCol
        removeTail1(canvas)


def moveSnake2(canvas, drow, dcol):
    # Moving the second snake drow nbr of rows and dcol nbr of column in the matrix stored in canvas.
    # The canvas stores positioning information
    canvas.data["snake2Drow"] = drow # storing the direction for the next timer event
    canvas.data["snake2Dcol"] = dcol
    snakeBoard = canvas.data["snakeBoard"]
    rows = len(snakeBoard)
    cols = len(snakeBoard[0])
    headRow = canvas.data["headRow2"]
    headCol = canvas.data["headCol2"]
    newHeadRow = headRow + drow
    newHeadCol = headCol + dcol
    newHeadCol = newHeadCol % cols
    newHeadRow = newHeadRow % rows
    if (((snakeBoard[newHeadRow][newHeadCol] > 0) and (snakeBoard[newHeadRow][newHeadCol] < 100)) or (snakeBoard[newHeadRow][newHeadCol] > 100)):
        # Snake ran into someone!
        gameOver(canvas,2)
    elif (snakeBoard[newHeadRow][newHeadCol] < 0):
        # Snake ate food!
        snakeBoard[newHeadRow][newHeadCol] = 1 + snakeBoard[headRow][headCol]
        canvas.data["headRow2"] = newHeadRow
        canvas.data["headCol2"] = newHeadCol
        canvas.data["points2"] += 1
        placeFood(canvas)
    else:
        # Normal move forward
        snakeBoard[newHeadRow][newHeadCol] = 1 + snakeBoard[headRow][headCol]
        canvas.data["headRow2"] = newHeadRow
        canvas.data["headCol2"] = newHeadCol
        removeTail2(canvas)

def removeTail2(canvas):
    # Finding every snake2-cell and substracting one from it. 
    # This is crucial in making tail, the end, of the snake move! 
    snakeBoard = canvas.data["snakeBoard"]
    rows = len(snakeBoard)
    cols = len(snakeBoard[0])
    for row in range(rows):
        for col in range(cols):
            if (snakeBoard[row][col] > 100):
                snakeBoard[row][col] -= 1


def removeTail1(canvas):
    # Finding every snake1-cell and substracting one from it. 
    # This is crucial in making tail, the end, of the snake move! 
    snakeBoard = canvas.data["snakeBoard"]
    rows = len(snakeBoard)
    cols = len(snakeBoard[0])
    for row in range(rows):
        for col in range(cols):
            if ((snakeBoard[row][col] > 0) and (snakeBoard[row][col] < 100)):
                snakeBoard[row][col] -= 1

def gameOver(canvas,who):
    # The game is over!
    canvas.data["isGameOver"] = True
    canvas.data["whodied"] = who

def timerFired(canvas):
    # The game loop event trigger!
    ignoreThisTimerEvent = canvas.data["ignoreNextTimerEvent"]
    canvas.data["ignoreNextTimerEvent"] = False
    if ((canvas.data["isGameOver"] == False) and
        (ignoreThisTimerEvent == False)):
        # Will only process if the game is not over
        drow = canvas.data["snake1Drow"]
        dcol = canvas.data["snake1Dcol"]
        moveSnake1(canvas, drow, dcol)
        drow = canvas.data["snake2Drow"]
        dcol = canvas.data["snake2Dcol"]
        moveSnake2(canvas, drow, dcol)
        redrawAll(canvas)
    # Call if the game is not over!
    delay = 120 # milliseconds
    canvas.after(delay, timerFired, canvas) # The main game-loop!

def redrawAll(canvas):
    # Drawing everything again! Called by the game loop after snakes have been moved.
    canvas.delete(ALL)
    tx = canvas.data["canvasWidth"]-100
    ty = canvas.data["canvasHeight"] - 100
    canvas.create_rectangle(tx-80,ty+10,tx+80,ty+20, fill="black")
    canvas.create_text(tx,ty, text ="Poäng turkos: "+str(canvas.data["points1"]), font=("Rockwell",24,"bold"))
    tx = tx/4 - 40
    canvas.create_rectangle(tx-70,ty+10,tx+50,ty+20, fill="black")
    canvas.create_text(tx,ty, text ="Poäng röd: "+str(canvas.data["points2"]), font=("Rockwell",24,"bold"))
    drawSnakeBoard(canvas)
    if (canvas.data["isGameOver"] == True):
        who = canvas.data["whodied"]
        cx = canvas.data["canvasWidth"]/2
        cy = canvas.data["canvasHeight"]/2
        if(canvas.data["points1"] > canvas.data["points2"]):
            canvas.create_text(cx, cy, text="Vinnare är spelare cyan!", font=("Rockwell", 32, "bold"))
        elif(canvas.data["points1"] == canvas.data["points2"]):
            canvas.create_text(cx, cy, text="Det blev lika!", font=("Rockwell", 32, "bold"))
        else:
            canvas.create_text(cx, cy, text="Vinnare är spelare röd!", font=("Rockwell", 32, "bold"))

def drawSnakeBoard(canvas):
    # the call for drawing the snakeboard onto the screen!
    snakeBoard = canvas.data["snakeBoard"]
    rows = len(snakeBoard)
    cols = len(snakeBoard[0])
    for row in range(rows):
        for col in range(cols):
            drawSnakeCell(canvas, snakeBoard, row, col)

def drawSnakeCell(canvas, snakeBoard, row, col):
    # Drawing cells onto the snakeboard on the screen. 
    # The content of the snakeboard matrix determines the color drawed.
    margin = canvas.data["margin"]
    cellSize = canvas.data["cellSize"]
    left = margin + col * cellSize
    right = left + cellSize
    top = margin + row * cellSize
    bottom = top + cellSize
#    canvas.create_rectangle(left, top, right, bottom, fill="white")
    if ((snakeBoard[row][col] > 0) and (snakeBoard[row][col] < 50)):
        # draw part of the "cyan" colored snake
        canvas.create_oval(left, top, right, bottom, fill="cyan")
    elif(snakeBoard[row][col] > 100):
        canvas.create_oval(left,top,right,bottom,fill="red")
    elif (snakeBoard[row][col] < 0):
        # drawing food item
        canvas.create_oval(left, top, right, bottom, fill="green")
    # used when debugging.. draws the number in the current cell of the snakeboard.
    if (canvas.data["inDebugMode"] == True):
        canvas.create_text(left+cellSize/2,top+cellSize/2,
                           text=str(snakeBoard[row][col]),font=("Helvetica", 14, "bold"))

def loadSnakeBoard(canvas):
    rows = canvas.data["rows"]
    cols = canvas.data["cols"]
    snakeBoard = [ ]
    for row in range(rows): snakeBoard += [[0] * cols]
    snakeBoard[rows/2][cols/2] = 1
    snakeBoard[rows/2+2][cols/2-1] = 101
    canvas.data["snakeBoard"] = snakeBoard
    findSnakeHead(canvas)
    placeFood(canvas)

def placeFood(canvas):
    # Placing a food item, represented by -1, onto the snakeboard. 
    snakeBoard = canvas.data["snakeBoard"]
    rows = len(snakeBoard)
    cols = len(snakeBoard[0])
    while True:
        row = random.randint(0,rows-1)
        col = random.randint(0,cols-1)
        if (snakeBoard[row][col] == 0):
            break
    snakeBoard[row][col] = -1

def findSnakeHead(canvas):
    # finding where to find the head of snake1 and snake2 respectively and 
    # storing them in the data dictionary contained in canvas.
    snakeBoard = canvas.data["snakeBoard"]
    rows = len(snakeBoard)
    cols = len(snakeBoard[0])
    headRow1 = 0
    headCol1 = 0
    headRow2 = 0
    headCol2 = 0
    for row in range(rows):
        for col in range(cols):
            if (snakeBoard[row][col] == 1):
                headRow1 = row
                headCol1 = col
            elif(snakeBoard[row][col] == 101):
                headRow2 = row
                headCol2 = col
    canvas.data["headRow1"] = headRow1
    canvas.data["headCol1"] = headCol1
    canvas.data["headRow2"] = headRow2
    canvas.data["headCol2"] = headCol2

def printInstructions():
    # Printing some instructions!
    print "Ha det så kul! Tryck 'r' för att restarta spelet."

def init(canvas):
    # Initialising the game!
    printInstructions()
    loadSnakeBoard(canvas)
    canvas.data["inDebugMode"] = False
    canvas.data["isGameOver"] = False
    canvas.data["snake1Drow"] = 0
    canvas.data["snake1Dcol"] = -1 # start moving left
    canvas.data["snake2Drow"] = 0
    canvas.data["snake2Dcol"] = 1
    canvas.data["ignoreNextTimerEvent"] = False
    redrawAll(canvas)

def run(rows, cols):
    # Creates the root and the canvas!
    root = Tk()
    margin = 3
    cellSize = 15
    canvasWidth = 2*margin + cols*cellSize
    canvasHeight = 2*margin + rows*cellSize
    canvas = Canvas(root, width=canvasWidth, height=canvasHeight)
    canvas.pack()
    root.resizable(width=0, height=0)
    # Stores canvas in root and in itself for callbacks. (Not original idea.. found help online)
    root.canvas = canvas.canvas = canvas
    # Setting up the canvas and the dictionary containg data of the game in canvas.
    canvas.data = { }
    canvas.data["margin"] = margin
    canvas.data["cellSize"] = cellSize
    canvas.data["canvasWidth"] = canvasWidth
    canvas.data["canvasHeight"] = canvasHeight
    canvas.data["rows"] = rows
    canvas.data["cols"] = cols
    canvas.data["points1"] = 0
    canvas.data["points2"] = 0
    init(canvas)
    # set up events
    root.bind("<Button-1>", mousePressed)
    root.bind("<Key>", keyPressed)
    timerFired(canvas)
    # and launch the app
    root.mainloop()  

if __name__=="__main__":
    run(50,50)
