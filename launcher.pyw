import os.path
import platform
import sys
import tkinter
from tkinter.messagebox import showerror, askyesno
import requests

class Log:
    def __init__(self, type_: str, _file):
        self.type_ = type_
        self.file = _file
        self.name = self.file.name
        self.last_v = ''

    def write(self, v):
        if v not in ['', ' ', '\n', '<VirtualEvent event x=0 y=0>'] and v != self.last_v:
            repr_v = repr(v)[1:-1]
            if repr(v)[1:-1][len(repr_v) - 2:len(repr_v)] == r'\n':
                v = v[:len(v) - 1]
            try:
                self.file.write(f'[{self.type_}]{v}\n')
            except UnicodeError:
                self.file.write(f'[{self.type_}][loader] log_file_unsupported_encoding\n')
            self.last_v = v
            self.file.flush()  # Сбрасываем буфер для немедленной записи
        if v not in ['', ' ', '\n', '<VirtualEvent event x=0 y=0>']:
            try:
                sys.__stdout__.write(f'[{self.type_}]{v}\n')
            except AttributeError:
                pass

    def flush(self):
        self.file.flush()

os.makedirs('./data/logs', exist_ok=True)
with open('./data/logs/low_launcher.log', 'w'):
    pass

log_file = open('./data/logs/low_launcher.log', 'a')

if '-no-file-log' not in sys.argv:
    sys.stderr = Log(type_='STDERR', _file=log_file)
    sys.stdout = Log(type_='STDOUT', _file=log_file)

libs = ['./data/btaeui.py', './data/utils.py', './plugins/btac/chat.py', './plugins/btac/auth.py', './plugins/core/mod.py']
files = ['msgr.py', 'loader.py',
         './data',
           './data/data.nc',
           './data/base_data.json',
            './data/locale',
             './data/locale/en',
              './data/locale/en/locale.cfg',
           './data/theme',
            './data/theme/night.theme',
         './plugins',
           './plugins/core',
           './plugins/btac']
py_ver = sys.version_info
url_patches = "https://raw.githubusercontent.com/zcveo5/msgr-patches/main"
url_main = "https://raw.githubusercontent.com/zcveo5/msgr-qw/main"
def download_patch(pyver, libn, save_path):
    content = requests.get(f'{url_patches}/{pyver}/{libn}.py').content
    with open(f'{save_path}/{libn}_backup', 'wb') as fl:
        fl.write(open(f'{save_path}/{libn}.py', 'rb').read())
    with open(f'{save_path}/{libn}.py', 'wb') as fl:
        fl.write(content)


def download_file(path, save_path):
    content = requests.get(f'{url_main}/{path.replace("./", "")}').content
    with open(save_path, 'wb') as fl:
        fl.write(content)

def check_for_updates():
    for i in libs:
        ver = open(i, 'rb').readlines(1)
        print(ver, ver.__class__)
        if ver[0] != b'# downloaded from msgr-patches for 3.8!\r\n' and 8 <= py_ver[1] < 13:
            return True
        elif ver[0] != b'# downloaded from msgr-patches!\r\n' and py_ver[1] >= 13:
            return True
    return False


def update_status(text, mode='set'):
    if mode == 'set':
        status_lbl['text'] = text + '\n'
    elif mode == 'plus':
        status_lbl['text'] += text + '\n'
    win.update()


print('[software checker] ~ INFO ~\nRunning on ' + platform.system() + ' ' + str(platform.release()) + '\nwith Python ' + str(py_ver[0]) + '.' + str(py_ver[1]) + '.' + str(py_ver[2]))

win = tkinter.Tk()
win.title('Info')
tkinter.Label(win,
              text='System: ' + str(platform.system()) + ' ' + str(platform.release()) + '\n' + 'Python: ' + str(py_ver[0]) + '.' + str(py_ver[1]) + '.' + str(py_ver[2])).pack()
