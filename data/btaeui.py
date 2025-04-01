import tkinter


class ProgressBar:
    def __init__(self, obj: tkinter.Label):
        self.tk = obj
        self.percentage = 0
        self._progress = "." * 100
        self.tk['text'] = f'[{self._progress}] {self.percentage}/100'

    def i(self):
        return self.tk

    def plus(self, v=1):
        if self.percentage < 100:
            self.percentage += v
            self._progress = '|' * self.percentage + '.' * (100 - self.percentage)
            self.tk['text'] = f'[{self._progress}] {self.percentage}/100'
        else:
            self.tk['text'] = f'[{self._progress}] Completed'
        self.tk.update()