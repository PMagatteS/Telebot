import Frames
import Settings
import Telegrambot
from configparser import ConfigParser

config = ConfigParser()
config.read('Telebot.ini')
command_list = Settings.FileManager().check_file()
try:
    config_data = config['default']
    TOKEN = config_data['token']
except:
    TOKEN = ''

def get_token():
    entry = app.token.token_entry.get()
    if len(entry)< 1:
        Frames.NotificationWindow(app, 'token not valid')
        return False
    else:
        try:
            if Telegrambot.get_me(entry):
                global TOKEN
                TOKEN = entry
                app.show_manage()
            else:
                Frames.NotificationWindow(app, 'token not valid')
                return False
                
        except:
            Frames.NotificationWindow(app, 'check your network connection')
            return False
            

def load_commands():
    global command_list
    new_list = Settings.FileManager().open_file()
    if new_list is not None:
        command_list.clear()
        for cmd in new_list:
            command_list.append(cmd)
        app.manage.delete_all_items()
        app.manage.display()

def add_cmd_list():
    global command_list
    new_list = Settings.FileManager().open_file()
    if new_list is not None:
        for cmd in new_list:
            command_list.append(cmd)
        app.manage.delete_all_items()
        app.manage.display()
    

def connection():    
    try:
        if Telegrambot.get_me(TOKEN):
            global bot
            bot = Settings.StopableThread(Telegrambot.main, {'token': TOKEN, 'list': command_list}, 2.0)
            bot.run()
        else:
            Frames.NotificationWindow(app, 'invalid token')           
    except:
        Frames.NotificationWindow(app, 'enable to connect to network')

        
def disconection():
    if bot.thread.is_alive():
        bot.stop()


def check_bot():
    if bot.thread.is_alive():
        menu.server_menu.entryconfig('Run bot', state = 'disabled')
        menu.server_menu.entryconfig('Stop bot', state = 'normal')
        app.status_bar.status_var.set('connected')
    else:
        menu.server_menu.entryconfig('Run bot', state = 'normal')
        menu.server_menu.entryconfig('Stop bot', state = 'disabled')
        app.status_bar.status_var.set('disconnected')


def get_copy():
    Settings.FileManager().copy_dir(command_list, TOKEN)




app = Frames.MainWindow(command_list)
app.resizable(False, False)
menu = app.menu
menu.server_menu.entryconfig('Run bot', command = connection)
menu.server_menu.entryconfig('Stop bot', command = disconection)
menu.files_menu.entryconfig('Load commands', command = load_commands)
menu.files_menu.entryconfig('Get server files', command = get_copy)
menu.files_menu.entryconfig('Add command list', command = add_cmd_list)
bot = Settings.StopableThread(Telegrambot,{'token':TOKEN, 'list': command_list}, 2.0)
app.token.validate_token.config(command= get_token)
check = Settings.StopableThread(check_bot, None, 3.0)
check.run()

app.mainloop()

Settings.FileManager().save_file(command_list)
config['default'] = {"token": TOKEN}
with open('Telebot.ini', 'w') as f:
    config.write(f)

if check.thread.is_alive():
    check.stop()
if bot.thread.is_alive():   
    bot.stop()