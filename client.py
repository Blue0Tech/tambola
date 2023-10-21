import socket
from threading import Thread
from tkinter import *
import random
from PIL import Image, ImageTk

SERVER = None
IP_ADDRESS = '127.0.0.1'
PORT = 5000

def setup():
    global SERVER
    global IP_ADDRESS
    global PORT

    SERVER = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS,PORT))

    thread = Thread(target=receivedMsg)
    thread.start()
    askPlayerName()

playerName = None
nameEntry = None
nameWindow = None
canvas1 = None

def askPlayerName():
    global playerName
    global nameEntry
    global nameWindow
    global canvas1

    nameWindow = Tk()
    nameWindow.title('Tambola Family Fun!')
    nameWindow.geometry('800x600')

    swidth = nameWindow.winfo_screenwidth()
    sheight = nameWindow.winfo_screenheight()
    bg = ImageTk.PhotoImage(file='./assets/background.png')

    canvas1 = Canvas(nameWindow,width=500,height=500)
    canvas1.pack(fill='both',expand=True)
    canvas1.create_image(0,0,image=bg,anchor='nw')
    canvas1.create_text(swidth/4.5,sheight/8,text='Enter Name',font=('Chalkboard SE',60),fill='black')

    nameEntry = Entry(nameWindow,width=15,justify='center',font=('Chalkboard SE',30),bd=5,bg='white')
    nameEntry.place(x=swidth/7,y=sheight/4)

    button = Button(nameWindow,text='Save',font=('Chalkboard SE',30),width=11,command=saveName,height=2,bg='#80DEEA',bd=3)
    button.place(x=swidth/6,y=sheight/3)

    nameWindow.resizable(True,True)
    nameWindow.mainloop()

def saveName():
    global SERVER
    global nameWindow
    global nameEntry
    global playerName

    playerName = nameEntry.get()
    nameEntry.delete(0,END)
    nameWindow.destroy()

    SERVER.send(playerName.encode())

def receivedMsg():
    pass

setup()