import json
import tkinter
import traceback
from tkinter import Tk, Label, ttk, Button
from plugins.core.mod import SConfig, decrypt, SNConfig, encrypt, get_win, generate_salt, JsonObject
from data.utils import *
import ctypes
import platform
import sys
from tkinter.messagebox import showerror, askyesno

if __name__ != '__main__':
    if 'launcher.pyw' not in sys.argv[0]:
        sys.exit()

with open('./data/logs/tracebacks.log', 'w'):
    pass

print(f'[loader][info] {__file__} launcher for BTAE.')
print('[loader][info] Initializing')
print('[loader][info] replacing stderr, stdout')
cons_shut = True

def show(title, text, ret_win=False, custom_close=None):
    info = Tk()
    def exit_mb():
        nonlocal info
        info.destroy()
        info = None
        if custom_close is not None:
            custom_close()
    info.title(title)
    fnt = ('Consolas', 9)
    bg = 'white'
    fg = 'black'
    info.configure(bg=bg)
    info.resizable(False, False)
    info.attributes('-topmost', True)
    Label(info, text=text, bg=bg, fg=fg, font=fnt, justify=tkinter.LEFT).pack(anchor='center', pady=30, ipadx=10)
    Button(info, text='OK', bg=bg, fg=fg, font=fnt, command=exit_mb).pack(anchor='se', side='bottom', expand=True, ipadx=10, ipady=5)
    if ret_win:
        return info


def custom_exc_handler(exc_type, exc_value=None, exc_traceback=None):
    tb_lines = list(traceback.format_exception(exc_type, exc_value, exc_traceback))
    if 'safe_command' in tb_lines[1]:
        tb_lines = tb_lines[1::]
        tb_lines.insert(0, 'btae ui widget Traceback\nbtae ui widget called function, last returned raw traceback:\n')

    tb_text = "".join(tb_lines)
    print('===== TRACEBACK =====\n' + tb_text + f'\n===== END =====')
    with open('./data/logs/tracebacks.log', 'a') as f_l:
        f_l.write(tb_text + '\n\n')
    try:
        show(f'Error: {exc_type.__name__}', tb_text)
    except AttributeError:
        show(f'Error: {exc_type.__class__}', tb_text)


def custom_exc_handler_thread(exc_type, exc_value=None, exc_traceback=None):
    tb_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
    tb_text = "".join(tb_lines)
    print('===== TRACEBACK THREAD =====\n' + tb_text + '===== END =====')
    with open('./data/logs/tracebacks.log', 'a') as f_l:
        f_l.write(tb_text + '\n\n')
    show(f'Error from thread: {exc_type}', tb_text)


sys.excepthook = custom_exc_handler
threading.excepthook = custom_exc_handler_thread


# Очищаем файл лога
with open('./data/msgr.log', 'w'):
    pass

# Открываем файл для записи
log_file = open('./data/msgr.log', 'a')

# Перенаправляем stdout и stderr
if '-no-file-log' not in sys.argv:
    sys.stderr = Log(type_='STDERR', file=log_file)
    sys.stdout = Log(type_='STDOUT', file=log_file)

try:
    print(' ~ LOG STARTED ~')
except Exception as _ex:
    showerror(f'Error {type(_ex)}', traceback.format_exc())
    sys.exit()


try:
    import requests
except ModuleNotFoundError:
    print('[loader][warning] !! Update is unavailable: requests not found !!')



# opening datas
version_0 = '0'
loader = Tk()
base_conf = json.load(open('./data/base_data.json'))
# configuring window
loader.title(f'loader')
loader.resizable(False, False)
loader.geometry('300x100')
Label(text=f'file: {__file__}\nname: {__name__}\n').pack()
# info and windows check
print(f'[loader][info] launcher&exception hook v.{version_0}')
print(f'[loader][info] win release {platform.release()}')
# loading data.nc
try:
    dat = SNConfig(decrypt(open('./data/DATA.NC', 'r', encoding='windows-1251').read(), eval(base_conf['CC'])))
    data_ = dat.load()
    cnf = SConfig(data_['[LOADER_CONFIG]'])
    versions = cnf['CC_VERSIONS'].split('$%')
    vers = cnf['CC_VERSIONS'].split('$%')[0]
