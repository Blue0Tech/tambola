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

gameWindow = None
ticketGrid = []
currentNumberList = []
randomColList = []

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
    global gameWindow

    playerName = nameEntry.get()
    nameEntry.delete(0,END)
    nameWindow.destroy()

    SERVER.send(playerName.encode())

    gameWindow = Tk()
    gameWindow.title('Tambola Family Fun!')
    gameWindow.geometry('800x600')
    
    swidth = gameWindow.winfo_screenwidth()
    sheight = gameWindow.winfo_screenheight()
    bg = ImageTk.PhotoImage(file='./assets/background.png')

    createTicket()
    placeNumber()

def receivedMsg():
    pass

def createTicket():
    global gameWindow
    global ticketGrid

    mainLabel = Label(gameWindow,width=92,height=17,relief='ridge',borderwidth=5,bg='white')
    mainLabel.place(x=95,y=119)

    xPos = 105
    yPos = 130

    for row in range(0,3):
        rowList = []
        for col in range(0,10):
            boxButton = Button(gameWindow,font=('Chalkboard SE',30),width=2,height=1,borderwidth=5,bg='#fff176')
            boxButton.place(x=xPos,y=yPos)
            rowList.append(boxButton)
            xPos+=64
        ticketGrid.append(rowList)
        xPos = 105
        yPos+=82

def placeNumber():
    global ticketGrid
    global currentNumberList
    global randomColList

    for row in range(0,3):
        randomColList = []
        counter = 0
        while(counter<=4):
            randomCol = random.randint(0,9)
            if(randomCol not in randomColList):
                randomColList.append(randomCol)
                counter+=1
    
    numberContainer = {}
    for i in range(0,3):
        numberContainer[i] = []
        for j in range(0,10):
            number = (i*10)+j
            numberContainer[i].append(number)
    
    counter = 0
    while(counter < len(randomColList)):
        colNum = randomColList[counter]
        # numbersListByIndex = numberContainer[str(colNum)]
        # randomNumber = random.choice(numbersListByIndex)
        randomList = random.choice(list(numberContainer.items()))
        currentRow = randomList[0]
        randomNumber = randomList[1][colNum]

        if(randomNumber not in currentNumberList):
            numberBox = ticketGrid[currentRow][colNum]
            numberBox.configure(text=randomNumber,fg='black')
            currentNumberList.append(randomNumber)
            counter+=1

setup()