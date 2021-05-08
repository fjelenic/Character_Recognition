import NeuronskeMreze as NN
from tkinter import *
import math
from matrica import *

MAX_UZORAKA = 6
M = 50


# IZRADA SKUPA ZA UČENJE

def click(event):
    global koordinate
    koordinate.append([event.x, event.y])


def drag(event):
    global koordinate
    canvas.create_line(koordinate[-1][0], koordinate[-1][1], event.x, event.y, fill="#000000")
    koordinate.append([event.x, event.y])


def release(event):
    global primjeri, koordinate, slova, slovo_index, redni_broj
    primjeri.append((koordinate, slova[slovo_index]))
    koordinate = []
    canvas.delete("all")
    if redni_broj == MAX_UZORAKA and slovo_index == len(slova) - 1:
        window.destroy()
    elif redni_broj < MAX_UZORAKA:
        redni_broj += 1
    else:
        slovo_index += 1
        redni_broj = 1
    label['text'] = "{} {}/{}".format(slova[slovo_index], redni_broj, MAX_UZORAKA)


window = Tk()
canvas = Canvas(window, width=400, height=400, background='white')
canvas.bind("<ButtonPress-1>", click)
canvas.bind('<B1-Motion>', drag)
canvas.bind('<ButtonRelease-1>', release)
canvas.grid(row=1, column=0)

slova = ['ALFA', 'BETA', 'GAMA', 'DELTA', 'EPSILON']
slovo_index = 0
redni_broj = 1

label = Label(bd=4, relief="solid", font="Times 22 bold", bg="white", fg="black")
label.grid(row=0, column=0)
label['text'] = "{} 1/{}".format(slova[0], MAX_UZORAKA)

koordinate = []
primjeri = []

window.mainloop()


# RAD S DOBIVENIM VEKTORIMA TOČAKA

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


def jednojedinicni_kod(y):
    index = slova.index(y)
    kod = []
    for i in range(len(slova)):
        if i == index:
            kod.append(1)
        else:
            kod.append(0)
    return kod


pripremljeni_primjeri = []
for primjer in primjeri:
    Tc = centroid(primjer[0])
    for i in range(len(primjer[0])):
        primjer[0][i][0] -= Tc[0]
        primjer[0][i][1] -= Tc[1]
    mx = max(primjer[0], key=lambda x: abs(x[0]))[0]
    my = max(primjer[0], key=lambda x: abs(x[1]))[1]
    m = max(abs(mx), abs(my))
    for i in range(len(primjer[0])):
        primjer[0][i][0] /= m
        primjer[0][i][1] /= m
    kumulativna_duljina = duljina(primjer[0])
    D = kumulativna_duljina[-1]
    uzorkovan_vektor = []
    i = 0
    for k in range(M):
        while True:
            if kumulativna_duljina[i] + 10 ** -6 >= (k * D) / (M - 1):
                uzorkovan_vektor.append(primjer[0][i])
                break
            i += 1
    pripremljeni_primjeri.append((uzorkovan_vektor, jednojedinicni_kod(primjer[1])))

with open("oznaceni_primjeri_main.txt", "w") as f:
    zapis = ""
    for primjer in pripremljeni_primjeri:
        for tocka in primjer[0]:
            zapis += "{};{};".format(tocka[0], tocka[1])
        zapis = zapis[:-1] + "\t"
        for yi in primjer[1]:
            zapis += "{};".format(yi)
        zapis = zapis[:-1] + "\n"
    f.write(zapis)

# IZRADA NEURONSKE MREŽE
'''
oblik = [int(x) for x in input("Odredite oblik mreže: ").split('X')]
while oblik[0] != 2*M or oblik[-1] != len(slova):
    print("Ulazni sloj mora biti veličine 2*M, a izlazni veličine broja klasa.")
    oblik = [int(x) for x in input("Odredite oblik mreže: ").split('X')]
stopa_ucenja = float(input("Odredite stopu učenja: "))
max_iter = int(input("Odredite maksimalan broj iteracija: "))
alg = input("Odredite algoritam optimizacije: ")
nn = NN.NeuronskaMreza(*oblik)
X,y=NN.raspakiraj('oznaceni_primjeri_main.txt')
nn.fit(X,y,stopa_ucenja,max_iter,alg)
'''

nn = NN.NeuronskaMreza(100, 6, 5)
X, y = NN.raspakiraj('oznaceni_primjeri_main.txt')
nn.fit(X, y, 0.1, 150)


# PREDVIĐANJA

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
