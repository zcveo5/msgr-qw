import json
import os.path
import platform
import sys
import traceback
from tkinter import Tk, Label, ttk
from tkinter.messagebox import showerror, askyesno
import plugins.btac.auth
import data.btaeui
from plugins.core.mod import SConfig, decrypt, SNConfig, encrypt, get_win, generate_salt, JsonObject

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
loader = Tk()
loader.resizable(False, False)

# check LL_Update in RUNT_ACTION
if base_conf['RUNT_ACTION'] == 'LL_Update':
    Label(text='Update in progress...').pack()
    loader.update()
    pb = data.btaeui.ProgressBar(Label())
    pb.i().pack()
    with open('./msgr.py', 'r') as fl:
        with open('./data/code_backup.py', 'w'):
            pass
        open('./data/code_backup.py', 'w').write(fl.read())
    if open('./data/code_backup.py', 'r').read() == open('./msgr.py', 'r').read():
        with open('./msgr.py', 'w'):
            pass
        with open('./msgr.py', 'w') as fl:
            print(data_)
            server = eval(data_['[SETTINGS]'])['USER_SETTINGS']['BT_SERV']
            try:
                plugins.btac.auth.connect(server.split(':')[0], int(server.split(':')[1]))
                print(plugins.btac.auth.raw_request({'action': 'update'}))
                fl.write(plugins.btac.auth.raw_request({'action': 'update'})['answer'])
                base_conf['RUNT_ACTION'] = ''
            except (ConnectionError, IndexError):
                print('[loader][error][update] failed connect to server, reverting changes')
                fl.write(open('./data/code_backup.py', 'r').read())
    else:
        print('[loader][error][update] failed to backup code')
    plugins.btac.auth.disconnect()


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
    showerror('Error', f'Looks {vers} is not exists. Please change path using data_nc_wrk.py')
    sys.exit()


for i in sys.argv:
    if 'BTAE!DebugAction' in i:
        exec(i.split('$=%')[1])
json.dump(base_conf, JsonObject(open('./data/base_data.json', 'w')))
loader.destroy()
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