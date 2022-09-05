import os
import json
import shutil
import threading
import time
from tkinter import filedialog

class StopableThread:
    def __init__(self, func,  args, timing):
        super(StopableThread, self).__init__()
        self.func = func
        self.args = args
        self.timing = timing
        self.thread = threading.Thread(target= self.loop, daemon= True)

    def loop(self):
        if self.args is not None:
            while self.running:
                self.func(self.args)
                time.sleep(self.timing)
        else:
            while self.running:
                self.func()
                time.sleep(self.timing)

    def run(self):
        self.running = True
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join(timeout= self.timing)


class FileManager:
    def __init__(self):
        super(FileManager, self).__init__()
    def check_file(self):
        command_list = []
        if os.path.exists('commandlist.json'):
            with open('commandlist.json', 'r') as f:
                command_list = json.load(f)
                if type(command_list) is not list:
                    command_list = []
        return command_list

    def save_file(self, command_list):
        with open('commandlist.json', 'w') as f:
            json.dump(command_list, f)

    def save_as(self, command_list):
       path = filedialog.asksaveasfile(mode= 'w', defaultextension= '.json', initialfile='commandlist', confirmoverwrite= True)
       if path is not None:
           path.write(json.dumps(command_list))

    def open_file(self):
        path = filedialog.askopenfilename(defaultextension='.json')
        with open(path, 'r', encoding= 'utf8') as f:
            command_list = json.load(f)
            if type(command_list) is not list:
                return
        return command_list

    def copy_dir(self, command_list, token):
        dst_path = filedialog.askdirectory()
        if os.path.exists(dst_path):
            dst_path = dst_path+'/bot'
        else:
            return
        src_path = os.getcwd()+'/bot'
        shutil.copytree(src_path, dst_path)
        with open(dst_path+ '/commandlist.json', 'w') as f:
            json.dump(command_list, f)
        with open(dst_path+ '/token', 'w') as f:
            json.dump(token, f)