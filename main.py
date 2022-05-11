import numpy as np
def Initial_Conditions():
    vertexes = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8])
    matr = np.array([[0, 1, 1, 1, 2, 2, 0, 1, 1], #0
                    [1, 0, 1, 1, 0, 1, 1, 0, 0], #1
                    [1, 1, 0, 0, 0, 0, 1, 0, 2], #2
                    [1, 1, 0, 0, 1, 0, 0, 0, 0], #3
                    [2, 0, 0, 1, 0, 1, 0, 0, 0], #4
                    [2, 1, 0, 0, 1, 0, 0, 0, 0], #5
                    [0, 1, 1, 0, 0, 0, 0, 1, 0], #6
                    [1, 0, 0, 0, 0, 0, 1, 0, 1], #7
                    [1, 0, 2, 0, 0, 0, 0, 1, 0]]) #8
    iter = 1
    allVertexes = []
    Print_Matrix(matr, vertexes, iter, allVertexes)

def Print_Matrix (matr, vertexes, iter, allVertexes):
    print("\n\t\tІтерація №", iter)
    Print_Graph(vertexes)
    print("\tМатриця зв'язності має вигляд:")
    print(vertexes)
    print("___________________________")

    for i in matr:
        print(i)
    allVertexes.append(vertexes.tolist())
    Average_Length_For_Each_Vertex(vertexes, matr, iter, allVertexes)

def Print_Graph (vertexes):
    mat = []
    while vertexes.any():
        mat.append(vertexes[:3])
        vertexes = vertexes[3:]
    print("\tТочки графа мають розташування:")
    for i in mat:
        print(i)


def Average_Length_For_Each_Vertex(vertexes, matr, iter, allVertexes):
    print("\tCередні довжини ребер для кожної вершини графа")
    L = []
    L_G = []
    width = len(matr)

    for i in range(width):
        sum = 0
        L.append(0)
        L_G.append(0)
        #print("\t i - ", i)
        for j in range(width):
            sum += matr[i][j]
            d = Dij(i, j)
            dr = d * matr[i][j]
            #print(dr, "=", d, "*", matr[i][j])
            L_G[i] += dr
            if j == 8:
                L[i] = L_G[i] / sum
                L[i] = round(L[i], 2)
    #print(L_G)
    print(L)

    max = 0
    maxi = 0
    sum = 0
    for i in range(width):
        sum += L_G[i]
        if L[i] >= max:
            max = L[i]
            maxi = vertexes[i]
    print("\tСумарна довжина ребер: ", sum / 2)

    ifend = True
    for i in range(width):
        if L[i] >= 2:
            ifend = False
            break

    if ifend == True:
        print("\t\tВсі L < 2. Кінець.")
    else:
        Gravity_Center(max, maxi, matr, vertexes, L, iter, allVertexes)

def Gravity_Center(max, maxi, matr, vertexes, L, iter, allVertexes):
    conections = []
    sum = 0
    count = 0
    lineInMatr = np.take(vertexes, maxi) #vertexes.index(maxi)
    for i in matr[lineInMatr]:
        sum += i
        if i != 0:
            conections.append(count)
        count += 1
    #print(lineInMatr, conections)

    length = len(conections)
    S = 0
    t = 0
    for i in range(length):
        if conections[i] == 0 or conections[i] == 3 or conections[i] == 6:
            S += 1
        elif conections[i] == 1 or conections[i] == 4 or conections[i] == 7:
            S += 2
        else:
            S += 3

        if conections[i] <= 2:
            t += 3
        elif 3 <= conections[i] <= 5:
            t += 2
        else:
            t += 1
    S = round(S/sum, 2)
    t = round(t/sum, 2)
    Vertexes_In_Gravity_Centre(S, t, True, max, maxi, matr, vertexes, L, iter, allVertexes)

