import copy
import math

EPSILON = 10 ** -9


class Matrica:
    def __init__(self, mat):
        self.elementi = mat
        self.oblik = (len(mat), len(mat[0]))

    def __getitem__(self, item):
        return self.elementi[item]

    def __setitem__(self, key, value):
        self.elementi[key] = value

    def __str__(self):
        ispis = "["
        for redak in self.elementi:
            ispis += "["
            for ele in redak:
                ispis += '{:>7.3f}'.format(ele) + " "
            ispis += "]\n "
        ispis = ispis[:-2] + "]"
        return ispis

    def __add__(self, other):
        if not (isinstance(other, Matrica) and self.oblik[0] == other.oblik[0]):
            raise Exception("Matricu je moguće zbrajati samo s drugom matricom iste prve dimenzije.")
        nova_matrica = nulMatrica(*self.oblik)
        for i in range(self.oblik[0]):
            for j in range(self.oblik[1]):
                if other.oblik[1] == self.oblik[1]:
                    nova_matrica[i][j] = self[i][j] + other[i][j]
                elif other.oblik[1] == 1:
                    nova_matrica[i][j] = self[i][j] + other[i][0]
                else:
                    raise Exception("Matricu je moguće zbrajati samo s drugom matricom iste prve dimenzije.")
        return nova_matrica

    def __radd__(self, other):
        return Matrica.__add__(self, other)

    def __sub__(self, other):
        if not (isinstance(other, Matrica) and self.oblik[0] == other.oblik[0]):
            raise Exception("Matricu je moguće oduzimati samo od druge matrice iste prve dimenzije.")
        nova_matrica = nulMatrica(*self.oblik)
        for i in range(self.oblik[0]):
            for j in range(self.oblik[1]):
                if other.oblik[1] == self.oblik[1]:
                    nova_matrica[i][j] = self[i][j] - other[i][j]
                elif other.oblik[1] == 1:
                    nova_matrica[i][j] = self[i][j] - other[i][0]
                else:
                    raise Exception("Matricu je moguće oduzimati samo s drugom matricom iste prve dimenzije.")
        return nova_matrica

    def __rsub__(self, other):
        return Matrica.__sub__(self, other)

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            nova_matrica = nulMatrica(*self.oblik)
            for i in range(self.oblik[0]):
                for j in range(self.oblik[1]):
                    nova_matrica[i][j] = self[i][j] * other
        elif isinstance(other, Matrica) and self.oblik[1] == other.oblik[0]:
            nova_matrica = nulMatrica(self.oblik[0], other.oblik[1])
            for i in range(self.oblik[0]):
                for j in range(other.oblik[1]):
                    for k in range(self.oblik[1]):
                        nova_matrica[i][j] += self[i][k] * other[k][j]
        else:
            raise Exception("Matricu je moguće množiti sa skalarom ili drugom matricom s uvijetom (m X n) * (n X k)")
        return nova_matrica

    def __rmul__(self, other):
        return Matrica.__mul__(self, other)

    def __invert__(self):
        nova_matrica = nulMatrica(self.oblik[1], self.oblik[0])
        for i in range(self.oblik[0]):
            for j in range(self.oblik[1]):
                nova_matrica[j][i] = self[i][j]
        return nova_matrica

    def __eq__(self, other):
        if not isinstance(other, Matrica):
            return False
        return self.elementi == other.elementi

    def invertiraj(self):
        A = copy.deepcopy(self.elementi)
        A = Matrica(A)
        P = LUPDekompozicija(A)
        novi_elementi = []
        for i in range(self.oblik[0]):
            b = ~Matrica([P[i]])
            supstitucijaUnaprijed(A, b)
            supstitucijaUnatrag(A, b)
            b = ~b
            novi_elementi.append(b.elementi[0])
        return ~(P * Matrica(novi_elementi))

    def norma(self):
        norm = 0
        for i in range(self.oblik[0]):
            for j in range(self.oblik[1]):
                norm += self.elementi[i][j] ** 2
        return math.sqrt(norm)

    def determinanta(self):
        A = copy.deepcopy(self.elementi)
        A = Matrica(A)
        _, S = LUPDekompozicija(A, True)
        umnozak = 1
        for i in range(A.oblik[0]):
            umnozak *= A[i][i]
        return (-1) ** S * umnozak

    def zapisiUDatoteku(self, file):
        with open(file, 'w') as f:
            for redak in self.elementi:
                for ele in redak:
                    f.write(str(ele) + " ")
                f.write("\n")

    def ispisiNaZaslon(self):
        print(self)

    def kopiraj(self):
        return copy.deepcopy(self)


