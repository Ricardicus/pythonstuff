# This is a program used to send secrets!
# It's implemented in Python2.x and will only run on iOS devices using Python2.x 

# coding: UTF-8

# The GUI is implemented in Tkinter! (works for python 2.x)

import Tkinter as tk

from os import system

from tkFileDialog import askopenfilename 

# font
TITLE_FONT = ("Avenir",30)

def crypt(entry,title):
# Encrypting messange retrieved from 'entry' field and displaying it 'title' field
	
	global v
	global b
	global z
	
	message = u''
	st = unicode(entry.get())
	a = 0
	
	for i in range(0,len(st)):
		l = b[st[i]]	
		p = a % len(z)
		message += v[(l+z[p]) % len(v)]
		a += 1
	
	title.delete(1.0,'end')
	title.insert('insert',message)

def cryptfile(st):
# returning an encrypted version of the string 'st'
	global title
	message = u''
	
	a = 0
	for i in range(0,len(st)):
		l = bfile[st[i]]
		p = a % len(z)
		message += vfile[(l+z[p]) % len(vfile)]	
		a += 1

	title.delete(1.0,'end')
	title.insert('insert','Sådär! Det lyckades. Filen är krypterad.')
    
	return message

def decrypt(entry,title,intvar):
# Decrypting messange retrieved from 'entry' field and displaying it 'title' field
# If the Tk.intvar class instance intvar returns 'true' upon the get() call the 
# decrypted message will be said by the computer
# - only works for iOS machines!!!
	
	global v
	global b
	global z
	global message
	
	
	message = u''	
	st = unicode(entry.get())
	a = 0
		
	for i in range(0,len(st)):
		l = b[st[i]]			
		p = a % len(z)	
		message += v[(len(v)*5+l-z[p]) % len(v)]
		a += 1

	
	title.delete(1.0,'end')
	title.insert('insert',message)
    
	if(intvar.get()):
		try:
			system('say '+str(message.encode('UTF-8')))    
		except ValueError:
			print("funkade ej :/")

def decryptfile(st):
# returns an encrypted version of the string 'st'
	global title
	
	message = u''	
	a = 0
		
	for i in range(0,len(st)):
		l = bfile[st[i]]
		p = a % len(z)
		message += vfile[(len(vfile)*5+l-z[p]) % len(vfile)]
		a += 1

	title.delete(1.0,'end')
	title.insert('insert','Sådär! Det lyckades. Filen är dekrypterad.')
	return message


def setKey(entry):
# sets how the encryption will work by setting the crypting key to the value contained in the entry field from 'entry'
	global z
	
	st = unicode(entry.get())
	z = []
	for i in st:
		z.append(ord(i))

def readandcrypt():
# reads and crypts a .txt file
# if it doesn't work, it wont erase the content of .txt file!
	filename = askopenfilename()
	
	try:
		file = open(filename,'r')
		
	except ValueError:
		
		title.delete(1.0,'end')
		title.insert('insert','Tyvärr gick det inte att läsa den där filen!')
		return
	except IOError:
		return

	file_data = file.read()
	file.close()
	
	try:
		file = open(filename,'w')
		
	except ValueError:
		
		title.delete(1.0,'end')
		title.insert('insert','Tyvärr gick det inte att läsa den där filen!')
		return
	except IOError:
		return	
	
	file_data = file_data.decode("UTF-8")
	result = u''
	try:
		result += cryptfile(file_data)
	except Exception:
		print "The file contained characters that weren't supported!"
		file.write(file_data.encode("UTF-8"))
		return
	file.write(result.encode("UTF-8"))