def Vertexes_In_Gravity_Centre(S, t, first, max, maxi, matr, vertexes, L, iter, allVertexes):
    if first == True:
        changeVertexesIndexes = VertexIndexesCircle1(S, t)
    else:
        changeVertexesIndexes = VertexIndexesCircle2(S, t)

    changeVertexesIndexes.sort()
    changeVertexes = []
    for i in changeVertexesIndexes:
        changeVertexes.append(vertexes[i])
    if first == True:
        print("\tВ коло радіуса 1 з центром", S, t, "потрапили вершини:")
    else:
        print("\tВ коло радіуса 2 з центром", S, t, "потрапили вершини:")
    print(changeVertexes)
    Сonditional_Permutation(changeVertexesIndexes, changeVertexes, max, maxi, matr, vertexes, L, iter, allVertexes, S, t, first)

def Сonditional_Permutation(changeVertexesIndexes, changeVertexes, max, maxi, matr, vertexes, L, iter, allVertexes, S, t, first):
    Lф = []
    # d = []
    r = []
    sumr = 0

    x = vertexes.tolist().index(maxi)
    for i in changeVertexesIndexes:
        r.append(matr[x][i])
        sumr += matr[x][i]
    #print("r - ", r)

    length = len(changeVertexes)
    for i in range(length):
        sumdr = 0
        for j in range(length):
            if i == j:
                d = Dij(changeVertexesIndexes[i], x)
            else:
                d = Dij(changeVertexesIndexes[i], changeVertexesIndexes[j])
            dr = d * r[j]
            #print(dr, "=", d, "*", r[j])
            sumdr += dr
        #print(sumdr, sumr)
        if sumr == 0:
            Lф.append(sumdr)
        else:
            Lф.append(round(sumdr/sumr, 2))
    print("\tЗначення середньої довжини ребер вершини", maxi, "при умовному розміщенні в сітці:")
    print(Lф)
#############################
    σq = []
    σф = []
    δ = []
    for i in range(length):
        σq.append(round(Lф[i] - L[changeVertexesIndexes[i]], 2))
        σф.append(round(L[x] - Lф[i], 2))
        δ.append(round(σф[i] + σq[i], 2))
    #print("σф", σф)
    print("\tАлгебраїчна сума, що необхідна для визначення які вершини слід переставляти:")
    print(δ)

    # print("\t", allVertexes, "allVertexes")

    for i in range(length):
        max = 0
        maxδ = ""
        for j in range(length):
            if δ[j] >= max:
                max = δ[j]
                maxδ = changeVertexes[j]
            #print(max, "= max,", δ[j], ": δ[", j, "]")
        # print(" i ", i, "tochky", maxi, maxδ)
        # print("*vertexes*", vertexes)
        checkVertexes = Change_Vertexes(vertexes, maxi, maxδ)
        #print("\t", checkVertexes, "checkVertexes")
        if allVertexes != []:
            for j in range(iter-1):
                na = np.array(allVertexes[j])
                #print(j, "\t", na, "j")
                if np.array_equiv(na, checkVertexes):
                    #print(checkVertexes, "checkVertexes")
                    #print(j, "\t", na, "j")
                    print("\tМаксимальне δ = ", max, "відповідає парі вершин", maxi, "i", maxδ,
                            "однак відбулось зациклення, тому оберемо іншу вершину")
                    δ.remove(max)
                    changeVertexes.remove(maxδ)
                    length -= 1
                    break
        Change_Vertexes(vertexes, maxi, maxδ)
        # print("**end**")

    ifend = []
    # print("\t\t if end: ", ifend)
    for i in range(length):
        ifend.append(0)
        if δ[i] > 0:
            ifend[i] = False
        else:
            ifend[i] = True

    if False in ifend:
        print("\tМаксимальне δ = ", max, "відповідає парі вершин", maxi, "i", maxδ)
        Change_Matrix(matr, vertexes, allVertexes, maxi, maxδ, iter)
    else:
        if first == True:
            print()
            print("\tВсі δ <= 0, тому необхідно збільшити радіус кола")
            Vertexes_In_Gravity_Centre(S, t, False, max, maxi, matr, vertexes, L, iter, allVertexes)
        else:
            print()
            print("\tОберемо інакшу точку для центру ваги")
            L2 = L
            L2.sort()
            max = L2[-2]
            maxi = L.index(max)
            Gravity_Center(max, maxi, matr, vertexes, L, iter, allVertexes)


