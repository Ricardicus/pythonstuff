# This is a program that maps a 2d coordinate to one in 3d using some basic math
# learned in school. It draws a pendulum. Check it out! 

# using Tkinter for the GUI
from Tkinter import *
import math

# global varables
Width = 600.0
Height = 600.0

drawtime = True

x = 0
y = 0

dx = 0.0
dy = 0.0

theta = 0.0
radius = 260
	
def move(event):
	# using the Left and Right arrows, the dot in the left canvas moves causing the pendulum to move accordingly
	global theta

	if(event.keysym == "Left"):
		theta += 0.05 * math.pi
	elif(event.keysym == "Right"):
		theta += -0.05 * math.pi

def draw():
	# draws the running dot on the left canvas and the pendulum onto the right canvas.
	global canvas1
	global canvas2
	global y
	global x
	global theta
	global dx
	global dy
	global o1
	global o2
	global o3

	canvas1.delete(o1)
	canvas2.delete(o2)
	canvas2.delete(o3)

	dx = 2*math.cos(theta)
	dy = 2*math.sin(theta)
	x = (x+dx)%Width
	y = (y+dy)%Height	
	
	o1 = canvas1.create_oval(x,y,x+10,y+10,fill="red")
		
	x1 = x
	y1 = y
	theta2 = (x1 / Width) * math.pi
	psi = (y1 / Height) * 2 * math.pi
	y1 = Height / 2 + radius * math.cos(theta2)
	x1 = Width / 2 + radius * math.sin(theta2) * math.cos(psi)

	k = 10 * (1+math.cos(psi-math.pi/2))
	o2 = canvas2.create_line(Width/2,Height/2,x1,y1,width=2.0,smooth = 1,fill="blue")
	o3 = canvas2.create_oval(x1-k,y1-k,x1+k,y1+k,fill="blue")
	
def Letstryit(event):
	# drawing the pendulum (function name stems from eagerness)!
	global canvas1
	global canvas2
	global o1	
	global o2
	global o3
	global x
	global y
	global drawtime
	
	drawtime = False
	
	x = event.x % Width
	y = event.y % Height
		
	canvas1.delete(o1)
	canvas2.delete(o2)
	canvas2.delete(o3)

	o1 = canvas1.create_oval(x,y,x+10,y+10,fill="red")
	
	x1 = x
	y1 = y
	theta = (x1 / Width) * math.pi
	psi = (y1 / Height) * 2 * math.pi
	radius = 100
	y1 = Height / 2 + radius * math.cos(theta)
	x1 = Width / 2 + radius * math.sin(theta) * math.cos(psi)

	k = 10 * (1+math.cos(psi-math.pi/2))
	
	o2 = canvas2.create_line(Width/2,Height/2,x1,y1,width=5.0,smooth = 1,fill="blue")
	o3 = canvas2.create_oval(x1-k,y1-k,x1+k,y1+k,fill="blue")

def drawingtimeison(event):
	# wheter or not the drawing should occur, if the left canvas is clicked and held the state is active (true)
	global drawtime
	drawtime = True

def timer(canvas1):
	# the root loop! 
	if(drawtime):
		draw()	
	canvas1.after(20, timer, canvas1)

if __name__=="__main__":
	root = Tk()

	canvas1 = Canvas(root, width = Width, height = Height, bg = "blue")
	canvas2 = Canvas(root, width = Width, height = Height, bg = "red")
	canvas1.pack(side = LEFT)
	canvas2.pack(side = LEFT)
	o1 = canvas1.create_oval(0,0,0,0,fill="blue")
	o2 = canvas2.create_oval(0,0,0,0,fill="blue")
	o3 = canvas2.create_oval(0,0,0,0,fill="blue")
	#root.bind("<Button-1>",tryck)
	root.bind("<Key>",move)
	#root.bind("<B1-Motion>",tryck)
	#root.bind("<ButtonRelease-1>",tryck)	
	#root.bind("<B1-Motion>",Letstryit) 

	n = 20.0
	for i in range(0,int(n)):
		ps = 2 * math.pi
		th = i/n * math.pi
		y2 = Height / 2 + radius * math.cos(th)
		x2 = Width / 2 + radius * math.sin(th) * math.cos(ps)
		canvas2.create_oval(x2,y2,x2+4,y2+4,fill="blue")
		ps = math.pi
		y2 = Height / 2 + radius * math.cos(th)
		x2 = Width / 2 + radius * math.sin(th) * math.cos(ps)		 
		canvas2.create_oval(x2,y2,x2+4,y2+4,fill="blue")
		ps = 2 * math.pi
		th = i/n * math.pi
		y2 = Height / 2 + 20 * math.cos(th)
		x2 = Width / 2 + radius * math.sin(th) * math.cos(ps)
		k = 4/1.5 * (1+0.5*math.sin(th+math.pi/4))
		canvas2.create_oval(x2,y2,x2+k,y2+k,fill="blue")
		ps = math.pi
		y2 = Height / 2 + 20 * math.cos(th)
		x2 = Width / 2 + radius * math.sin(th) * math.cos(ps)	
		k = 4/1.5 * (1+0.5*math.sin(th+math.pi/4))
		canvas2.create_oval(x2,y2,x2+k,y2+k,fill="blue")
	#	ps = 16/24 * 2 * math.pi	
	#	y2 = Height / 2 + radius * math.cos(th)
	#	x2 = Width / 2 + radius * math.sin(th) * math.cos(ps)		 
	#	canvas2.create_oval(x2,y2,x2+2,y2+2,fill="blue")
	#	ps = 4/24 * 2 * math.pi	
	#	y2 = Height / 2 + radius * math.cos(th)
	#	x2 = Width / 2 + radius * math.sin(th) * math.cos(ps)		 
	#	canvas2.create_oval(x2,y2,x2+2,y2+2,fill="blue")
	canvas2.create_oval(Width/2-5,Height/2-5,Width/2+5,Height/2+5,fill="blue")
	root.bind("<B1-Motion>",Letstryit)
	root.bind("<ButtonRelease-1>",drawingtimeison)  
	root.title("2d till 3d!")
	timer(canvas1)
	root.mainloop()
	