status_lbl = tkinter.Label(win, justify='left')
status_lbl.pack()
print('checking files...')
update_status('checking files...')
need_to_download = []
for _fl in files + libs:
    res = os.path.exists(_fl)
    if res:
        path_spl = _fl.split('/')
        if '.' in path_spl[len(path_spl) - 1]:
            _frst = open(_fl, 'rb').readlines(1)
            if _frst[0]  == b'404: Not Found':
                print(f'[  ER  ] {_fl} not found on repo')
                update_status(f'[  ER  ] {_fl} not found on repo', 'plus')
                showerror('Fatal Error', f'[  ER  ] {_fl} not found on repo')
            else:
                print(f'[  OK  ] {_fl} first str is {_frst}')
        print(f'[  OK  ] {_fl} exists')
        update_status(f'[  OK  ] {_fl} exists', 'plus')
    else:
        print(f'[  ER  ] {_fl} not exists, creating')
        update_status(f'[  ER  ] {_fl} not exists, creating', 'plus')
        path_spl = _fl.split('/')
        if '.' in path_spl[len(path_spl) - 1]:
            need_to_download.append(_fl)
            with open(_fl, 'w'):
                pass
            print(f'  [  OK  ] created {_fl} as file')
            update_status(f'  [  OK  ] created {_fl} as file', 'plus')
        else:
            os.mkdir(_fl)
            update_status(f'  [  OK  ] created {_fl} as directory', 'plus')
            update_status(f'  [  OK  ] created {_fl} as directory', 'plus')

update_status('')
if need_to_download:
    update_status('[  OK  ] downloading needed files')
    for file in need_to_download:
        print(f'[  WR  ] downloading {file}')
        update_status(f'[  WR  ] downloading {file}', 'plus')
        download_file(file, file)


print('checking python version...')
if py_ver[0] < 3:
    showerror('Error', 'Unsupported Python major Version ' + str(py_ver[0]) + ' < 3')
    sys.exit()
if py_ver[1] < 8:
    showerror('Error', 'Unsupported Python minor Version 3.' + str(py_ver[1]) + ' < 3.8')
    sys.exit()
print('supported!')
print('checking platform')
if platform.system() not in ['Windows', 'Linux']:
    if not askyesno('Warning', 'Not Windows system detected. On your system MSGR not tested and some functions can not work. If it works, you can comment my repo on GitHub.\n\nContinue?'):
        sys.exit()
elif platform.system() == 'Windows':
    if platform.release() not in ['7', '10', '11']:
        showerror('Error', 'Unsupported Windows version')
        sys.exit()
elif platform.system() == 'Linux':
    ...
print('completed!')
if py_ver[0] == 3 and 8 <= py_ver[1] < 13 and check_for_updates() or '--force-update' in sys.argv:
    ask = askyesno('Warn', f'Detected Python 3.{py_ver[1]}.{py_ver[2]}. You need to download patched libs optimized for version 3.8 - 3.12.\nDownload it now?')
    if ask:
        win.winfo_children()[0]['text'] = 'Update in progress!\ndownloading utils...'; win.update()
        download_patch('3.8', 'utils', './data')

        win.winfo_children()[0]['text'] = 'Update in progress!\ndownloading auth...'; win.update()
        download_patch('3.8', 'auth', './plugins/btac')

        win.winfo_children()[0]['text'] = 'Update in progress!\ndownloading chat...'; win.update()
        download_patch('3.8', 'chat', './plugins/btac')

        win.winfo_children()[0]['text'] = 'Update in progress!\ndownloading core...'; win.update()
        download_patch('3.8', 'mod', './plugins/core')

        win.winfo_children()[0]['text'] = 'Update in progress!\ndownloading btaeui...'; win.update()
        download_patch('3.8', 'btaeui', './data')
elif py_ver[0] == 3 and py_ver[1] == 13 and check_for_updates() or '--force-update' in sys.argv:
    ask = askyesno('Warn',
                   'Detected Python 3.13. You need to download patched libs optimized for version 3.13 and above.\nDownload it now?')
    if ask:
        win.winfo_children()[0]['text'] = 'Update in progress!\ndownloading utils...' ; win.update()
        download_patch('3.13', 'utils', './data')

        win.winfo_children()[0]['text'] = 'Update in progress!\ndownloading auth...' ; win.update()
        download_patch('3.13', 'auth', './plugins/btac')

        win.winfo_children()[0]['text'] = 'Update in progress!\ndownloading chat...' ; win.update()
        download_patch('3.13', 'chat', './plugins/btac')

        win.winfo_children()[0]['text'] = 'Update in progress!\ndownloading core...' ; win.update()
        download_patch('3.13', 'mod', './plugins/core')

        win.winfo_children()[0]['text'] = 'Update in progress!\ndownloading btaeui...' ; win.update()
        download_patch('3.13', 'btaeui', './data')


win.quit() ; win.destroy()
print('running loader')
__import__('loader')