except (KeyError, TypeError, FileNotFoundError) as nc_load_ex:
    if isinstance(nc_load_ex, FileNotFoundError):
        with open('./data/DATA.NC', 'w'):
            pass
    showerror('Error', f'DATA.NC not loaded. All configuration will be reset. If this is first launch, ignore this error.\nAnyway, restart program')
    if askyesno('Clear DATA.NC?', 'Clear DATA.NC?'):
        base_conf['CC'] = str(generate_salt())
        json.dump(base_conf, JsonObject(open('./data/base_data.json', 'w')))
        base_conf = json.load(open('./data/base_data.json'))
        with open('./data/DATA.NC', 'w', encoding='windows-1251') as fl:
            d = base_conf['DATA_NC_CLEARED']
            fl.write(encrypt(d, eval(base_conf['CC'])))
        dat = SNConfig(decrypt(open('./data/DATA.NC', 'r', encoding='windows-1251').read(), eval(base_conf['CC'])))
        data_ = dat.load()
        cnf = SConfig(data_['[LOADER_CONFIG]'])
        versions = cnf['CC_VERSIONS'].split('$%')
        vers = cnf['CC_VERSIONS'].split('$%')[0]
    else:
        sys.exit()
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
            base_conf['RUNT_ACTION'] = 'LL_F_Update'
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
# Loader:AllFilesAreExec argv
if 'Loader:AllFilesAreExec' in sys.argv:
    tmp = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if '__pycache__' not in os.path.join(root, file):
                tmp.append(os.path.join(root, file).replace('\\', '/'))
    versions = []
    for i in tmp:
        if '.py' in i and i != 'run.pyw':
            versions.append(i)
    sys.argv.append('VerSelect')
# VerSelect argv
if 'VerSelect' in sys.argv:
    def ver_sel(event):
        global vers
        print(event)
        vers = ver_s.get()
        win.quit()
        win.destroy()
    win = Tk()
    win.geometry('200x200')
    Label(win, text='select ver').pack()
    ver_s = ttk.Combobox(win, values=versions, state='readonly')
    ver_s.bind('<<ComboboxSelected>>', ver_sel)
    ver_s.pack()

    win.mainloop()
# file check
if not os.path.exists(f'{vers}'):
    showerror('Error', f'{vers} is not exists')
    sys.exit()
# dpi from screen settings
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(eval(data_['[SETTINGS]'])['USER_SETTINGS']['SCREEN_SETTINGS'][1])
except (FileNotFoundError, AttributeError):
    pass
# pre-start important things
json.dump(base_conf, JsonObject(open('./data/base_data.json', 'w')))
path = convert_path_to_module(vers)
sys.argv.insert(1, path)
# execute
try:
    print(' - ~ * PROGRAM * ~ - ')
    app = __import__(path)
    base_conf = json.load(open('./data/base_data.json', 'r'))
except Exception as __ex:
    exc = f'{type(__ex)}:{__ex}'
    print(f'[loader][error] {__ex}')
    print(f'[loader][traceback]\n{traceback.format_exc()}')
    print(exc)
    if exc not in base_conf['EXC_DATA']:
        get_win(exc_with_traceback=traceback.format_exc(), program_title='msgr qw (low-level traceback)')
    else:
        get_win(exc_with_traceback=base_conf['EXC_DATA'][exc], program_title='msgr qw')

cons_shut = False
if len(threading.enumerate()) > 1:
    print('some threads are exists, destroying')
    c = 0
    l_enum = len(threading.enumerate())
    for thread in threading.enumerate():
        print(f'{c}/{l_enum}')
        if thread != threading.current_thread():
            print(f'joined {thread.name}')
            thread.join()
        else:
            print('cur, passed')
        c += 1
print('exiting...')