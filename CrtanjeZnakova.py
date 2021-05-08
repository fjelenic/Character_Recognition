from tkinter import *
import math

MAX_UZORAKA = 20
M = 50


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

with open("oznaceni_primjeri.txt", "w") as f:
    zapis = ""
    for primjer in pripremljeni_primjeri:
        for tocka in primjer[0]:
            zapis += "{};{};".format(tocka[0], tocka[1])
        zapis = zapis[:-1] + "\t"
        for yi in primjer[1]:
            zapis += "{};".format(yi)
        zapis = zapis[:-1] + "\n"
    f.write(zapis)
