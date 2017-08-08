import time
import requests
import os
import os.path as path
from tkinter import filedialog
from tkinter import *

url = 'http://checkip.amazonaws.com'
timeout = 1800
config = 'config.txt'


def get_file():
    if os.name == 'posix':
        print("You are using Linux")
        root = Tk()
        root.filename = filedialog.asksaveasfilename(initialdir = "~/",title = "Select file",filetypes = (("text files","*.txt"),("all files","*.*")))
        root.destroy()
        return root.filename
    elif os.name == 'nt':
        print("You are using Windows")
        root = Tk()
        root.filename = filedialog.asksaveasfilename(initialdir = "C:/",title = "Select file",filetypes = (("text files","*.txt"),("all files","*.*")))
        root.destroy()
        return root.filename
    else:
        root = Tk()
        error = Label(toplevel, text="Your OS is unsupported :'(",height=0, width=100).pack()


def configuration():
    # Create new config
    file = ""
    if not path.isfile(config):
        cfg = open(config, 'w+')
        file = get_file()
        cfg.write(file)
        cfg.close()
    else:
        # Check config on start
        cfg = open(config, 'r')
        data = cfg.read()
        file = data
        cfg.close()
    return file

file_path = configuration()

def get_pub_ip():
    curr_ip = requests.get(url)
    conf = open(file_path, 'r')
    old_ip = conf.read()
    conf.close()
    if curr_ip.text == old_ip:
        print("Pausing 1hr..")
        time.sleep(timeout)
    else:
        f = open(file_path, 'w+')
        f.write(curr_ip.text)
        f.close()


def loop():
    while True:
        print("Running..")
        get_pub_ip()
        print("Pausing 30min..")
        time.sleep(timeout)


def start():
    try:
        print("IP Updater")
        loop()
    except KeyboardInterrupt:
        print("\nExiting..")


if __name__ == '__main__':
    start()
