# encoding: windows-1251

# BTAE Utils module. PLEASE DONT EDIT

from __future__ import annotations
from tkinter.ttk import Combobox
from typing import TextIO
import traceback
from tkinter.messagebox import showerror, showinfo
import _tkinter
import sys
from tkinter import *
import random
import json
import os
import time

app = None
class CorePlugin:
    @staticmethod
    def give_data(v):
        global app
        app = v

    @staticmethod
    def execute():
        pass


def plugin_info():
    showinfo('BTAEML (BebraTech Application Engine Mod Loader)',
             "BTAEML (BebraTech Application Engine Mod Loader) coded by BebraTech Inc. (BTAE authors).\n"
             "ALL plugins/mods made by other people (not BebraTech Inc.)\n"
             "We aren't take responsibility if your PC damaged by plugins/mods.\n\n"
             "BTAEML is included in all BTAE version 2.8.9 and above.\n"
             "In other versions BTAEML work unstable.\n\n"
             "BTAEML Team (BebraTech subdivision) 2025")


def load(theme_load, def_bg=None, def_fg=None, def_font=None):
    theme = {}
    temp = theme_load.read().split('''
''')
    for i in temp:
        theme.update({i.split('=')[0]: i.split('=')[1]})
    if def_bg is not None:
        def_bg = theme['main_color']
    if def_fg is not None:
        def_fg = theme['secondary_color']
    if def_font is not None:
        tmp = theme['font'].split()
        if theme['font'] == 'None':
            def_font = (None, 9)
        else:
            try:
                def_font = (tmp[0], int(tmp[len(tmp) - 1]))
            except IndexError:
                def_font = ''
    return def_bg, def_fg, def_font


class Locale:
    def __init__(self, conf: Config):
        self.lc_dct = conf.dct
        self.conf = conf

    def __getitem__(self, item):
        if item in self.lc_dct:
            return self.lc_dct[item]
        else:
            return f'locale_off:{item}'


def tk_wait(sec: int, win):
    _time = float(sec)
    while _time < sec:
        time.sleep(0.2)
        win.update()
        _time += 0.2


class NConfig:
    def __init__(self, fl: TextIO):
        self.conf = fl.read()

    def load(self):
        decoded = {}
        tmp = self.conf.split('#$#$SER')
        for i in tmp:
            i_sp = i.split('\n')
            i_sp_w = i_sp.copy()
            i_sp_w.pop(0)
            decoded.update({i_sp[0]: '\n'.join(i_sp_w)})
        for i in decoded:
            decoded[i] = decoded[i][0:len(decoded[i]) - 1]
        try:
            decoded.pop('')
        except KeyError:
            pass
        return decoded

    @staticmethod
    def dump(conf):
        coded = ''
        for i in conf:
            coded += f'#$#$SER{i}\n'
            coded += conf[i] + '\n'
        return coded



class SNConfig:
    def __init__(self, fl: str):
        self.conf = fl

    def load(self):
        decoded = {}
        tmp = self.conf.split('#$#$SER')
        for i in tmp:
            i_sp = i.split('\n')
            i_sp_w = i_sp.copy()
            i_sp_w.pop(0)
            decoded.update({i_sp[0]: '\n'.join(i_sp_w)})
        for i in decoded:
            decoded[i] = decoded[i][0:len(decoded[i]) - 1]
        try:
            decoded.pop('')
        except KeyError:
            pass
        return decoded

    @staticmethod
    def dump(conf):
        coded = ''
        for i in conf:
            coded += f'#$#$SER{i}\n'
            coded += conf[i] + '\n'
        return coded


def generate_salt():
    codec = r"""qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890~!@#$%^&*()_+-=?><,./|"'[]{}:; """
    symbols = ['\n']
    for i in codec:
        symbols.append(i)
    randomized_symbols = {}
    symbols_c = symbols.copy()
    for i in range(len(symbols_c)):
        print(i)
        cur_ind = random.randint(0, len(symbols) - 1)
        randomized_symbols.update({symbols_c[i]: symbols[cur_ind]})
        symbols.remove(symbols[cur_ind])
    return randomized_symbols


def encrypt(data, salt):
    out = []
    for sym in data:
        try:
            out.append(salt[sym])
        except KeyError:
            salt.update({sym: "?"})
            out.append(salt[sym])
    return ''.join(out)


def decrypt(data, salt):
    out = []
    k_list = list(salt.keys())
    v_list = list(salt.values())
    for sym in data:
        try:
            out.append(k_list[v_list.index(sym)])
        except ValueError:
            out.append('?')
    return ''.join(out)


def get_win(exc_with_traceback='No-Information-Provided',
            program_title='No-Information-Provided'):
    try:
        rep = Tk()
    except _tkinter.TclError:
            print('[FATAL_ERROR] Invalid TCL configuration')
            print(traceback.format_exc())
            sys.exit()
    rep.title('Fatal Error')
    rep.resizable(False, False)
    Label(rep, text=f'Program {program_title} has been crashed.\n\n\n'
                    f'There is some crash info:\n{exc_with_traceback}', justify=LEFT).pack()
    rep.mainloop()
    sys.exit()