def readanddecrypt():
# reads and decrypts a .txt file
# if it doesn't work, it wont erase the content of .txt file!
	filename = askopenfilename()
	
	try:
		file = open(filename,'r')
		
	except ValueError:
		
		title.delete(1.0,'end')
		title.insert('insert','Tyvärr gick det inte att läsa den där filen!')
		return

	except IOError:
		return
	
	file_data = file.read()
	file.close()
	
	try:
		file = open(filename,'w')
		
	except ValueError:
		
		title.delete(1.0,'end')
		title.insert('insert','Tyvärr gick det inte att läsa den där filen!')
		return

	except IOError:
		return
	
	file_data = file_data.decode("UTF-8")
	result = u''
	try:
		result += decryptfile(file_data)
	except Exception:
		print "The file contained characters that weren't supported!"
		file.write(file_data.encode("UTF-8"))
		return
	file.write(result.encode("UTF-8"))

class LurisApp(tk.Tk):
# The root of the GUI 
	def __init__(self,*args,**kwargs):
		tk.Tk.__init__(self,*args,**kwargs)
		self.bind("<Escape>", lambda e: e.widget.quit())
		container = tk.Frame(self)
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)
		
# Initialising the dictionary stored in the class that contains the Tk.Frame instances that can be displayed
		self.frames = {}
		for F in (Meny, Kryptera,Krypterafil):
			frame = F(container, self)
			self.frames[F] = frame
			frame.grid(row=0, column=0, rowspan=12, columnspan=6, sticky="nsew")

		self.show_frame(Meny)

# Method called to switch frames
	def show_frame(self, c):
		frame = self.frames[c]
		frame.tkraise()

class Meny(tk.Frame):
# The Menu frame class
	def __init__(self,parent,controller):
		tk.Frame.__init__(self,parent)
		label = tk.Label(self,background = "blue",text="Luris! Huvudmeny",fg = "white",font=TITLE_FONT)
		label.pack(side="top", fill="x", pady=10)
		self.configure(bg="blue",highlightbackground="blue",background="blue")
		
		btn1 = tk.Button(self,highlightbackground="blue",text="Kryptera/avläsa ett meddelande ",command=lambda: controller.show_frame(Kryptera))
		btn2 = tk.Button(self,highlightbackground="blue",text="Kryptera/avläsa en fil",command=lambda: controller.show_frame(Krypterafil))
		btn1.pack()
		btn2.pack()

class Kryptera(tk.Frame):
# The class representing the frame where direct message en/decrypting can be done
	def __init__(self,parent,controller):
		tk.Frame.__init__(self,parent)
		global w
		
		root = self
		top = tk.Frame(self)
		self.configure(background="blue")
		hdr = tk.Label(top,text="Luris!",font=("Avenir",20),fg="white",bg="blue",height=3)
		hdr.pack()
		bottom = tk.Frame(root,bd=0,relief=tk.FLAT)
		title = tk.Text(bottom,height=10)
		title.insert(tk.INSERT,"")
		title.configure(background="blue",insertbackground="blue",foreground="white",highlightbackground="blue")


		subtop = tk.Frame(root,bd=0)
		subtop.configure(background="blue")

		subtop2 = tk.Frame(root,bd=0)
		subtop2.configure(background="blue")

		subsubtop = tk.Frame(root,bd=0)
		subsubtop.configure(background="blue")

		w = tk.Entry(subsubtop, text="Skriv det du vill kryptera!",bd=0,selectbackground="blue",fg="black",width=150)
		intvar = tk.IntVar()

		bnt1 = tk.Button(subtop, bd=0,highlightbackground="blue",text="Kryptera", bg="blue",command=lambda: crypt(w,title))
		btn2 = tk.Button(subtop, highlightbackground="blue",relief = tk.FLAT,bd=0,bg="blue",text="Avläs",command=lambda: decrypt(w,title,intvar))
		btn3 = tk.Button(subtop, relief = tk.FLAT, highlightbackground="blue", bd=0,bg="blue",text="Sätt nyckel",command=lambda: setKey(w))
		btn4 = tk.Button(subtop, relief = tk.FLAT,bd=0, highlightbackground="blue", bg="blue",text="Återgå till meny",command=lambda: controller.show_frame(Meny))

		c = tk.Checkbutton(subtop2, variable = intvar)
		l = tk.Label(subtop2,text = "Läs upp meddelandet",fg = "white",bg ="blue")
		c.config(foreground = "white",bg="blue")
		c.pack(side=tk.LEFT)
		l.pack(side=tk.LEFT)
		          

		title.pack(side="top")
		bnt1.pack(side=tk.LEFT)
		btn2.pack(side=tk.LEFT)
		btn3.pack(side=tk.LEFT)
		btn4.pack(side=tk.BOTTOM)
		w.pack(anchor=tk.CENTER)

		top.pack(side=tk.TOP)
		bottom.pack(side="bottom")
		subtop.pack()
		subsubtop.pack()
		subtop2.pack()