def Change_Matrix(matr, vertexes, allVertexes, maxi, maxδ, iter):
    #allVertexes.append(vertexes)
    length = len(vertexes)
    vertexes = Change_Vertexes(vertexes, maxi, maxδ)
    #print(maxδ, "before")
    point1 = vertexes.tolist().index(maxδ)
    point2 = vertexes.tolist().index(maxi)
    #print(maxδ, "= vertexes.tolist().index(maxδ)", )
    #print(maxi, "maxi")

    for i in range(length):
        matr[i][point2], matr[i][point1] = matr[i][point1], matr[i][point2]
    matr[[point2, point1]] = matr[[point1, point2]]

    iter += 1
    Print_Matrix(matr, vertexes, iter, allVertexes)
    # return matr, allVertexes

def Change_Vertexes(vertexes, maxi, maxδ):
    point1 = vertexes.tolist().index(maxδ)
    point2 = vertexes.tolist().index(maxi)
    vertexes[point2], vertexes[point1] = vertexes[point1], vertexes[point2]
    # print("################\nCHANGE_VERTEXES", maxi, ",", maxδ, ":", vertexes, "\n################")
    return vertexes

def Dij (i, j):
    if i == 0 or i == 3 or i == 6:
        xi = 1
    elif i == 1 or i == 4 or i == 7:
        xi = 2
    else:
        xi = 3

    if j == 0 or j == 3 or j == 6:
        xj = 1
    elif j == 1 or j == 4 or j == 7:
        xj = 2
    else:
        xj = 3

    if i <= 2:
        yi = 3
    elif 3 <= i <= 5:
        yi = 2
    else:
        yi = 1

    if j <= 2:
        yj = 3
    elif 3 <= j <= 5:
        yj = 2
    else:
        yj = 1

    d = abs(xi - xj) + abs(yi - yj)
    #print("d", i, j, " = ", d)
    return d

def VertexIndexesCircle1(S, t):
    changeVertexesIndexes = []
    if 0 < S <= 0.5:
        if 0 < t <= 0.5:
            changeVertexesIndexes.append(6)
        elif 0.5 < t < 1.5:
            changeVertexesIndexes.append(6)
            changeVertexesIndexes.append(3)
        elif t == 1.5:
            changeVertexesIndexes.append(3)
        elif 1.5 < t < 2.5:
            changeVertexesIndexes.append(3)
            changeVertexesIndexes.append(0)
        elif t >= 2.5:
            changeVertexesIndexes.append(0)
    elif 0.5 < S < 1.5:
        if 0 < t <= 0.5:
            changeVertexesIndexes.append(6)
            changeVertexesIndexes.append(7)
        elif 0.5 < t < 1.5:
            changeVertexesIndexes.append(6)
            changeVertexesIndexes.append(7)
            changeVertexesIndexes.append(3)
            changeVertexesIndexes.append(4)
        elif t == 1.5:
            changeVertexesIndexes.append(3)
            changeVertexesIndexes.append(4)
        elif 1.5 < t < 2.5:
            changeVertexesIndexes.append(3)
            changeVertexesIndexes.append(0)
            changeVertexesIndexes.append(4)
            changeVertexesIndexes.append(1)
        elif t >= 2.5:
            changeVertexesIndexes.append(0)
            changeVertexesIndexes.append(1)
    elif S == 1.5:
        if 0 < t <= 0.5:
            changeVertexesIndexes.append(7)
        elif 0.5 < t < 1.5:
            changeVertexesIndexes.append(7)
            changeVertexesIndexes.append(4)
        elif t == 1.5:
            changeVertexesIndexes.append(4)
        elif 1.5 < t < 2.5:
            changeVertexesIndexes.append(4)
            changeVertexesIndexes.append(1)
        elif t >= 2.5:
            changeVertexesIndexes.append(1)
    elif 1.5 < S < 2.5:
        if 0 < t <= 0.5:
            changeVertexesIndexes.append(7)
            changeVertexesIndexes.append(8)
        elif 0.5 < t < 1.5:
            changeVertexesIndexes.append(7)
            changeVertexesIndexes.append(8)
            changeVertexesIndexes.append(4)
            changeVertexesIndexes.append(5)
        elif t == 1.5:
            changeVertexesIndexes.append(4)
            changeVertexesIndexes.append(5)
        elif 1.5 < t < 2.5:
            changeVertexesIndexes.append(4)
            changeVertexesIndexes.append(1)
            changeVertexesIndexes.append(5)
            changeVertexesIndexes.append(2)
        elif t >= 2.5:
            changeVertexesIndexes.append(1)
            changeVertexesIndexes.append(2)
    elif S >= 2.5:
        if 0 < t <= 0.5:
            changeVertexesIndexes.append(8)
        elif 0.5 < t < 1.5:
            changeVertexesIndexes.append(8)
            changeVertexesIndexes.append(5)
        elif t == 1.5:
            changeVertexesIndexes.append(5)
        elif 1.5 < t < 2.5:
            changeVertexesIndexes.append(5)
            changeVertexesIndexes.append(2)
        elif t >= 2.5:
            changeVertexesIndexes.append(2)
    return changeVertexesIndexes

