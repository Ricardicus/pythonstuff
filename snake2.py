# -*- coding: UTF-8 -*- 
import random
from Tkinter import *

#Mouse event handling
def mousePressed(event):
    canvas = event.widget.canvas
    redrawAll(canvas)

#Key event handling
def keyPressed(event):
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
    # Changing the snake1's location drow number of rows and dcol number of columns in the matrix
    # store direction for the next timer event
    canvas.data["snake1Drow"] = drow
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
        # snake ran into someone!
        gameOver(canvas,1 )
    elif(snakeBoard[newHeadRow][newHeadCol] < 0):
        # sanke are food. 
        snakeBoard[newHeadRow][newHeadCol] = 1 + snakeBoard[headRow][headCol]
        canvas.data["headRow1"] = newHeadRow
        canvas.data["headCol1"] = newHeadCol
        canvas.data["points1"] += 1
        placeFood(canvas)
    else:
        # normal move forward (not eating food)
        snakeBoard[newHeadRow][newHeadCol] = 1 + snakeBoard[headRow][headCol]
        canvas.data["headRow1"] = newHeadRow
        canvas.data["headCol1"] = newHeadCol
        removeTail1(canvas)


def moveSnake2(canvas, drow, dcol):
    # move the snake one step forward in the given direction.
    # store direction for next timer event
    canvas.data["snake2Drow"] = drow
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
        # snake ran into someone!
        gameOver(canvas,2)
    elif (snakeBoard[newHeadRow][newHeadCol] < 0):
        # Snake ate food. 
        snakeBoard[newHeadRow][newHeadCol] = 1 + snakeBoard[headRow][headCol]
        canvas.data["headRow2"] = newHeadRow
        canvas.data["headCol2"] = newHeadCol
        canvas.data["points2"] += 1
        placeFood(canvas)
    else:
        # normal move forward (not eating food)
        snakeBoard[newHeadRow][newHeadCol] = 1 + snakeBoard[headRow][headCol]
        canvas.data["headRow2"] = newHeadRow
        canvas.data["headCol2"] = newHeadCol
        removeTail2(canvas)

def removeTail2(canvas):
    # finding every snakecell containin snake2 in the board and removing one from it.
    # crucial aspect in making this game work.
    snakeBoard = canvas.data["snakeBoard"]
    rows = len(snakeBoard)
    cols = len(snakeBoard[0])
    for row in range(rows):
        for col in range(cols):
            if (snakeBoard[row][col] > 100):
                snakeBoard[row][col] -= 1


def removeTail1(canvas):
    # finding every snakecell containing snake1 in the board and removing one from it.
    # crucial aspect in making this game work.
    snakeBoard = canvas.data["snakeBoard"]
    rows = len(snakeBoard)
    cols = len(snakeBoard[0])
    for row in range(rows):
        for col in range(cols):
            if ((snakeBoard[row][col] > 0) and (snakeBoard[row][col] < 100)):
                snakeBoard[row][col] -= 1

def gameOver(canvas,who):
    # when the game shall end. 
    canvas.data["isGameOver"] = True
    canvas.data["whodied"] = who

def timerFired(canvas):
    # timer event trigging the game loop. 
    ignoreThisTimerEvent = canvas.data["ignoreNextTimerEvent"]
    canvas.data["ignoreNextTimerEvent"] = False
    if ((canvas.data["isGameOver"] == False) and
        (ignoreThisTimerEvent == False)):
        # only process timerFired if game is not over
        drow = canvas.data["snake1Drow"]
        dcol = canvas.data["snake1Dcol"]
        moveSnake1(canvas, drow, dcol)
        drow = canvas.data["snake2Drow"]
        dcol = canvas.data["snake2Dcol"]
        moveSnake2(canvas, drow, dcol)
        redrawAll(canvas)
    delay = 120 # milliseconds
    canvas.after(delay, timerFired, canvas) # pause, then call timerFired again

def redrawAll(canvas):
    # draws the information contained in the board onto the canvas displaying the game as we want to see it!
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
    # drawing the snakeboard onto the canvas
    snakeBoard = canvas.data["snakeBoard"]
    rows = len(snakeBoard)
    cols = len(snakeBoard[0])
    for row in range(rows):
        for col in range(cols):
            drawSnakeCell(canvas, snakeBoard, row, col)

def drawSnakeCell(canvas, snakeBoard, row, col):
    # drawing a snake cell. How depends on the info in the snakeboard. 
    margin = canvas.data["margin"]
    cellSize = canvas.data["cellSize"]
    left = margin + col * cellSize
    right = left + cellSize
    top = margin + row * cellSize
    bottom = top + cellSize
    if ((snakeBoard[row][col] > 0) and (snakeBoard[row][col] < 10)):
        # draw the snake body
        canvas.create_oval(left, top, right, bottom, fill="cyan")
    elif(snakeBoard[row][col] > 100):
        canvas.create_oval(left,top,right,bottom,fill="red")
    elif (snakeBoard[row][col] < 0):
        # draw food
        canvas.create_oval(left, top, right, bottom, fill="green")
        # used in debugging, drawing the number in the cell
    if (canvas.data["inDebugMode"] == True):
        canvas.create_text(left+cellSize/2,top+cellSize/2,
                           text=str(snakeBoard[row][col]),font=("Helvetica", 14, "bold"))

def loadSnakeBoard(canvas):
    # loads the snakeboard. 
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
    # placing the value of a food item, -1, onto the snakeboard. 
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
    # find where snakeBoard[row][col] is largest, and
    # store this location in headRow, headCol
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
    print "Ha det så kul! Tryck 'r' för att restarta spelet."

def init(canvas):
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
    # create the root and the canvas
    root = Tk()
    margin = 3
    cellSize = 15
    canvasWidth = 2*margin + cols*cellSize
    canvasHeight = 2*margin + rows*cellSize
    canvas = Canvas(root, width=canvasWidth, height=canvasHeight)
    canvas.pack()
    root.resizable(width=0, height=0)
    # Store canvas in root and in canvas itself for callbacks
    root.canvas = canvas.canvas = canvas
    # Set up canvas data and call init
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

run(50,50)
