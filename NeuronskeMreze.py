from matrica import *
import random


def dekodiraj_predvidjanje(y):
    max = 0
    for i in range(1, y.oblik[0]):
        if y[i][0] > y[max][0]:
            max = i
    return max


def raspakiraj(file):
    with open(file, 'r') as f:
        X = []
        y = []
        for line in f.readlines():
            if line != '\n':
                line_X, line_y = line[:-1].split('\t')
                X.append([float(x) for x in line_X.split(';')])
                y.append([float(x) for x in line_y.split(';')])
        return Matrica(X), Matrica(y)


def sigmoid(X):
    Y = X.kopiraj()
    for i in range(X.oblik[0]):
        for j in range(X.oblik[1]):
            Y[i][j] = 1 / (1 + math.exp(-X[i][j]))
    return Y


def mnozenje_po_parovima(X, Y):
    Z = X.kopiraj()
    for i in range(X.oblik[0]):
        for j in range(X.oblik[1]):
            Z[i][j] = X[i][j] * Y[i][j]
    return Z


def jedan_minus(X):
    Z = X.kopiraj()
    for i in range(X.oblik[0]):
        for j in range(X.oblik[1]):
            Z[i][j] = 1 - X[i][j]
    return Z


def stisni_horizontalno(X):
    Z = []
    for i in range(X.oblik[0]):
        Z.append([sum(X[i])])
    return Matrica(Z)


class NeuronskaMreza:

    def __init__(self, *args):
        self.W = []
        for i in range(len((args)) - 1):
            mat = []
            for j in range(args[i + 1]):
                mat.append([])
                for k in range(args[i]):
                    mat[j].append(random.uniform(0, 1))
            self.W.append(Matrica(mat))
        self.b = []
        for dim in args[1:]:
            theta = []
            for i in range(dim):
                theta.append(random.uniform(0, 1))
            self.b.append(~Matrica([theta]))

    def predict(self, X):
        self.A = []
        self.A.append((~X).kopiraj())
        for l in range(len(self.W) - 1):
            Z = self.W[l] * self.A[l]
            Z = Z + self.b[l]
            self.A.append(sigmoid(Z))
        Z = self.W[-1] * self.A[-1] + self.b[-1]
        self.A.append(sigmoid(Z))
        return self.A[-1]

    def backprop(self, y):
        dA = [None for _ in range(len(self.W))]
        dZ = [None for _ in range(len(self.W))]
        self.dW = [None for _ in range(len(self.W))]
        self.db = [None for _ in range(len(self.W))]
        dA[-1] = self.A[-1] - y
        dZ[-1] = mnozenje_po_parovima(dA[-1], self.A[-1])
        dZ[-1] = mnozenje_po_parovima(dZ[-1], jedan_minus(self.A[-1]))
        self.dW[-1] = dZ[-1] * ~self.A[-2]
        self.db[-1] = stisni_horizontalno(dZ[-1])
        dA[-2] = ~self.W[-1] * dZ[-1]
        for l in range(2, len(self.W) + 1):
            dZ[-l] = mnozenje_po_parovima(dA[-l], self.A[-l])
            dZ[-l] = mnozenje_po_parovima(dZ[-l], jedan_minus(self.A[-l]))
            self.dW[-l] = dZ[-l] * ~self.A[-l - 1]
            self.db[-l] = stisni_horizontalno(dZ[-l])
            if l < len(self.W):
                dA[-l - 1] = ~self.W[-l] * dZ[-l]

    def update(self, alpha):
        for i in range(len(self.W)):
            self.W[i] = self.W[i] - alpha * self.dW[i]
            self.b[i] = self.b[i] - alpha * self.db[i]

    def error(self, h, y):
        diff = h - y
        err = 0
        for i in range(diff.oblik[0]):
            for j in range(diff.oblik[1]):
                err += diff[i][j] ** 2
        return err / (diff.oblik[0] * diff.oblik[1])

    def fit(self, X, y, learning_rate=0.01, max_iter=10000, alg="Backpropagation"):
        if alg == "Backpropagation":
            y = ~y
            for i in range(max_iter):
                h = self.predict(X)
                if i % 10 == 0:
                    print("Pogreška u {}. iteraciji => {}".format(i, self.error(h, y)))
                self.backprop(y)
                self.update(learning_rate)
            print("KRAJ => {}\n".format(self.error(h, y)))
        if alg == "Stohastic Backpropagation":
            for i in range(max_iter):
                if i % 10 == 0:
                    h = self.predict(X)
                    print("Pogreška u {}. iteraciji => {}".format(i, self.error(h, ~y)))
                redosljed = list(range(X.oblik[0]))
                random.shuffle(redosljed)
                for j in redosljed:
                    _ = self.predict(Matrica([X[j]]))
                    self.backprop(~Matrica([y[j]]))
                    self.update(learning_rate)
            h = self.predict(X)
            print("KRAJ => {}\n".format(self.error(h, ~y)))
        if alg == "Mini-batch Backpropagation":
            n_kategorija = len(y[0])
            n_primjera = int(len(y.elementi) / n_kategorija)
            for i in range(max_iter):
                if i % 10 == 0:
                    h = self.predict(X)
                    print("Pogreška u {}. iteraciji => {}".format(i, self.error(h, ~y)))
                for j in range(0, n_primjera, 2):
                    batch_X = []
                    batch_y = []
                    for k in range(n_kategorija):
                        batch_X.append(X[j + k * n_primjera])
                        batch_X.append(X[j + k * n_primjera + 1])
                        batch_y.append(y[j + k * n_primjera])
                        batch_y.append(y[j + k * n_primjera + 1])
                    _ = self.predict(Matrica(batch_X))
                    self.backprop(~Matrica(batch_y))
                    self.update(learning_rate)
            h = self.predict(X)
            print("KRAJ => {}\n".format(self.error(h, ~y)))


class EvolucijskaNeuronskaMreza:

    def __init__(self, *args):
        self.model = args
        n_parametara = args[0] * args[1] * 2
        for i in range(2, len(args)):
            n_parametara += args[i] * (args[i - 1] + 1)
        self.n_parametara = n_parametara

    def sig(self, x):
        return 1 / (1 + math.exp(-x))

    def calcOutput(self, parametri, X):
        rez = []
        for x in X:
            p = 0
            temp_rez = x[:]
            for i in range(self.model[1]):
                suma = 0
                for k in range(self.model[0]):
                    slicnost = abs(temp_rez[k] - parametri[p])
                    p += 1
                    slicnost /= abs(parametri[p])
                    p += 1
                    suma += slicnost
                y = 1 / (1 + suma)
                temp_rez.append(y)
            for k, n in enumerate(self.model[2:]):
                odmak = sum(self.model[:k + 1])
                for i in range(n):
                    y = parametri[p]
                    p += 1
                    for j in range(self.model[k + 1]):
                        y += temp_rez[odmak + j] * parametri[p]
                        p += 1
                    temp_rez.append(self.sig(y))
            rez.append(temp_rez[-self.model[-1]:])
        return rez

    def calcError(self, parametri, X, y):
        pred = self.calcOutput(parametri, X)
        error = 0
        for i in range(len(y)):
            for j in range(len(y[i])):
                error += (pred[i][j] - y[i][j]) ** 2
        return error / len(y)
