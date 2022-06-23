import time
import numpy as np
import warnings
from pathlib import Path
import os
try:
    import board
    import adafruit_am2320
except ImportError:
    warnings.warn('Import Error. Probably not Raspberry Pi?')

def generateJSFile(base_path, temp_array, humd_array):
    jspath = base_path / "apps/static/assets/demo"
    with open(str((jspath/'demo_temp.js').absolute()), 'w') as fw:
        with open(str((jspath/'demo_up').absolute()), 'r') as f1:
            while True:
                line = f1.readline()
                if not line:
                    break
                fw.write(line)
        fw.write('\n')

        fw.write(f'var temp_chart_data = {str(temp_array.tolist())};\n')
        fw.write(f'var humd_chart_data = {str(humd_array.tolist())};\n')

        fw.write('\n')
        with open(str((jspath/'demo_dot').absolute()), 'r') as f2:
            while True:
                line = f2.readline()
                if not line:
                    break
                fw.write(line)
    os.rename(str((jspath/'demo_temp.js').absolute()), str((jspath/'demo.js').absolute()))


i2c = board.I2C()
sensor = adafruit_am2320.AM2320(i2c)

arr_temp = np.array([25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25])
arr_humd = np.array([50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50])

while True:
    for i in range(10):
        try:
            temp = sensor.temperature
            humd = sensor.relative_humidity
            arr_temp = np.delete(arr_temp, 0)
            arr_temp = np.append(arr_temp, temp)
            arr_humd = np.delete(arr_humd, 0)
            arr_humd = np.append(arr_humd, humd)
            break
        except:
            continue

    time.sleep(30)
    generateJSFile(Path('.'), arr_temp, arr_humd)
	
