# downloaded from msgr-patches for 3.8!

import math
import os.path
import sys
from tkinter import TclError
import tkinter
from typing import Literal, Union
import data.ru_to_en
from data import utils


class LogMeta(type):
    def __new__(cls, name, bases, dct):
        # Создаём новый класс
        new_class = super().__new__(cls, name, bases, dct)
        return new_class

class AdvLog(metaclass=LogMeta):
    def __getattribute__(self, name):
        # Получаем атрибут
        attr = super().__getattribute__(name)
        if callable(attr):
            # Если атрибут — это метод, создаём обёртку
            def wrapper(*args, **kwargs):
                if isinstance(self, Widget):
                    print_adv(f'[advlog][{self._name}] IS DESTROY : {self.destroyed} CALLED {name}')
                else:
                    print_adv(f"[advlog][{self}] called {name}")
                return attr(*args, **kwargs)
            return wrapper
        return attr

BLACK_LIST_LOGGING = ['empty name']
if __name__ != '__main__':
    with open('./data/logs/btae_ui.log', 'w'):
        pass
    with open('./data/logs/advlog_btae_ui.log', 'w'):
        pass
    def print_adv(v):
        _out = True
        for i in BLACK_LIST_LOGGING:
            if i in v:
                _out = False
                break
        if _out:
            print(f'[{os.path.basename(__file__)}]{v}')
            if 'advlog' not in v:
                with open(f'./data/logs/btae_ui.log', 'a') as fl:
                    try:
                        fl.write(f'[{os.path.basename(__file__)}]{v}\n')
                    except UnicodeError:
                        fl.write(f'[{os.path.basename(__file__)}]{data.ru_to_en.replace_letters(v)}\n')
            else:
                with open('./data/logs/advlog_btae_ui.log', 'a') as fl:
                    try:
                        fl.write(f'[{os.path.basename(__file__)}]{v}\n')
                    except UnicodeError:
                        fl.write(f'[{os.path.basename(__file__)}]{data.ru_to_en.replace_letters(v)}\n')
else:
    def print_adv(v):
        print(v)


def _pass():
    pass

class Widget(AdvLog):
    def __init__(self, mast, obj, name: str, **kw):
        self._root_win = mast
        self.tk = obj
        self._kwargs = kw
        self._name = name
        self._place_mode = 'NotPlaced'
        self.destroyed = False

    def build(self, mode: Literal['place', 'grid', 'pack'], **kwargs):
        print_adv(f'[{self._name}] build {mode} {kwargs} {self.tk.__dict__}')
        if mode == 'place':
            self.tk.place(**kwargs)
        elif mode == 'grid':
            self.tk.grid(**kwargs)
        elif mode == 'pack':
            self.tk.pack(**kwargs)
        self._place_mode = mode

    def forget(self):
        if self._place_mode == 'place':
            self.tk.place_forget()
        elif self._place_mode == 'grid':
            self.tk.grid_forget()
        elif self._place_mode == 'pack':
            self.tk.pack_forget()

    def destroy(self):
        try:
            if self.tk.winfo_exists():  # Проверка существования
                self.forget()
                self.tk.destroy()
                print_adv(f'[{self._name}] {self._name} destroyed')  # Лог успешного удаления
                self.destroyed = True
        except TclError as e:
            print_adv(f'[{self._name}] Error destroying: {e}')

    def configure(self, **kwargs):
        self.tk.configure(**kwargs)

    def __getitem__(self, item):
        return self.tk[item]

    def __setitem__(self, key, value):
        self.tk[key] = value


class CallBack:
    def __init__(self, target = _pass):
        self.Target = target


class ProgressBar(tkinter.Label):
    def __init__(self, len_to_count=100, **kwargs):
        super().__init__(**kwargs)
        self.percentage = 0
        self._ltc = len_to_count
        self._progress = "." * 100

        self['text'] = f'[{self._progress}] {self.percentage}/100'

    def plus(self, v=1):
        if self.percentage < 100:
            self.percentage += math.ceil(v * self._gen_percent())
            self._progress = '|' * self.percentage + '.' * (100 - self.percentage)
            try:
                if self.winfo_exists():
                    self['text'] = f'[{self._progress}] {self.percentage}/100'
            except TclError:
                pass
        else:
            self['text'] = f'[{self._progress}] Completed'
        self.update()

    def _gen_percent(self):
        return 100 / self._ltc



class Button(tkinter.Button):
    def __init__(self, master=None, command="", **kwargs):
        if command != "":
            command = self._wrap_command(command)
        # Явный вызов конструктора родителя с правильными аргументами
        super().__init__(
            master=master,
            command=command,
            **kwargs
        )

    @staticmethod
    def _wrap_command(cmd):
        def safe_command():
            try:
                cmd()
            except Exception as e:
                sys.excepthook(type(e), e, e.__traceback__)
        return safe_command


