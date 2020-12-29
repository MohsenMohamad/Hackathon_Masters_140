import keyboard
import threading
import time

finished = False


def on_key_release(key):
    print(key.name)


def el_x():
    keyboard.on_release(callback=on_key_release)
    if finished:
        return


if __name__ == '__main__':
    z = threading.Thread(target=el_x)
    z.start()
    time.sleep(5)
    finished = True
    print("killed thread")

