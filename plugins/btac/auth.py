# BTAE Auth module. PLEASE DONT EDIT

import socket

app = None
class AuthPlugin:
    @staticmethod
    def give_data(v):
        global app
        app = v

    @staticmethod
    def execute():
        pass

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ips = []

class User:
    def __init__(self, usr: str, passw: str, host: str, port: int):
        connect(host, port)
        self.username = usr
        self.password = passw

    def get_data(self):
        dats = login(self.username, self.password)
        return dats

    def update_personal_config(self, data: [str, str]):
        update_personal_conf(self.username, data)

    def is_user_in_db(self):
        return is_user_in_db(self.username)

    @staticmethod
    def get_modlist():
        return _request({'action': 'modlist'})

def connect(host: str, port: int):
    global ips
    client_socket.connect((host, port))
    ips = [host, port]


def _request(req: dict) -> dict:
    to_send = req
    try:
        client_socket.send(f"{to_send}".encode('utf-8'))
    except Exception as _ex:
        return {'status': 'error', 'err': f'{type(_ex)}'}
    serv_ans = None
    count_sim = 0
    last = None
    while serv_ans is None:
        try:
            serv_ans = client_socket.recv(1024)
        except Exception as recv_ex:
            if last is type(recv_ex):
                count_sim += 1
            last = type(recv_ex)
            if count_sim > 10:
                break
    try:
        return eval(serv_ans.decode('utf-8'))
    except (NameError, SyntaxError):
        return {'status': 'error', 'err': 'NameError, Server is sent a string'}



def login(username, password):
    answer = _request({'username': username, 'password': password})
    print(answer)
    if answer['status'] != 'ok':
        return False, answer
    if answer['answer'] == 'blocked':
        return True, 'blocked'
    if password == answer['answer']['password']:
        if answer['status'] != 'ok':
            return False, answer
        else:
            return True, answer
    else:
        return False, 'password'


def update_personal_conf(username, data):
    _request({'username': username, 'action': f'update_data:{data[0]}:{data[1]}'})


def is_user_in_db(username):
    return _request({'username': username, 'action': '_in_db'})['answer']


def is_my_ver_actual(a):
    return _request({'non-login-action': f'confirm_ver!{a}'})