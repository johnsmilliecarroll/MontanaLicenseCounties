import csv
import tkinter as tk
from tkinter import Canvas
from tkinter import Radiobutton
from tkinter import PhotoImage

#  set up CSV
myfile = open("MontanaCounties.csv")
numCounties = 56

mycsv = csv.reader(myfile)  # read file

next(mycsv)  # read past header
rows = []
for row in mycsv:
    rows.append(row)  # add rows to array

orderedRows = []
for x in range(1, numCounties + 1):  # order array by license number
    for y in rows: # loop through whole list to find the current index
        if int(y[2]) == x:  # if the license number is the same as our current index
            orderedRows.append(y)
            rows.remove(y)  # get rid of it so we don't have to check it again
            break

# set up GUI
winwidth = 640
winheight = 480

wn = tk.Tk()
wn.title("County License Plate Prefixes")
wn.geometry(str(winwidth) + "x" + str(winheight))
canvas = Canvas(wn, width=winwidth, height=winheight)
canvas.pack()

myValue = tk.StringVar()  # radio button values

myState = tk.Label(wn)  # county name
myState.place(x=winwidth * 0.25, y=winheight / 4, anchor='center')
mySeat = tk.Label(wn)  # county seat
mySeat.place(x=winwidth * 0.75, y=winheight / 4, anchor='center')
myError = tk.Label(wn, fg="red")  # error text
myError.place(x=winwidth * 0.75, y=40, anchor='center')
radioValue = tk.StringVar(wn, '2')
img1 = PhotoImage()
img2 = PhotoImage()
Image1 = canvas.create_image(winwidth * 0.25, winheight * 0.60, image=img1, anchor='center')
Image2 = canvas.create_image(winwidth * 0.75, winheight * 0.60, image=img2, anchor='center')


def returnInfo():  # populate the gui with the information
    global myError
    global img1
    global img2
    try:
        if myValue.get() != "":  # make sure it isn't empty
            myIndex = int(myValue.get()) - 1  # get index
            myStateVal = orderedRows[myIndex][0]
            mySeatVal = orderedRows[myIndex][1]
            path1 = "images/" + str(myValue.get()) + "-0.png"  # get path for images
            path2 = "images/" + str(myValue.get()) + "-1.png"
            if radioValue.get() == '0':  # radio button is only county
                myState["text"] = "County Name: " + myStateVal
                mySeat["text"] = ""
                img1 = PhotoImage(file=path1)
                img2 = PhotoImage()
            elif radioValue.get() == '1':  # radio button is only seat
                myState["text"] = ""
                mySeat["text"] = "Seat City: " + mySeatVal
                img1 = PhotoImage()
                img2 = PhotoImage(file=path2)
            else:    # radio button is both
                myState["text"] = "County Name: " + myStateVal
                mySeat["text"] = "Seat City: " + mySeatVal
                img1 = PhotoImage(file=path1)
                img2 = PhotoImage(file=path2)
            canvas.itemconfig(Image1, image=img1, anchor='center')  # change images
            canvas.itemconfig(Image2, image=img2, anchor='center')
            myError['text'] = ""  # it worked so erase any errors
    except IndexError:
        myError['text'] = "Value not valid!"
    except ValueError:
        myError['text'] = "Value not a number!"


# set up the rest of the gui

myLabel = tk.Label(wn, text="Enter License Plate Prefix Number:")
myLabel.place(x=winwidth / 2, y=15, anchor='center')

txtEntry = tk.Entry(wn, textvariable=myValue)
txtEntry.place(x=winwidth / 2, y=40, anchor='center')

radio0 = Radiobutton(wn, text="County", variable=radioValue, value='0')
radio0.place(x=winwidth * 0.25, y=70, anchor='center')
radio1 = Radiobutton(wn, text="Seat", variable=radioValue, value='1')
radio1.place(x=winwidth * 0.5, y=70, anchor='center')
radio2 = Radiobutton(wn, text="Both", variable=radioValue, value='2')
radio2.place(x=winwidth * 0.75, y=70, anchor='center')

btnMyButton = tk.Button(wn, text="Enter", command=returnInfo)
btnMyButton.place(x=winwidth / 3, y=40, anchor='center')

wn.mainloop()
