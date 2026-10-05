import numpy as np
from tqdm import tqdm
from pathlib import Path

from scripts.read_txt_file import read_txt_xy
from scripts.plot_xy import plot_xy_markers
from scripts.write_data_txt import write_txt_xy
from scripts.get_formated_time import get_formatted_time
LINEWIDTHS = [2,3,1]

WAVELENGTH_START = 1056
WAVELENGTH_STOP = 1071  # Последний элемент не включается
WAVELENGTH_STEP = 1
WAVELENGTHS = np.arange(WAVELENGTH_START, WAVELENGTH_STOP, WAVELENGTH_STEP)

NUMBER_ITERATIONS=40
MEGA=1e+6
x_label="Iteration (N)"
y_label='Frequency (MHz)'

# Диапазон поиска пика (в МГц)
MAX_FREQ_START = 50
MAX_FREQ_STOP = 1000


CURRENT = 9.95
# # Получаем текущую дату и время
# time_now = get_formatted_time()

# Папка, где лежат данные   




# Формирование имя файлов
filename=f'freq_vs_time'
png_title=f'Current {CURRENT} А'
        
iteration_arr, max_freq_arr = [], []

for iteration in range(1, NUMBER_ITERATIONS+1):
    
    rf_txt_file = Path(rf"C:\Users\namys\Documents\DATA_dual_wavelength_laser\30-September_2026\LD_set_I_9.95A_Sep-30-2026_time_17-05-14\RF_port_1064nm\span_1000.0MHz\RF_{iteration}_span_1000.0MHz.txt")
    DATA_FOLDER=rf_txt_file.parents[2]
    SAVE_FOLDER=rf'{DATA_FOLDER}\Freq_stability'
    freq_arr, pow_arr = read_txt_xy(file_path=rf_txt_file)
    
    
    # ЛОГИКА ОГРАНИЧЕНИЯ ДИАПАЗОНА ПОИСКА
    # Переводим границы поиска из МГц обратно в Гц (как в исходном файле)
    start_hz = MAX_FREQ_START * MEGA
    stop_hz = MAX_FREQ_STOP * MEGA
    
    # Создаем маску: True для элементов, попавших в диапазон
    mask = (freq_arr >= start_hz) & (freq_arr <= stop_hz)
    
    # Проверяем, есть ли вообще точки в этом диапазоне, чтобы не упасть с ошибкой
    if not np.any(mask):
        print(f"\n[Warning] No data points found in range {MAX_FREQ_START}-{MAX_FREQ_STOP} MHz for iteration {iteration}")
        continue
    
    # Фильтруем массивы по маске
    sub_freq = freq_arr[mask]
    sub_pow = pow_arr[mask]
    
    # Ищем пик только внутри обрезанного диапазона мощности
    max_sub_index = np.argmax(sub_pow)
    
    # Берем частоту, соответствующую этому пику
    max_freq = sub_freq[max_sub_index] / MEGA
    
    max_freq_arr.append(max_freq)
    iteration_arr.append(iteration)
    


plot_xy_markers(
    x=iteration_arr, 
    y=max_freq_arr, 
    title=png_title, 
    xlabel=x_label, 
    ylabel=y_label, 
    folder_path=SAVE_FOLDER, 
    filename=filename, 
    show_plot=False
)

write_txt_xy(
    x_arr=iteration_arr,
    x_label=x_label,
    y_arr=max_freq_arr,
    y_label=y_label,
    header=None,
    folder_path=SAVE_FOLDER,
    filename=filename,
)

        
    
        
        
