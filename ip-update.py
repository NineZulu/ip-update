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
    yn = input("Would you like to use the GUI? y/[n]")
    if yn.lower() == "y":
        if os.name == 'posix':
            root = Tk()
            root.filename = filedialog.asksaveasfilename(initialdir = "~/",title = "Select file",filetypes = (("text files","*.txt"),("all files","*.*")))
            root.destroy()
            return root.filename
        elif os.name == 'nt':
            root = Tk()
            root.filename = filedialog.asksaveasfilename(initialdir = "C:/",title = "Select file",filetypes = (("text files","*.txt"),("all files","*.*")))
            root.destroy()
            return root.filename
    else:
        path = input("Enter the location you'd like to save your IP:\n")
        return path


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
        time.sleep(timeout)
    else:
        f = open(file_path, 'w+')
        f.write(curr_ip.text)
        f.close()
        os.system('./Dropbox-Uploader/dropbox_uploader.sh upload home-ip.txt home-ip.txt')


def loop():
    while True:
        print("Running..")
        get_pub_ip()
        time.sleep(timeout)


def start():
    try:
        print("IP Updater")
        loop()
    except KeyboardInterrupt:
        print("\nExiting..")


if __name__ == '__main__':
    start()
