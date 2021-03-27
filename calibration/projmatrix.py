import numpy as np


# Нахождение компонент проекционной матрицы методом наименьших квадратов

# Входные параметры:
#   JP = 3xM матрица - 3D-координаты точек калибровочного объекта
#       в собственной системе координат объекта (J), столбцы матрицы
#       соответствуют векторам JPi
#   Ip = 2xM матрица - 2D-координаты изображений точек JPi калибровочного
#       объекта в системе координат цифрового изображения (I)

# Выходные параметры:
#   projmatrix = 3x4 матрица - проекционная матрица камеры
from calc import calc_residual


def eval_projmatrix(JP, Ip):
    # Проверяем размерности входных данных(в случае ошибки возвращаем нулевую проекционную матрицу)
    M = JP.shape[1]
    if M != Ip.shape[1]:
        # todo: вывод ошибки в интерфейс
        return np.zeros((3, 4))

    if M < 6:
        # todo: вывод ошибки в интерфейс
        return np.zeros((3, 4))

    if JP.shape[0] != 3 or Ip.shape[0] != 2:
        # todo: вывод ошибки в интерфейс
        return np.zeros((3, 4))

    # Из исходных данных формируем матрицу Q(формула(28))
    Q = np.zeros((2 * M, 12))

    q1 = np.zeros((2, 12))  # пара строк в Q, соответствующих одной точке объекта

    for i in range(M):
        q1[0, :] = [JP[0, i], JP[1, i], JP[2, i], 1, 0, 0, 0, 0, - Ip[0, i] * JP[0, i], - Ip[0, i] * JP[1, i],
                    - Ip[0, i] * JP[2, i], - Ip[0, i]]
        q1[1, :] = [0, 0, 0, 0, JP[0, i], JP[1, i], JP[2, i], 1, - Ip[1, i] * JP[0, i], - Ip[1, i] * JP[1, i],
                    - Ip[1, i] * JP[2, i], - Ip[1, i]]

        x = (2 * (i - 1)) + 2
        y = 2 * i + 2
        Q[x:y, :] = q1

    # Решаем систему уравнений Q * m = 0(уравнение(28)) линейным методом наименьших квадратов:

    # 1.Выполнили сингулярное разложение
    [U, W, V] = np.linalg.svd(Q)

    # 2. Столбцы матрицы V представляют собой возможные решение
    # (но нас интересует только соответствующее минимальному и не равному 0 сингулярному значению, выбор которого при
    # наличии шума осуществить достаточно трудно - для этого
    # будем искать решение, которое даст наилучшее приближение
    # исходных данных Ip)

    NS = V.shape[1]  # количество решений

    # перебираем все возможные и ищем то, которое даст минимальную ошибку

    best_i = 0
    best_m = V[best_i, :]
    best_projmatrix = form_projmatrix(best_m)
    best_Ip = projection(JP, best_projmatrix)
    best_err = calc_residual(Ip, best_Ip)


    if NS > 1:
        for i in range(NS):
            if W[i] > 0:
                i_m = V[i, :]
                i_projmatrix = form_projmatrix(i_m)
                i_Ip = projection(JP, i_projmatrix)
                i_err = calc_residual(Ip, i_Ip)

                if i_err < best_err:
                    best_i = i
                    best_projmatrix = i_projmatrix
                    best_err = i_err

    return best_projmatrix


# [projmatrix] = form_projmatrix(m)
#
# формируем проекционную матрицу из найденного вектора m
#
def form_projmatrix(m):
    a = 0
    projmatrix = np.zeros((3, 4))
    for i in range(3):
        for j in range(4):
            projmatrix[i, j] = m[a]
            a += 1
    return projmatrix


#  [Ip] = projection(JP,projmatrix)
#  
#  Вычисление координат изображений точек объекта в соответствии
#  с преобразованием (J)->(I) (формула (26))
# 
#  Входные параметры:
#    JP = 3xM матрица - 3D-координаты точек калибровочного объекта
#        в собственной системе координат объекта (J), столбцы матрицы
#        соответствуют векторам JPi
#    projmatrix = 3x4 матрица - проекционная матрица камеры
# 
#  Выходные параметры:
#    Ip = 2xM матрица - 2D-координаты изображений точек JPi калибровочного
#        объекта в системе координат цифрового изображения (I)
# 
def projection(JP, projmatrix):
    M = JP.shape[1]

    # Проверка размерности матрицы данных JP
    if JP.shape[0] != 3 or M < 1:
        raise Exception("error in projection() : invalid size of JP!")

    Ip = np.zeros((2, M))  # сразу же выделяем место

    # Проверка размерности проекционной матрицы
    if projmatrix.shape[0] != 3 or projmatrix.shape[1] != 4:
        raise Exception("error in projection() : invalid size of projmatrix!")

    # В цикле заполняем Ip
    for i in range(M):
        JPi = np.append(JP[:, i], 1)  # делаем 4D-вектор из 3D-вектора
        Czi = np.multiply(projmatrix[2, :], JPi).sum(axis=0)

        Ip[0, i] = np.multiply(projmatrix[0, :], JPi).sum(axis=0) / Czi  # (формула (26))
        Ip[1, i] = np.multiply(projmatrix[1, :], JPi).sum(axis=0) / Czi

    return Ip