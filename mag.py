from Tkinter import *
import math

def draw_arrow(start_x,start_y,dir_x,dir_y,canvas):
	color = canvas.info["field lines color"]
	if(dir_x==0):
		return
	theta = math.atan(-dir_y/dir_x);
	if(dir_y>0 and dir_x < 0):
		theta += math.pi/2
	elif(dir_y<0 and dir_x <0):
		theta += math.pi
	canvas.create_line(start_x,start_y,start_x+dir_x,start_y+dir_y,fill=color)
#	mag = math.sqrt(dir_x**2+dir_y**2)/4

#	offset = 0.5

#	canvas.create_line(start_x+mag*math.cos(theta+offset),start_y+mag*math.sin(theta-offset),start_x+dir_x,start_y+dir_y,fill=color)
#	canvas.create_line(start_x+mag*math.cos(theta-offset),start_y+mag*math.sin(theta+offset),start_x+dir_x,start_y+dir_y,fill=color)

def draw(click):
	global w
	w.create_rectangle(0,0,w.info["width"],w.info["height"],fill=w.info["background color"])
	x = click.x
	y = click.y
	dir_x = 0
	dir_y = 0
	mag = 0
	for wx in range(0,w.info["width"]):
		for wy in range(0,w.info["height"]):
			if( not (abs(wx-x) < 10 and abs(wy-y) < 10) and wx % 20 == 0 and wy % 20 == 0):
				R = math.sqrt((wx-x)**2 + (wy-y)**2)
				power = 1000
				mag = power/(R**2)
				if(mag > power/100):
					mag = power/100
				dir_x = (wx-x)*mag
				dir_y = (wy-y)*mag
				draw_arrow(wx,wy,dir_x,dir_y,w)
				w.create_line(wx,wy,wx+dir_x,wy+dir_y,fill=w.info["field lines color"])
	p = w.info["dot width"]
	w.create_oval(x-p,y-p,x+p,y+p,fill="green")
	w.create_line(x,y+p,x,y-p,fill="black")
	w.create_line(x-p,y,x+p,y,fill="black")

if __name__=="__main__":
	root = Tk()
	global w

	width = 800
	height = 600

	w = Canvas(root,width=width,height=height)
	w.info = {}
	w.info["width"] = width
	w.info["height"] = height
	w.info["background color"] = "blue"
	w.info["field lines color"] = "white"
	w.info["dot width"] = 5
	w.bind("<Button-1>", draw)
	root.bind("<Escape>", lambda e: e.widget.quit())
	w.pack()
	w.create_rectangle(0,0,w.info["width"],w.info["height"],fill=w.info["background color"])

	root.mainloop()