def procitajMatricu(file):
    mat = []
    with open(file, 'r') as f:
        for line in f.readlines():
            if line != "\n":
                if line[-1] == "\n":
                    line = line[:-1]
                line = [float(x) for x in line.replace("   ", " ").split(" ")]
                mat.append(line)
    return Matrica(mat)


def nulMatrica(n_redaka, n_stupaca):
    return Matrica([[0 for _ in range(n_stupaca)] for _ in range(n_redaka)])


def jedinicnaMatrica(n):
    I = nulMatrica(n, n)
    for i in range(n):
        I[i][i] = 1
    return I


def supstitucijaUnaprijed(A, b):
    if b.oblik[0] != A.oblik[0] or b.oblik[0] != A.oblik[1]:
        raise Exception("Duljina vektora mora biti jednaka dimenziji kvadratne matrice.")
    if b.oblik[1] != 1:
        raise Exception("Vektor mora biti vektor stupac oblika (n X 1).")
    for i in range(b.oblik[0] - 1):
        for j in range(i + 1, b.oblik[0]):
            b[j][0] -= A[j][i] * b[i][0]


def supstitucijaUnatrag(A, b):
    if b.oblik[0] != A.oblik[0] or b.oblik[0] != A.oblik[1]:
        raise Exception("Duljina vektora mora biti jednaka dimenziji kvadratne matrice.")
    if b.oblik[1] != 1:
        raise Exception("Vektor mora biti vektor stupac oblika (n X 1).")
    for i in range(b.oblik[0] - 1, -1, -1):
        if jeNula(A[i][i]):
            raise ZeroDivisionError("Matrica je singularna.")
        b[i][0] /= A[i][i]
        for j in range(i - 1, -1, -1):
            b[j][0] -= A[j][i] * b[i][0]


def LUDekompozicija(A):
    if A.oblik[0] != A.oblik[1]:
        raise Exception("Matrica mora biti kvadratna.")
    n = A.oblik[0]
    for i in range(n - 1):
        for j in range(i + 1, n):
            if jeNula(A[i][i]):
                raise ZeroDivisionError("LU dekompozicija nije moguća. Pivot je 0.")
            A[j][i] /= A[i][i]
            for k in range(i + 1, n):
                A[j][k] -= A[j][i] * A[i][k]


def LUPDekompozicija(A, broji_permutacije=False):
    if A.oblik[0] != A.oblik[1]:
        raise Exception("Matrica mora biti kvadratna.")
    n = A.oblik[0]
    P = jedinicnaMatrica(n)
    if broji_permutacije:
        brojac = 0
    for i in range(n - 1):
        pivot = odaberiPivot(A, i, i)
        if pivot is None:
            raise Exception("Nepostoji pivot različit od nule. Matrica je singularna.")
        if pivot != i:
            zamjeniRetke(A, i, pivot)
            zamjeniRetke(P, i, pivot)
            if broji_permutacije:
                brojac += 1
        for j in range(i + 1, n):
            A[j][i] /= A[i][i]
            for k in range(i + 1, n):
                A[j][k] -= A[j][i] * A[i][k]
    if broji_permutacije:
        return P, brojac
    return P


def dekompozicija(A, pivotiranje=True):
    if pivotiranje:
        return LUPDekompozicija(A)
    else:
        LUDekompozicija(A)


def odaberiPivot(A, i, j):
    najveci_element = 0
    najveci_indeks = None
    for k in range(i, A.oblik[0]):
        if jeNula(A[k][j]):
            continue
        if najveci_indeks is None or abs(A[k][j]) > najveci_element:
            najveci_element = abs(A[k][j])
            najveci_indeks = k
    return najveci_indeks


def zamjeniRetke(A, i, j):
    temp = A[i]
    A[i] = A[j]
    A[j] = temp


def jeNula(n):
    return abs(n) < EPSILON


def rijesiSustav(A, b, pivotiranje=True):
    if pivotiranje:
        P = dekompozicija(A, pivotiranje)
        b = P * b
    else:
        dekompozicija(A, pivotiranje)
    supstitucijaUnaprijed(A, b)
    supstitucijaUnatrag(A, b)
    return b


def postaviEpsilon(vrijednost=10 ** -9):
    global EPSILON
    EPSILON = vrijednost