def autoload_objects(_plugs):
    for key, value in _plugs.items():
        cur_mod = key
        try:
            print(f'[plug_api][info] auto loading mod {key}')
            st_time = time.time()
            value['plugin'].execute()
            fin_time = time.time()
            print(f"[plug_api][info] completed in {str(fin_time - st_time).split('.')[0]}sec")
        except Exception as _ex:
            print(f'[plug_api][error] {cur_mod} loaded with error. skip '
                          f'(error details: {_ex})')


def get_plugs():
    print('[plug_api][info] compiling plugins')
    compiled_plugins = {}
    for name in os.listdir("./plugins"):
        if os.path.isdir(os.path.join("./plugins", name)):
            try:
                open(f"./plugins/{name}/metadata.json")
                with open(f"./plugins/{name}/metadata.json") as f:
                    plugin_data = json.load(f)
                    if plugin_data['state'] == 'True':
                        imported = __import__(f"plugins.{name}.{plugin_data['file']}")
                        compiled_plugins[plugin_data['name']] = {"plugin": (getattr(getattr(getattr(imported, name), plugin_data['file']), plugin_data['class']))(), "metadata": plugin_data}
                print(f'[plug_api][info] compiled plugin {name}')
            except Exception as _ex:
                print(f'[plug_api][error] invalid plugin {name}, skip ({_ex})')
    print('[plug_api][info] pre-loading plugins')
    mod = __import__('msgr')
    for key, value in compiled_plugins.items():
        try:
            value['plugin'].give_data(mod)
            print(f'[plug_api][info] {key} pre-loaded')
        except AttributeError as preload_ex:
            print(f'[plug_api][error] invalid plugin_MainThread {key}. details: {preload_ex}')
    print('[plug_api][info] completed')
    print(compiled_plugins)
    return compiled_plugins


class Config:
    def __init__(self, title, coding=None):
        self.title = title
        try:
            open(title, 'r')
        except FileNotFoundError:
            with open(title, 'w'):
                pass
        self.config_w = open(title, 'a', encoding=coding)
        self.config_r = open(title, 'r', encoding=coding)
        self.dct = self._get_items()

    def write(self, key, value):
        self.config_w.write(f'{key}:{value}\n')
        self.config_w.close()
        self.config_w = open(self.title, 'a')

    def _get_items(self):
        """WARNING!!! THIS METHOD IS BROKEN! USE self.dct OR __getitem__"""
        cnf = {}
        for elem in self.config_r.read().split('\n'):
            if len(elem.split(':')) == 2:
                cnf.update({elem.split(':')[0]: elem.split(':')[1]})
        return cnf

    def __getitem__(self, item):
        return self.dct[item]


class SConfig:
    def __init__(self, data):
        self.data = data
        self.dct = self._get_items()

    def _get_items(self):
        """WARNING! THIS METHOD IS BROKEN! USE self.dct OR __getitem__"""
        cnf = {}
        for elem in self.data.split('\n'):
            if len(elem.split(':')) == 2:
                cnf.update({elem.split(':')[0]: elem.split(':')[1]})
        return cnf

    def __getitem__(self, item):
        return self.dct[item]


def log_add(data):
    open('log.log', 'a').write(f'\n{data}')


work = True


class FirstSetup:
    def __init__(self, bg, fg, fnt, locale, change_lc, change_th):
        self.bg = bg
        self.fg = fg
        self.fnt = fnt
        self.locale = locale
        self.funcs = (change_lc, change_th)

    def get_win(self):
        global work
        work = True

        win = Tk()
        def ini1():

            def ex():
                global work
                work = False
                win.destroy()


            def locale_help(event):
                lc = self.funcs[1](sel_lc.get(), True)
                print(sel_lc.get())
                self.locale = lc
                ini1()
                lb1.pack_forget()
                lb2.pack_forget()
                sel_lc.pack_forget()
                sel_th.pack_forget()
                c.pack_forget()

            def theme_help(event):
                theme_ = self.funcs[0](sel_th.get().split('.')[0], True)
                self.fg = theme_[1]
                self.bg = theme_[2]
                self.fnt = theme_[0]
                ini1()
                lb1.pack_forget()
                lb2.pack_forget()
                sel_lc.pack_forget()
                sel_th.pack_forget()
                c.pack_forget()

            win.configure(bg=self.bg)
            win.title(self.locale['fs_title'])
            win.geometry('300x200')
            win.resizable(False, False)
            lb1 = Label(win, text=self.locale['fs_locale'], bg=self.bg, fg=self.fg, font=self.fnt)
            lb1.pack()
            sel_lc = Combobox(win, values=os.listdir('./data/locale'), state="readonly", font=self.fnt)
            sel_lc.pack()
            sel_lc.bind("<<ComboboxSelected>>", locale_help)
            lb2 = Label(win, text=self.locale['fs_theme'], bg=self.bg, fg=self.fg, font=self.fnt)
            lb2.pack()
            sel_th = Combobox(win, values=os.listdir('./data/theme'), state="readonly", font=self.fnt)
            sel_th.pack()
            sel_th.bind("<<ComboboxSelected>>", theme_help)
            c = Button(win, text=self.locale['fs_continue'], bg=self.bg, fg=self.fg, font=self.fnt, command=ex)
            c.pack()

        ini1()
        while work:
            try:
                win.update()
            except TclError:
                break
            time.sleep(0.01)
        else:
            try:
                win.destroy()
            except TclError:
                pass
