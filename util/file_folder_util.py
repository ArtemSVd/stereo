import numpy as np


# Вычитывание координат точек калибровочного объекта из файла с заданным именем

#  Входные параметры:
#   filename = строка - имя файла
#   X = число - количество координат

# Выходные параметры (при X = 3):
#  JP = 3xM матрица - 3D - координаты точек калибровочного объекта
#  в собственной системе координат объекта(J), столбцы матрицы  соответствуют векторам JPi

# Выходные параметры (при Х = 2):
#   Ip = 2xM матрица - 2 D - координаты изображений точек JPi калибровочного объекта
# в системе координат цифрового изображения(I)

def read_file(filename, X):
    # открываем файл для чтения
    fid = open(filename, 'r')
    # todo: проверка файла на существование и вывод ошибки

    # вычитываем M
    M = np.loadtxt(fid, max_rows=1)

    # todo: обработка ошибок чтения файла

    # проверка значения M
    if M < 1:
        print("invalid M !")
        fid.close()
        return np.array([])

    # вычитываем JPi
    matrix = np.loadtxt(fid, unpack=True)

    if matrix.size != X * M:
        print("error in read_JP() : can not read JP !")
        fid.close()
        return np.array([])

    fid.close()
    return matrix


#  Запись проекционной матрицы камеры в файл с заданным именем
#
#  Входные параметры:
#    filename = строка - имя файла
#    projmatrix = 3x4 матрица - проекционная матрица камеры
#
def write_projmatrix(filename, projmatrix):
    # запись projmatrix
    np.savetxt(filename, projmatrix, fmt='%4.6e', delimiter='     ')


#  Запись внутренних и внешних параметров камеры в файл с заданным именем
# 
#  Входные параметры:
#    filename = строка - имя файла
#    alpha = число - отношение fF/sx (отношение фокусного расстояния к
#        горизонтальному размеру пиксела фотоматрицы камеры)
#    beta = число - отношение fF/sy (отношение фокусного расстояния к
#        вертикальному размеру пиксела фотоматрицы камеры)
#    theta = число - угол, определяющий непрямоугольность пиксела
#        фотоматрицы
#    x0 = число - положение начала координат физического изображения
#        в системе координат цифрового изображения IxOL
#    y0 = число - положение начала координат физического изображения
#        в системе координат цифрового изображения IyOL
#    R = 3x3 матрица - матрица CJR поворота преобразования координат (J)->(C)
#    t = 3x1 вектор - вектор смещения преобразования координат (J)->(C)
# 
def write_params(filename, alpha, beta, theta, x0, y0, R, t):
    fid = open(filename, 'w')
    # todo: проверка файла на существование и вывод ошибки

    np.savetxt(fid, t, delimiter='     ', fmt='%4.6e', header='T', footer='\n', comments='')

    np.savetxt(fid, R, delimiter='     ', fmt='%4.6e', header='R', footer='\n', comments='')

    np.savetxt(fid, np.array([alpha]), fmt='%4.6e', header='alpha', footer='\n', comments='')

    np.savetxt(fid, np.array([beta]), fmt='%4.6e', header='beta', footer='\n', comments='')

    np.savetxt(fid, np.array([theta]), fmt='%4.6e', header='theta', footer='\n', comments='')

    np.savetxt(fid, np.array([x0]), fmt='%4.6e', header='x0', footer='\n', comments='')

    np.savetxt(fid, np.array([y0]), fmt='%4.6e', header='y0', footer='\n', comments='')

    fid.close()
