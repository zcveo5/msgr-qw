from tkinter import *
app = None

class Main:
    @staticmethod
    def give_data(v):
        global app
        app = v

    @staticmethod
    def execute():
        app.main.create('bypass_button', Button, text='bypass', command=app.main.quit, recreate_if_exists=True).build('place', x=0, y=0)