from projmatrix import eval_projmatrix, projection
from util import file_folder_util as ut
from calc import calc_params, calc_calmatrix, calc_projmatrix

# ФОТОГРАММЕТРИЧЕСКАЯ КАЛИБРОВКА КАМЕРЫ (БЕЗ УЧЁТА РАДИАЛЬНЫХ ИСКАЖЕНИЙ)
# Главный скрипт.
if __name__ == '__main__':
    # Имя папки для хранения входных и выходных данных
    dirname = 'serj'

    # Имена входных и выходных файлов
    fname_obj_calpts = 'input/obj_calpts.txt'

    fname_cam1_img_calpts = 'input/cam1_img_calpts.txt'
    fname_cam1_projmatrix = 'output/cam1_projmatrix.txt'
    fname_cam1_params = 'output/cam1_params.txt'

    fname_cam2_img_calpts = 'input/cam2_img_calpts.txt'
    fname_cam2_projmatrix = 'output/cam2_projmatrix.txt'
    fname_cam2_params = 'output/cam2_params.txt'

    # Загружаем данные из файлов
    JP = ut.read_file(fname_obj_calpts, 3)
    cam1_Ip = ut.read_file(fname_cam1_img_calpts, 2)
    cam2_Ip = ut.read_file(fname_cam2_img_calpts, 2)

    # Определяем компоненты проекционных матриц камер
    cam1_projmatrix = eval_projmatrix(JP, cam1_Ip)
    cam2_projmatrix = eval_projmatrix(JP, cam2_Ip)

    # Вычисляем внутренние и внешние параметры камер
    [cam1_alpha, cam1_beta, cam1_theta, cam1_x0, cam1_y0, cam1_R, cam1_t] = calc_params(cam1_projmatrix)
    [cam2_alpha, cam2_beta, cam2_theta, cam2_x0, cam2_y0, cam2_R, cam2_t] = calc_params(cam2_projmatrix)

    # Сохраняем полученные результаты в файлы
    ut.write_projmatrix(fname_cam1_projmatrix, cam1_projmatrix)
    ut.write_projmatrix(fname_cam2_projmatrix, cam2_projmatrix)

    ut.write_params(fname_cam1_params, cam1_alpha, cam1_beta, cam1_theta, cam1_x0, cam1_y0, cam1_R, cam1_t)
    ut.write_params(fname_cam2_params, cam2_alpha, cam2_beta, cam2_theta, cam2_x0, cam2_y0, cam2_R, cam2_t)

    # todo: Отображаем найденые параметры камеры

    # Для контроля за правильностью определения параметров камеры
    # вычисляем координаты точек объекта на изображении
    # используя найденные параметры и проекционную матрицу
    cam1_Ip2 = projection(JP, cam1_projmatrix)

    cam1_calmatrix3 = calc_calmatrix(cam1_alpha, cam1_beta, cam1_theta, cam1_x0, cam1_y0)
    cam1_projmatrix3 = calc_projmatrix(cam1_calmatrix3, cam1_R, cam1_t)
    cam1_Ip3 = projection(JP, cam1_projmatrix3)
    # todo: нарисовать график matplotlib
    # figure(1);
    # subplot(1,2,1);
    # plot(cam1_Ip(1,:),-cam1_Ip(2,:),'+r',cam1_Ip2(1,:),-cam1_Ip2(2,:),'vb',cam1_Ip3(1,:),-cam1_Ip3(2,:),'^k');
    # title('camera1');
    # legend('experimental','calc with found projmatrix','calc with found parameters');
    #
    #
    cam2_Ip2 = projection(JP, cam2_projmatrix)

    cam2_calmatrix3 = calc_calmatrix(cam2_alpha, cam2_beta, cam2_theta, cam2_x0, cam2_y0)
    cam2_projmatrix3 = calc_projmatrix(cam2_calmatrix3, cam2_R, cam2_t)
    cam2_Ip3 = projection(JP, cam2_projmatrix3)
    # todo: нарисовать график matplotlib
    # figure(1);
    # subplot(1,2,2);
    # plot(cam2_Ip(1,:),-cam2_Ip(2,:),'+r',cam2_Ip2(1,:),-cam2_Ip2(2,:),'vb',cam2_Ip3(1,:),-cam2_Ip3(2,:),'^k');
    # title('camera2');
    # legend('experimental','calc with found projmatrix','calc with found parameters');
    #
    # return;

    print("OK")
