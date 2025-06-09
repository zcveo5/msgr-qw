# BTAE Auth module. PLEASE DONT EDIT
# downloaded from msgr-patches for 3.8!
import socket
import os

def print_adv(v):
    print(f'[{os.path.basename(__file__)}]{v}')



client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ips = []

class User:
    def __init__(self, usr: str, passw: str, host: str, port: int, null_user: bool = False):
        if not null_user:
            connect(host, port)

        self.null = null_user
        self.username = usr
        self.password = passw

    def get_data(self):
        if not self.null:
            dats = login(self.username, self.password)
            return dats
        else:
            return True, {}

    def update_personal_config(self, data: [str, str]):
        update_personal_conf(self.username, data)

    def is_user_in_db(self):
        return is_user_in_db(self.username)

    @staticmethod
    def get_modlist():
        return raw_request({'action': 'modlist'})

def connect(host: str, port: int):
    global ips
    client_socket.connect((host, port))
    ips = [host, port]


def disconnect():
    global client_socket
    try:
        client_socket.shutdown(socket.SHUT_RDWR)
    except OSError as _ex:
        if str(_ex) != '[WinError 10057] A request to send or receive data was disallowed because the socket is not connected and (when sending on a datagram socket using a sendto call) no address was supplied':
            print(f'sock close os exc ({_ex})')
    except Exception as _ex:
        print(f'sock close exc ({_ex})')
    client_socket.close()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def raw_request(req: dict) -> str:
    to_send = req
    try:
        client_socket.send(f"{to_send}".encode('utf-8'))
    except Exception as _ex:
        return str({'status': 'error', 'err': f'{type(_ex)}'})
    serv_ans = None
    count_sim = 0
    last = None
    while serv_ans is None:
        try:
            serv_ans = client_socket.recv(1024)
        except Exception as recv_ex:
            print_adv(f'[auth] rr exc {recv_ex}')
            if last is type(recv_ex):
                count_sim += 1
            last = type(recv_ex)
            if count_sim > 10:
                break
    return serv_ans.decode('utf-8')



def login(username, password):
    answer = eval(raw_request({'username': username, 'password': password}))
    if answer['status'] != 'ok':
        return False, answer
    if answer['answer'] == 'blocked':
        return True, {'status': 'error', 'answer': 'global block'}
    if password == answer['answer']['password']:
        if answer['status'] != 'ok':
            return False, answer
        else:
            return True, answer
    else:
        return False, {'status': 'error', 'answer': 'Incorrect password'}


def update_personal_conf(username, data):
    raw_request({'username': username, 'action': f'update_data:{data[0]}:{data[1]}'})


def is_user_in_db(username):
    return raw_request({'username': username, 'action': '_in_db'})['answer']


def is_my_ver_actual(a):
    return raw_request({'non-login-action': f'confirm_ver!{a}'})
