import json
import os.path
import platform

import traceback
from tkinter import Tk, Label, ttk
from tkinter.messagebox import showerror, askyesno
from plugins.core.mod import SConfig, decrypt, SNConfig, encrypt, get_win, generate_salt, JsonObject
import ctypes
import sys
from io import TextIOWrapper
from typing import Literal

import sys
from typing import Literal, TextIO


class Log:
    def __init__(self, type_: Literal['STDOUT', 'STDERR'], file: TextIO):
        self.type_ = type_
        self.file = file

    def write(self, v):
        if v not in ['', ' ', '\n']:
            self.file.write(f'{self.type_}: {v}\n')
            self.file.flush()  # Сбрасываем буфер для немедленной записи
            sys.__stdout__.write(f'{self.type_}: {v}\n')

    def flush(self):
        self.file.flush()


# Очищаем файл лога
with open('./data/msgr.log', 'w'):
    pass

# Открываем файл для записи
log_file = open('./data/msgr.log', 'a')

# Перенаправляем stdout и stderr
sys.stderr = Log(type_='STDERR', file=log_file)
sys.stdout = Log(type_='STDOUT', file=log_file)

try:
    import requests
except ModuleNotFoundError:
    print('!! Update is unavailable: requests not found !!')

# opening datas
version_0 = '0'
loader = Tk()
base_conf = json.load(open('./data/base_data.json'))
print(base_conf)

# configuring window
loader.title(f'loader')
loader.resizable(False, False)
loader.geometry('300x100')
Label(text=f'file: {__file__}\nname: {__name__}\n').pack()
# info and windows check
print(f'launcher&exception hook v.{version_0}')
print(f'[loader][info] win release {platform.release()}')
if platform.release() == '11':
    print('[loader][warning] in windows 11 tkinter may be work not correctly')
# loading data.nc
try:
    dat = SNConfig(decrypt(open('./data/DATA.NC', 'r', encoding='windows-1251').read(), eval(base_conf['CC'])))
    data_ = dat.load()
    cnf = SConfig(data_['[LOADER_CONFIG]'])
    vers = cnf['CC_VERSIONS'].split('$%')[0]
except (KeyError, TypeError) as nc_load_ex:
    showerror('Error', f'DATA.NC not loaded. All configuration will be reset. If this is first launch, ignore this error.\nAnyway, restart program')
    showerror('adv', traceback.format_exc())
    if askyesno('Clear DATA.NC?', 'Clear DATA.NC?'):
        base_conf['CC'] = str(generate_salt())
        json.dump(base_conf, JsonObject(open('./data/base_data.json', 'w')))
        base_conf = json.load(open('./data/base_data.json'))
        with open('./data/DATA.NC', 'w', encoding='windows-1251') as fl:
            d = base_conf['DATA_NC_CLEARED']
            fl.write(encrypt(d, eval(base_conf['CC'])))
        sys.exit()
    else:
        sys.exit()

# reinitializing loader win
loader.destroy()

# check LL_Update in RUNT_ACTION
if base_conf['RUNT_ACTION'] == 'LL_Update':
    with open('./msgr.py', 'r') as fl:
        with open('./data/code_backup.py', 'w'):
            pass
        open('./data/code_backup.py', 'w').write(fl.read())
    if open('./data/code_backup.py', 'r').read() == open('./msgr.py', 'r').read():
        with open('./msgr.py', 'w'):
            pass
        with open('./msgr.py', 'w') as fl:
            def download_from_github(url, save_path):
                # Заменяем на raw-ссылку если нужно
                if 'github.com' in url and 'raw.githubusercontent.com' not in url:
                    url = url.replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/')

                response = requests.get(url)
                if response.status_code == 200:
                    with open(save_path, 'wb') as f:
                        f.write(response.content)
                    print(f"Файл сохранен как {save_path}")
                else:
                    print(f"Ошибка загрузки: {response.status_code}")
            # Пример использования:
            github_url = "https://raw.githubusercontent.com/zcveo5/msgr-qw/main/msgr.py"
            download_from_github(github_url, "msgr_upd.py")
            print('Please update from file to complete update')
    else:
        print('[loader][error][update] failed to backup code')
# checking LL_F_Update in RUNT_ACTION
if base_conf['RUNT_ACTION'] == 'LL_F_Update':
    print('[loader] updating from file')
    try:
        open('./msgr_upd.py')
        with open('./msgr.py', 'r') as fl:
            with open('./data/code_backup.py', 'w'):
                pass
            open('./data/code_backup.py', 'w').write(fl.read())
        if open('./data/code_backup.py', 'r').read() == open('./msgr.py', 'r').read():
            with open('./msgr.py', 'w'):
                pass
            with open('./msgr.py', 'w') as _fl:
                _fl.write(open('./msgr_upd.py', 'r').read())
        print('[loader] updated')
        base_conf['RUNT_ACTION'] = ''
    except FileNotFoundError:
        print('[loader][error] cant find update file. must be in main directory (near with msgr.py) and with name msgr_upd.py')

# VerSelect argv
if 'VerSelect' in sys.argv:
    def ver_sel(event):
        global vers
        vers = ver_s.get()
        win.quit()
        win.destroy()
    win = Tk()
    win.geometry('200x200')
    Label(win, text='select ver').pack()
    ver_s = ttk.Combobox(win, values=cnf['CC_VERSIONS'].split('$%'), state='readonly')
    ver_s.bind('<<ComboboxSelected>>', ver_sel)
    ver_s.pack()

    win.mainloop()
if not os.path.exists(f'{vers}'):
    showerror('Error', f'{vers} is not exists')
    sys.exit()
print(data_)
ctypes.windll.shcore.SetProcessDpiAwareness(eval(data_['[SETTINGS]'])['USER_SETTINGS']['SCREEN_SETTINGS'][1])

for i in sys.argv:
    if 'BTAE!DebugAction' in i:
        exec(i.split('$=%')[1])
json.dump(base_conf, JsonObject(open('./data/base_data.json', 'w')))
sys.argv.insert(1, vers.replace('/', '.').replace('.py', ''))

# execute
try:
    app = __import__(vers.replace('/', '.').replace('.py', ''), fromlist=['load_lbl', 'main'])
except Exception as __ex:
    print(f'[loader][error] {__ex}')
    print(f'[loader][traceback]\n{traceback.format_exc()}')
    try:
        app.load_lbl['text'] += f'[loader][error] {__ex}\n[loader][traceback]\n{traceback.format_exc()}'
        app.main.update()
    except NameError:
        pass
    get_win(exc_with_traceback=traceback.format_exc(), program_title='msgr qw (low-level traceback)')

os.abort()
