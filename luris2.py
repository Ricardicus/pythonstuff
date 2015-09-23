#coding: UTF-8
from Tkinter import *
from os import system

# the encryption function! Linear and determined by adding content of the z-list
def crypt():
	global v
	global w
	global b
	global z
	global message
	global title
	
	message = unicode('','UTF-8')
	st = unicode(w.get())
	a = 0
	for i in range(0,len(st)):
		l = b[st[i]]
		p = a % len(z)
		message += v[(l+z[p]) % len(v)]
		a += 1
    
	title.delete(1.0,END)
        title.insert(INSERT,message)

# the decrytion function! Identical with the crypt() function but decrypts by substracting content of the z-list instead 	
def decrypt():
	global w
	global v
	global b
	global z
        global intvar
	global message
	
	message = unicode('','UTF-8')
	st = unicode(w.get())
	a = 0
	for i in range(0,len(st)):
		l = b[st[i]]			
		p = a % len(z)	
		message += v[(len(v)*5+l-z[p]) % len(v)]
		a += 1

	title.delete(1.0,END)
        title.insert(INSERT,message)
        if(intvar.get()):
            try:
                system('say '+str(message.encode('UTF-8')))
            except ValueError:
                print "funkade ej :/"

# set the encryption key
def setKey():
	global z
	global w

	st = w.get()
	z = []
	for i in st:
		z.append(ord(i))

if __name__=="__main__":
	# sets data, creates GUI and runs the program!
	message = unicode('')
	v = [u'a',u'b',u'c',u'd',u'e',u'f',u'g',u'h',u'i',u'j',u'k',u'l',u'm',u'n',u'o',u'p',u'q',u'r',u's',u't',u'u',u'v',u'w',u'x',u'y',u'z',u'å',u'ä',u'ö',u'!',u'?',u'1',u'2',u'3',u'0',u'4',u'5',u'6',u'7',u'8',u'9',u'-',u'(',u'A',u'B',u'C',u'D',u'E',u'F',u'G',u'H',u'I',u'J',u'K',u'L',u'M',u'N',u'O',u'P',u'Q',u'R',u'S',u'T',u'U',u'V',u'W',u'X',u'Y',u'Z',u'.',' ',u'Å',u'Ä',u'Ö',u',',u'/',u':',u';',u'&',u'@']
	b = {}
	for i in range(0,len(v)):
		b[v[i]] = i
	z = [1,10,5,5,5,4,-2,18,13,13,13,1,2,0,-4,0,17,9,21,8,-10,4,4]

	root = Tk()
	root.title("Lurisen")
	root.configure(background="blue")
	root.geometry("1200x600")
	root.bind("<Escape>", lambda e: e.widget.quit())
	top = Frame(root)
	top.configure(background="blue")
	hdr = Label(top,text="Luris!",state=DISABLED,font=("Avenir",20),fg="white",bg="blue",height=3)
	hdr.pack()
	bottom = Frame(root,bd=0,relief=FLAT)
	title = Text(bottom,height=10)
	title.insert(INSERT,"")
	title.configure(background="blue",insertbackground="blue",foreground="white",highlightbackground="blue")


	subtop = Frame(root,bd=0)
	subtop.configure(background="blue")

	subtop2 = Frame(root,bd=0)
	subtop2.configure(background="blue")

	subsubtop = Frame(root,bd=0)
	subsubtop.configure(background="blue")


	w = Entry(subsubtop, text="Skriv det du vill kryptera!",bd=0,selectbackground="blue",fg="black",width=150)

	#cryptcommand = partial(crypt,w1.get())
	bnt1 = Button(subtop, bd=0,text="Kryptera",relief = FLAT, bg="blue",command=crypt)
	bnt1.config(highlightbackground="blue")
	btn2 = Button(subtop, relief = FLAT,bd=0,bg="blue",text="Avläs",command=decrypt)
	btn2.config(highlightbackground="blue")
	btn3 = Button(subtop, relief = FLAT,bd=0,bg="blue",text="Sätt nyckel",command=setKey)
	btn3.config(highlightbackground="blue")

	intvar = IntVar()
	c = Checkbutton(subtop2, variable = intvar)
	l = Label(subtop2,text = "Läs upp meddelandet",fg = "white",bg ="blue")
	c.config(foreground = "white",bg="blue")
	c.pack(side=LEFT)
	l.pack(side=LEFT)
	          

	title.pack(side="top")
	bnt1.pack(side=LEFT)
	btn2.pack(side=LEFT)
	btn3.pack(side=LEFT)
	w.pack(anchor=CENTER)

	top.pack(side=TOP)
	bottom.pack(side="bottom")
	subtop.pack()
	subsubtop.pack()
	subtop2.pack()

	root.mainloop()
