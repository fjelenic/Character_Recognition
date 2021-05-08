import math
from matrica import *
import random
import NeuronskeMreze as NN
from tkinter import *


def centroid(vektor):
    Tc = vektor[0][:]
    for tocka in vektor[1:]:
        for i in range(len(tocka)):
            Tc[i] += tocka[i]
    for i in range(len(Tc)):
        Tc[i] /= len(vektor)
    return tuple(Tc)


def euklidska_udaljenost(v1, v2):
    dx = v1[0] - v2[0]
    dy = v1[1] - v2[1]
    return math.sqrt(dx ** 2 + dy ** 2)


def duljina(vektor):
    kumulativna_duljina = [0]
    for i in range(len(vektor) - 1):
        kumulativna_duljina.append(euklidska_udaljenost(vektor[i], vektor[i + 1]) + kumulativna_duljina[-1])
    return kumulativna_duljina


slova = ['ALFA', 'BETA', 'GAMA', 'DELTA', 'EPSILON']
slovo_index = 0
redni_broj = 1
MAX_UZORAKA = 20
M = 50


## RADNO!!!

def click_predict(event):
    global koordinate
    koordinate = []
    canvas.delete("all")
    koordinate.append([event.x, event.y])


def drag_predict(event):
    global koordinate
    canvas.create_line(koordinate[-1][0], koordinate[-1][1], event.x, event.y, fill="#000000")
    koordinate.append([event.x, event.y])


def release_predict(event):
    global slova, koordinate, nn
    Tc = centroid(koordinate)
    for i in range(len(koordinate)):
        koordinate[i][0] -= Tc[0]
        koordinate[i][1] -= Tc[1]
    mx = max(koordinate, key=lambda x: abs(x[0]))[0]
    my = max(koordinate, key=lambda x: abs(x[1]))[1]
    m = max(abs(mx), abs(my))
    for i in range(len(koordinate)):
        koordinate[i][0] /= m
        koordinate[i][1] /= m
    kumulativna_duljina = duljina(koordinate)
    D = kumulativna_duljina[-1]
    uzorkovan_vektor = []
    i = 0
    for k in range(M):
        while True:
            if kumulativna_duljina[i] + 10 ** -6 >= (k * D) / (M - 1):
                uzorkovan_vektor.append(koordinate[i])
                break
            i += 1
    X = []
    for v in uzorkovan_vektor:
        X.append(v[0])
        X.append(v[1])
    pred = nn.predict(Matrica([X]))
    print("Izlaz NN za primjer => {}".format(~pred))
    pred = NN.dekodiraj_predvidjanje(pred)
    label['text'] = slova[pred]


nn = NN.NeuronskaMreza(100, 6, 5)
X, y = NN.raspakiraj('oznaceni_primjeri.txt')
nn.fit(X, y, 0.1, 150)#, "Stohastic Backpropagation")

window = Tk()
canvas = Canvas(window, width=400, height=400, background='white')
canvas.bind("<ButtonPress-1>", click_predict)
canvas.bind('<B1-Motion>', drag_predict)
canvas.bind('<ButtonRelease-1>', release_predict)
canvas.grid(row=1, column=0)
label = Label(bd=4, relief="solid", font="Times 22 bold", bg="white", fg="black")
label.grid(row=0, column=0)
label['text'] = "Napišite slovo:"

koordinate = []
window.mainloop()