class Label(tkinter.Label):
    def __init__(self, master=None, **kwargs):
        super().__init__(
            master=master,
            **kwargs)


class Text(tkinter.Text):
    def __init__(self, master=None, **kwargs):
        super().__init__(
            master=master,
            **kwargs)


class Entry(tkinter.Entry):
    def __init__(self, master=None, **kwargs):
        super().__init__(
           master=master,
           **kwargs)



POSSIBLE_WIDGETS = [Label, Button, Text, Entry, ProgressBar]
POSSIBLE_WIDGETS_TK = [tkinter.Label, tkinter.Button, tkinter.Text, tkinter.Entry]


class Win(tkinter.Tk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.his = {}
        self._registered_widgets = []
        self.his_being = {}
        self.widgets_name = []
        self.recovery_widgets = []
        self.bind('<Control-s>', self.recovery)

    def recovery(self, event=None):
        self.destroy_all_in()
        for i in self.recovery_widgets:
            if callable(i):
                i()
            else:
                self.create(i['name'], i['obj'], recreate_if_exists=True, **i['kwargs']).build(i['place_mode'], **i['place_kw'])


    def geometry(self, size=None, pos=None):
        if size is None:
            size = []
        if pos is None:
            pos = []
        if size:
            super().geometry(f'{size[0]}x{size[1]}')
        if pos:
            super().geometry(f'{super().geometry().split("+")[0]}+{pos[0]}+{pos[1]}')
        if not size and not pos:
            return super().geometry()

    def create(self, name: str, obj: POSSIBLE_WIDGETS, recreate_if_exists=False, **kwargs) -> Widget:
        print_adv(f'[win {self.title()}] creating widget {name}')
        if name in self.his:
            if not recreate_if_exists:
                raise ValueError(f"Widget name '{name}' is not unique!")  # Явная ошибка при дубликате
            else:
                self.his[name].destroy()
                self.his.pop(name)
        print(f'[win {self.title()}][{name}] {kwargs} {obj}')
        create_kw = kwargs
        self.his[name] = Widget(self, obj(**create_kw), name=name)
        self._registered_widgets.append(self.his[name].tk)
        self.his_being.update({name: self.his[name]})
        self.widgets_name.append(name)
        return self.his[name]

    def being_ping(self):
        ans = {}
        for name in self.his_being:
            ans.update({name: self.his_being[name].tk.winfo_exists()})
        return ans

    def create_abstract(self, name: str, obj: CallBack):
        self.his.update({name: obj})

    def destroy_all_in(self):
        print_adv(f'[win {self.title()}] destroying all widgets')
        # Уничтожаем все виджеты, включая служебные
        for name in list(self.his.keys()):  # Используем list() для безопасного удаления
            print_adv(f"[win {self.title()}] Destroying: {name}")
            self.his[name].destroy()
        for n in self.winfo_children():
            n.place_forget()
        self.his = {}
        # Принудительно обновляем окно
        self.update()

    def update(self):
        super().update()

    def __getitem__(self, item):
        return self.his[item]


class SidePanelWidget:
    def __init__(self, win: Union[Win, tkinter.Tk], style=None, _side: Literal['R', 'L'] = 'R', title: str = 'Side Panel'):
        self.his = {}
        self._title = title
        if isinstance(win, Win):
            self._win = win
        else:
            self._win = win
        self._side = _side
        self._o = None
        self._widgets = []
        if style is None:
            self._style = ['SystemButtonFace', 'SystemButtonText', 'TkDefaultFont']
        else:
            self._style = style
        self._font = tuple(self._style[2].split(':'))
        if len(self._font) == 1:
            self._font = (self._style[2])
        print(f'[side {self._title}] IMPORTANT !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! -> font!!! :{self._font} style {style}')

    def build(self):
        print_adv(f'[side {self._title}] BUILDING')
        size = self._win.geometry().split('+')[0].split('x')
        size_x = int(size[0])
        size_y = int(size[1])
        pos_x = 0
        if self._side == 'L':
            pos_x = size_x - size_x // 3  # Используем целочисленное деление

        print_adv(f'[side {self._title}] CANVAS PROCESS')
        if not isinstance(self._win, Win):
            self._o = tkinter.Canvas(self._win, bg=self._style[0], height=size_y, width=size_x // 3)
        else:
            self._o = self._win.create(f'side-panel-_o-root${self._title}$', tkinter.Canvas, bg=self._style[0], height=size_y, width=size_x // 3).tk
        self._o.place(x=pos_x, y=0)

        print_adv(f'[side {self._title}] BASE BUTTONS')
        close_btn = tkinter.Button(self._o, text='X', command=self.destroy, bg=self._style[0], fg=self._style[1], font=self._font)
        self._o.create_window(10, 15, window=close_btn)

        title_label = tkinter.Label(self._o, text=self._title, bg=self._style[0], fg=self._style[1], font=self._font)
        self._o.create_window(25, 15, window=title_label, anchor='w')

        print_adv(f'[side {self._title}] CUSTOM WIDGETS')
        self._custom_create()
        self.his.update({'_O': self._o})
        print_adv(f'[side {self._title}] BUILD')

    def create(self, widget, x, y, name: str = '',  **kw):
        if self._o is None and {'widget': widget, 'x': x, 'y': y, 'name': name, 'kw': kw} not in self._widgets:
            if name != '':
                print_adv(f'[side {self._title}] p recreating {name}')
            else:
                try:
                    print_adv(f'[side {self._title}] p recreating empty name text={widget["text"]}')
                except TclError:
                    print_adv(f'[side {self._title}] p recreating empty name')
            self._widgets.append({'widget': widget, 'x': x, 'y': y, 'name': name, 'kw': kw})
        else:
            print_adv(f'[side {self._title}] creating {name}')
            # Если виджет уже имеет родителя, создаем копию
            if name != '':
                print_adv(f'[side {self._title}] NAME EXISTS')
                self.his.update({name: {'widget': widget, 'x': x, 'y': y, 'kw': kw}})
            if not isinstance(widget, int):
                if widget.winfo_exists() and widget.winfo_parent():
                    new_widget = self._create_widget_copy(widget)
                    item = self._o.create_window(x, y, window=new_widget, **kw)
                else:
                    widget.configure(bg=self._style[0], fg=self._style[1], font=self._font)
                    item = self._o.create_window(x, y, window=widget, **kw)
                self._o.tag_raise(item)
            else:
                item = widget
            return item

    def _custom_create(self):
        """Создает все отложенные виджеты"""
        # Удаляем старые виджеты
        #for widget_info in self._widgets[:]:
        #    if isinstance(widget_info['widget'], tkinter.Widget):
        #        widget_info['widget'].destroy()
        #self._widgets.clear()

        # Создаем новые
        for widget_info in self._widgets:
            self.create(widget_info['widget'], widget_info['x'], widget_info['y'], widget_info['name'],
                        **widget_info['kw'])

    def destroy(self):
        """Уничтожает панель"""
        for item in self._widgets:
            try:
                if isinstance(item['widget'], tkinter.Widget):
                    item['widget'].destroy()
            except TclError:
                pass
        self._widgets.clear()  # Очищаем список виджетов
        try:
            if isinstance(self._win, Win):
                try:
                    self._win.his.pop(f'side-panel-_o-root${self._title}$')
                except KeyError:
                    pass
            if self._o:
                self._o.destroy()
        except AttributeError:
            pass
        self._o = None

    def _create_widget_copy(self, original):
        """Создает копию виджета для нового родителя"""
        widget_class = original.__class__
        config = original.configure()

        # Создаем новый виджет с теми же параметрами
        new_widget = widget_class(self._o)

        # Копируем все настройки
        for key in config:
            if key not in ['class', 'master']:
                new_widget[key] = original[key]

        # Копируем команду (если есть)
        if 'command' in original.keys():
            new_widget.config(command=original['command'])
        try:
            new_widget.config(bg=self._style[0], fg=self._style[1], font=self._font)
        except TclError:
            pass

        return new_widget


class SidePanel(SidePanelWidget):
    def __init__(self, win: Union[Win, tkinter.Tk], style=None, _side: Literal['R', 'L'] = 'R', title: str = 'Side Panel'):
        super().__init__(win, style, _side, title)
        self.custom_widgets = []

    def create_custom_widget(self, widget, x: int, y: int, name: str = '', **kw):
        self.custom_widgets.append({'widget': widget, 'x': x, 'y': y, 'name': name, 'kw': kw})

    def build(self):
        for i in self.custom_widgets:
            self.create(i['widget'], i['x'], i['y'], i['name'], **i['kw'])
        super().build()

if __name__ == '__main__':
    app = Win()
    side = SidePanel(app)
    app.create('_T_Button1', Button, text='123').build('pack')
    app.create('_T_Label1', Label, text='123').build('pack')
    app.create('_T_Entry1', Entry).build('pack')
    app.create('_T_Button2-side', Button, text='side', command=CallBack(side.build)).build('pack')
    side.create_custom_widget(Button(text='123'), 50, 50)
    app.create('_T_Button3', Button, text='destroy all w', command=CallBack(app.destroy_all_in)).build('pack')
    app.mainloop()

