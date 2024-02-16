from tkinter import *
from random import *

#сделаем список карт
cards = [6, 8, 9, 10, 'валет', 'дама', 'король', 'туз'] * 4
shuffle(cards)
cmd = 0


def take():
    global cmd, cards
    card = cards.pop()
    if card == 'валет':
        card = 2
    if card == 'дама':
        card = 3
    if card == 'король':
        card = 4
    if card == 'туз':
        card = 11
    cmd += card

    if cmd > 21:
        lbl3['text'] = 'вы проиграли, так как ' + str(cmd) + ' очков'
        lbl2["text"] = 'вы проиграли'
    else:
        lbl2["text"] = "у вас " + str(cmd) + " очков"


def enough():
    global cmd
    if cmd == 21:
        lbl3['text'] = 'поздравляем, у вас ровно 21'
    if cmd < 21:
        lbl3['text'] = 'у вас ровно' + str(cmd) + ' очков'

#обозначим
tk = Tk()
tk.geometry('300x140')

lbl1 = Label(tk, text="Игра в Black-Jack", fg="black")
lbl1.place(x=100, y=0)

lbl2 = Label(tk, text="У вас 0 очков", fg="black")
lbl2.place(x=110, y=30)

btn = Button(tk, width="15", text="Взять", command=take)
btn.place(x=20, y=60)

btn2 = Button(tk, width="15", text="Стоп", command=enough)
btn2.place(x=160, y=60)

lbl3 = Label(tk, text="Результат игры", fg="red")
lbl3.place(x=90, y=100)

tk.mainloop()
