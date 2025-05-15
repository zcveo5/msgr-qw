import json
import socket
import threading
from typing import Any
import os

from plugins.core.mod import JsonObject


def print_adv(v):
    print(f'[{os.path.basename(__file__)}]{v}')

chat_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
online_list = []
cl = None

if os.path.exists('./plugins/btac/chatHistory.json'):
    hist = json.load(open('./plugins/btac/chatHistory.json'))
    msgs = hist['msgs']
    private_msgs = hist['private_msgs']
    loaded_msgs = hist['msgs']
    loaded_private_msgs = hist['private_msgs']
else:
    msgs = []
    private_msgs = {}
    loaded_msgs = []
    loaded_private_msgs = {}

class Chat:
    def __init__(self, addr: str, port: int):
        global cl
        self.ip = (addr, port)
        cl = self

    def connect(self):
        chat_sock.connect(self.ip)

    def send(self, data: Any):
        if isinstance(data, dict):
            if 'text' in data:
                if 'to_cl' not in data:
                    msgs.append(f'You: {data["text"]}')
                else:
                    msgs.append(f'You to {data["to_cl"]}: {data["text"]}')
                    if data["to_cl"] not in private_msgs:
                        private_msgs.update({data["to_cl"]: [f'You: {data["text"]}']})
                    else:
                        private_msgs[data["to_cl"]].append(f'You: {data["text"]}')
        self.backup()
        try:
            chat_sock.send(f'{data}'.encode('utf-8'))
        except OSError:
            pass

    def async_recv(self):
        while True:
            global online_list
            try:
                recv = chat_sock.recv(1024).decode('utf-8')
            except (ConnectionError, OSError):
                break
            try:
                recv_eval = []
                try:
                    recv_eval = eval(recv)
                except TypeError:
                    pass
                if isinstance(recv_eval, list):
                    if 'Online:' in recv_eval:
                        online_list = recv_eval
            except (NameError, SyntaxError):
                if 'PRIVATE: ' not in recv:
                    msgs.append(recv)
                if 'PRIVATE: ' in recv:
                    tmp = recv.replace('PRIVATE: ', '')
                    if tmp.split(': ')[0] not in private_msgs:
                        private_msgs.update({tmp.split(': ')[0]: [tmp.split(': ')[0] + ': ' + tmp.split(': ')[1]]})
                    else:
                        private_msgs[tmp.split(': ')[0]].append(tmp.split(': ')[0] + ': ' + tmp.split(': ')[1])
                self.backup()

    @staticmethod
    def shutdown(how):
        try:
            chat_sock.shutdown(how)
        except OSError:
            pass


    @staticmethod
    def close():
        chat_sock.close()

    @staticmethod
    def backup():
        backup_path = './plugins/btac/chatHistory.json'
        with open(backup_path, 'w'):
            pass
        json.dump({'msgs': msgs, 'private_msgs': private_msgs}, JsonObject(open(backup_path, 'w')))


