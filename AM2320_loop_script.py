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
        with open(str((jspath/'demo_bot').absolute()), 'r') as f2:
            while True:
                line = f2.readline()
                if not line:
                    break
                fw.write(line)
    os.rename(str((jspath/'demo_temp.js').absolute()), str((jspath/'demo.js').absolute()))

def generateIndexFile(base_path, msg):
    htmlpath = base_path / "apps/templates/home"
    with open(str((htmlpath/'index_temp').absolute()), 'w') as fw:
        with open(str((htmlpath/'index_top').absolute()), 'r') as f1:
            while True:
                line = f1.readline()
                if not line:
                    break
                fw.write(line)
        fw.write('\n')

        fw.write(f'<h4> {msg}</h4>\n')

        fw.write('\n')
        with open(str((htmlpath/'index_bot').absolute()), 'r') as f2:
            while True:
                line = f2.readline()
                if not line:
                    break
                fw.write(line)
    os.rename(str((htmlpath/'index_temp').absolute()), str((htmlpath/'index.html').absolute()))


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
            print(f'{time.ctime()} : temp : {temp} humd : {humd}')
            break
        except:
            continue

    generateJSFile(Path('/home/pi/VCF/Rat'), arr_temp, arr_humd)
    generateIndexFile(Path('/home/pi/VCF/Rat'), f'Last updated : {time.ctime()}<br> Temp : {arr_temp[-1]}Deg Humd : {arr_humd[-1]}%')
    time.sleep(30)
	
