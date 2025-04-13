from doctest import master
from tkinter import Canvas, TclError
import tkinter
from typing import Literal, Optional, List, Dict, Union

def _pass():
    pass

class Widget:
    def __init__(self, **kwargs):
        self._root_win = kwargs['_wid']
        self.tk = kwargs['_obj']
        self._kwargs = kwargs

    def build(self, mode: Literal['place', 'grid', 'pack'], **kwargs):
        if mode == 'place':
            self.tk.place(**kwargs)
        elif mode == 'grid':
            self.tk.grid(**kwargs)
        elif mode == 'pack':
            self.tk.pack(**kwargs)

    def destroy(self):
        self.tk.destroy()

    def configure(self, **kwargs):
        self.tk.configure(**kwargs)


class CallBack:
    def __init__(self, target = _pass):
        self.Target = target


class ProgressBar(tkinter.Label):
    def __init__(self, style=None, **kwargs):
        if style is None:
            style = ['white', 'black', 'Segoe UI:10']
        super().__init__(bg=style[0], fg=style[1], font=tuple(style[2].split(':')), **kwargs)
        self.percentage = 0
        self._progress = "." * 100
        self['text'] = f'[{self._progress}] {self.percentage}/100'

    def plus(self, v=1):
        if self.percentage < 100:
            self.percentage += v
            self._progress = '|' * self.percentage + '.' * (100 - self.percentage)
            self['text'] = f'[{self._progress}] {self.percentage}/100'
        else:
            self['text'] = f'[{self._progress}] Completed'
        self.update()


class Button(tkinter.Button):
    def __init__(self, style=None, command: CallBack = CallBack(), **kwargs):
        if style is None:
            style = ['white', 'black', 'Segoe UI:10']
        super().__init__(command=command.Target, bg=style[0], fg=style[1], font=tuple(style[2].split(':')), **kwargs)


class Label(tkinter.Label):
    def __init__(self, style=None, **kwargs):
        if style is None:
            style = ['white', 'black', 'Segoe UI:10']
        super().__init__(bg=style[0], fg=style[1], font=tuple(style[2].split(':')), **kwargs)


class Text(tkinter.Text):
    def __init__(self, style=None, **kwargs):
        if style is None:
            style = ['white', 'black', 'Segoe UI:10']
        super().__init__(bg=style[0], fg=style[1], font=tuple(style[2].split(':')), **kwargs)


class Entry(tkinter.Entry):
    def __init__(self, style=None, **kwargs):
        if style is None:
            style = ['white', 'black', 'Segoe UI:10']
        super().__init__(bg=style[0], fg=style[1], font=tuple(style[2].split(':')), **kwargs)


POSSIBLE_WIDGETS = [Label, Button, Text, Entry, ProgressBar]
POSSIBLE_WIDGETS_TK = [tkinter.Label, tkinter.Button, tkinter.Text, tkinter.Entry]


class Win:
    def __init__(self, **kwargs):
        self.wid = tkinter.Tk(**kwargs)
        self.his = {}

    def build(self) -> tkinter.Tk:
        return self.wid

    def create(self, name: str, obj: POSSIBLE_WIDGETS, **kwargs) -> Widget:
        self.his.update({name: Widget(_wid=self.wid, _obj=obj(**kwargs))})
        return self.his[name]

    def create_abstract(self, name: str, obj: CallBack):
        self.his.update({name: obj})


class SidePanel:
    def __init__(self, win: Union[Win, tkinter.Tk], style=None, side: Literal['R', 'L'] = 'R', title: str = 'Side Panel'):
        self.his = []
        self._title = title
        if isinstance(win, Win):
            self._win = win.wid
        else:
            self._win = win
        self._side = side
        self._o = None
        self._widgets = []
        if style is None:
            self._style = ['white', 'black', 'Segoe UI:10']
        else:
            self._style = style
        self._font = tuple(self._style[2].split(':'))

    def build(self):
        print('BUILDING')
        size = self._win.geometry().split('+')[0].split('x')
        size_x = int(size[0])
        size_y = int(size[1])
        pos_x = 0
        if self._side == 'L':
            pos_x = size_x - size_x // 3  # Используем целочисленное деление

        print('CANVAS PROCESS')
        self._o = tkinter.Canvas(self._win, bg=self._style[0], height=size_y, width=size_x // 3)
        self._o.place(x=pos_x, y=0)

        print('BASE BUTTONS')
        close_btn = tkinter.Button(self._o, text='X', command=self.destroy, bg=self._style[0], fg=self._style[1], font=self._font)
        self._o.create_window(10, 15, window=close_btn)

        title_label = tkinter.Label(self._o, text=self._title, bg=self._style[0], fg=self._style[1], font=self._font)
        self._o.create_window(25, 15, window=title_label, anchor='w')

        print('CUSTOM WIDGETS')
        self._custom_create()
        self.his.append(self._o)
        print('BUILDED')

    def create(self, widget, x, y, **kw):
        if self._o is None:
            self._widgets.append({'widget': widget, 'x': x, 'y': y, 'kw': kw})
        else:
            # Если виджет уже имеет родителя, создаем копию
            if widget.winfo_parent():
                new_widget = self._create_widget_copy(widget)
                item = self._o.create_window(x, y, window=new_widget, **kw)
            else:
                widget.configure(bg=self._style[0], fg=self._style[1], font=self._font)
                item = self._o.create_window(x, y, window=widget, **kw)
            self._o.tag_raise(item)
            return item

    def _custom_create(self):
        """Создает все отложенные виджеты"""
        for widget_info in self._widgets:
            self.create(widget_info['widget'], widget_info['x'], widget_info['y'], **widget_info['kw'])

    def destroy(self):
        """Уничтожает панель"""
        for item in self.his:
            item.destroy()
        self._o = None
        self._widgets = []

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