def VertexIndexesCircle2(S, t):
    changeVertexesIndexes = []
    if 0 < S <= 1:
        if 0 < t <= 1:
            changeVertexesIndexes.append(3)
            changeVertexesIndexes.append(4)
            changeVertexesIndexes.append(6)
            changeVertexesIndexes.append(7)
        elif 1 < t < 2:
            changeVertexesIndexes.append(0)
            changeVertexesIndexes.append(1)
            changeVertexesIndexes.append(3)
            changeVertexesIndexes.append(4)
            changeVertexesIndexes.append(6)
            changeVertexesIndexes.append(7)
        elif t >= 2:
            changeVertexesIndexes.append(0)
            changeVertexesIndexes.append(1)
            changeVertexesIndexes.append(3)
            changeVertexesIndexes.append(4)
    elif 1 < S < 2:
        if 0 < t <= 1:
            changeVertexesIndexes.append(6)
            changeVertexesIndexes.append(3)
            changeVertexesIndexes.append(4)
            changeVertexesIndexes.append(5)
            changeVertexesIndexes.append(8)
            changeVertexesIndexes.append(7)
        elif 1 < t < 2:
            changeVertexesIndexes.append(1)
            changeVertexesIndexes.append(2)
            changeVertexesIndexes.append(4)
            changeVertexesIndexes.append(5)
            changeVertexesIndexes.append(7)
            changeVertexesIndexes.append(8)
        elif t >= 2:
            changeVertexesIndexes.append(0)
            changeVertexesIndexes.append(1)
            changeVertexesIndexes.append(2)
            changeVertexesIndexes.append(5)
            changeVertexesIndexes.append(4)
            changeVertexesIndexes.append(3)
    elif S >= 2:
        if 0 < t <= 1:
            changeVertexesIndexes.append(5)
            changeVertexesIndexes.append(4)
            changeVertexesIndexes.append(8)
            changeVertexesIndexes.append(7)
        if 1 < t < 2:
            changeVertexesIndexes.append(2)
            changeVertexesIndexes.append(1)
            changeVertexesIndexes.append(5)
            changeVertexesIndexes.append(4)
            changeVertexesIndexes.append(8)
            changeVertexesIndexes.append(7)
        elif t >= 2:
            changeVertexesIndexes.append(2)
            changeVertexesIndexes.append(1)
            changeVertexesIndexes.append(5)
            changeVertexesIndexes.append(4)
    return changeVertexesIndexes

#####################

Initial_Conditions()