class Krypterafil(tk.Frame):
	# The class that describes the frame in which file encryption can be done!
	def __init__(self,parent,controller):
		tk.Frame.__init__(self,parent)
		global title
		global intvar

		self.configure(background ="blue")

		top = tk.Frame(self)

		top.configure(background="blue")

		bottom = tk.Frame(self)

		title = tk.Text(bottom,height=10)
		title.insert(tk.INSERT,"")
		title.configure(background="blue",insertbackground="blue",foreground="white",highlightbackground="blue")

		hdr = tk.Label(top,text="Kryptera/avläs fil!",font=("Avenir",20),fg="white",bg="blue",height=3)
		hdr.pack()

		w = tk.Entry(top, text="Skriv det du vill kryptera!",bd=0,selectbackground="blue",fg="black",width=150)

		b1 = tk.Button(top,bd=0,highlightbackground="blue",text="Sätt nyckel",command=lambda: setKey(w))

		b2 = tk.Button(bottom,highlightbackground="blue", text="Kryptera en .txt fil med aktuell nyckel!", background = "blue", command=readandcrypt)
		b3 = tk.Button(bottom,highlightbackground="blue", text="Avläs en .txt fil med aktuell nyckel!", background = "blue", command=readanddecrypt)
		b4 = tk.Button(bottom,highlightbackground="blue",text="Till meny", bg = "blue", command=lambda: controller.show_frame(Meny))

		w.pack(side="bottom")
		b1.pack()
		b2.pack(side='left')
		b3.pack(side='right')
		b4.pack();

		bottom.pack(side="bottom")
		
		top.pack()

if __name__=="__main__":
# The call that initialises the varibles used in the app and the app istelf!
	message = u''

	v = [u'a',u'b',u'c',u'd',u'e',u'f',u'g',u'h',u'i',u'j',u'k',u'l',u'm',u'n',u'o',u'p',u'q',u'r',u's',u't',u'u',u'v',u'w',u'x',u'y',u'z',u'å',u'ä',u'ö',u'!',u'?',u'1',u'2',u'3',u'0',u'4',u'5',u'6',u'7',u'8',u'9',u'-',u'(',u'A',u'B',u'C',u'D',u'E',u'F',u'G',u'H',u'I',u'J',u'K',u'L',u'M',u'N',u'O',u'P',u'Q',u'R',u'S',u'T',u'U',u'V',u'W',u'X',u'Y',u'Z',u'.',u' ',u'\n',u'Å',u'Ä',u'Ö',u',',u'/',u':',u';',u'&',u'@']
	vfile = [f for f in v]
	vfile.append(u"'")
	b = {}

	for i in range(0,len(v)):
		b[v[i]] = i

	bfile = {}

	for i in range(0,len(vfile)):
	
		bfile[vfile[i]] = i

	z = [1,10,-5,13,12,12,14,14,14,2,8,13,11,7,-2,22,-22,5,8,8,-10,4,4]

	intvar = 0
	luris = LurisApp()

	luris.bind("<Escape>", lambda e: e.widget.quit())

	luris.mainloop()