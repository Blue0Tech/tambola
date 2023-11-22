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

flashNumberLabel = None
flashNumberList = []
canvas2 = None
gameOver = False
markedNumberList = []

def showWrongMarking():
    global ticketGrid
    global flashNumberList

    for row in ticketGrid:
        for numberBox in row:
            if(numberBox['text']):
                if(int(numberBox['text']) not in flashNumberList):
                    numberBox.configure(state='disabled',background='#f48fb1',foreground='white')

def markNumber(button):
    global markedNumberList
    global flashNumberList
    global playerName
    global SERVER
    global currentNumberList
    global gameOver
    global flashNumberLabel
    global canvas2

    buttonText = int(button['text'])
    markedNumberList.append(buttonText)

    button.configure(state='disabled',background='#c5e1a5',foreground='black')

    winner = all(item in flashNumberList for item in markedNumberList)

    if(winner and sorted(currentNumberList) == sorted(markedNumberList)):
        message = playerName + ' wins the game.'
        SERVER.send(message.encode('utf-8'))
        return
    
    if(len(currentNumberList) == len(markedNumberList)):
        winner = all(item in flashNumberList for item in markedNumberList)
        if(not winner):
            gameOver = True
            message = 'You lose the game'
            canvas2.itemconfigure(flashNumberLabel,text=message,font=('Chalkboard SE',40))
            showWrongMarking()

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
    global flashNumberLabel
    global canvas2

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
    
    canvas2 = Canvas(gameWindow,width=500,height=500)
    canvas2.create_image(0,0,image=bg,anchor='nw')
    canvas2.pack(fill='both',expand=True)
    canvas2.create_text(swidth/4.5,50,text='Tambola Family Fun',font=('Chalkboard SE',50),fill='#3e2723')

    createTicket()
    placeNumber()

    flashNumberLabel = canvas2.create_text(400,sheight/2,text='Waiting for others to join...',font=('Chalkboard SE',30),fill='#3e2723')

    gameWindow.mainloop()

def receivedMsg():
    global SERVER
    global flashNumberLabel
    global flashNumberList
    global canvas2
    global gameOver

    numbers = [str(i) for i in range(0,30)]

    while(True):
        chunk = SERVER.recv(2048).decode()
        if(chunk in numbers and flashNumberLabel and not gameOver):
            flashNumberList.append(int(chunk))
            configureCanvas2(chunk,60)
        elif('wins the game.' in chunk):
            gameOver = True
            configureCanvas2(chunk,40)

def configureCanvas2(chunk,size):
    global canvas2
    global flashNumberLabel

    canvas2.itemconfigure(flashNumberLabel,text=chunk,font=('Chalkboard SE',size))

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
            boxButton.configure(command = lambda boxButton = boxButton : markNumber(boxButton))
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