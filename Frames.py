from tkinter import *
from tkinter import ttk
from ttkthemes import *
import threading
import Settings
import pystray
from PIL import Image
from os import getcwd

VERSION = '1.0'
ABOUT = f'Developer: P. Magatte Sady\nVersion: {VERSION}\nModules: Python requests, Python ttkthemes, Python pystray\nRepository: https//www.github.com'
IMG_DICT = {'function': 'send photo', 'media label': 'Enter image id(no limit) or url(limit 5mb)', 'type' : 'photo'}
VDO_DICT = {'function': 'send video', 'media label': 'Enter video id(no limit) or url(limit 20mb)', 'type' : 'video'}
DOC_DICT = {'function': 'send file', 'media label': 'Enter document id(no limit) or url(limit 20mb)', 'type' : 'document'}
MEDGRP_DICT = {'media label': 'Enter photo or video id or url'}


class NotificationWindow(Toplevel):
    def __init__(self, master, notification):
        super().__init__(master)
        self.wm_overrideredirect(1)
        self.attributes('-topmost', 1)
        frame = ttk.Frame(self)
        succes = ttk.Label(frame, text= notification)
        ok = ttk.Button(frame, text = ' ok ', command= self.destroy)
        frame.grid(column= 0, row= 0, ipadx= 10, ipady= 10, sticky='nwes')
        succes.grid(column= 0, row= 0, pady= 5, padx= 20)
        ok.grid(column= 0, row= 1, pady= 5, padx= 20)
        self.update_idletasks()
        wingeo = self.geometry().replace('x', '+').split('+')
        winx, winy = int(int(wingeo[0])/2), int(int(wingeo[1])/2)
        w, h = int(master.winfo_width()/2), int(master.winfo_height()/2)
        x, y = int(master.winfo_x()), int(master.winfo_y())
        self.geometry(f'+{x+w-winx}+{y+h-winy}')
        threading.Thread(target= lambda: self.after(5000, self.destroy)).start()

def succesfully_added(master):
    notification = NotificationWindow(master, 'succesfully added')
    


class TitleBar(ttk.Frame):
    def __init__(self, master, title):
        super().__init__(master)

        def set_appwindow(mainWindow):
            mainWindow.wm_withdraw()
            mainWindow.after(10, lambda: mainWindow.wm_deiconify())

        def minimize():
            master.attributes("-alpha",0)
            master.minimized = True

        def deminimize(event):
            master.attributes("-alpha",1)
            master.minimized = False 


        
        def get_pos(event):

                xwin = master.winfo_x()
                ywin = master.winfo_y()
                startx = event.x_root
                starty = event.y_root

                ywin = ywin - starty
                xwin = xwin - startx

                def move_window(event):
                    master.config(cursor="fleur")
                    master.geometry(f'+{event.x_root + xwin}+{event.y_root + ywin}')

                def release_window(event):
                    master.config(cursor="arrow")
                self.bind('<B1-Motion>', move_window)
                self.bind('<ButtonRelease-1>', release_window)
                self.title.bind('<B1-Motion>', move_window)
                self.title.bind('<ButtonRelease-1>', release_window)  


        master.bind("<FocusIn>",deminimize)  
        master.after(10, lambda: set_appwindow(master))                   


        self.close = ttk.Button(self, text='×', command= master.destroy,)
        self.minimize = ttk.Button(self, text='🗕',command=minimize)
        self.title = ttk.Label(self, text= title)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
        self.close.pack(side=RIGHT,ipadx=7,ipady=1)
        self.minimize.pack(side=RIGHT,ipadx=7,ipady=1)
        self.title.pack(side=LEFT, padx=10)
        self.bind('<Button-1>', get_pos)
        self.title.bind('<Button-1>', get_pos)



class TokenMenu(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.token_frame = ttk.Frame(self)
        self.token_label = ttk.Label(self.token_frame, text = "Insert valide bot's token")
        self.token_entry = ttk.Entry(self.token_frame, width= 50)
        self.validate_token = ttk.Button(self, text = " validate")
        #----------------------------------------------------------------------------
        self.token_frame.grid(column= 0, row= 0, pady= 10)
        self.token_label.grid(column= 0, row= 0, sticky= 'w')
        self.token_entry.grid(column= 0, row= 1)
        self.validate_token.grid(column= 0, row= 1, pady= 10)


        

class ManagementFrame(ttk.Frame):
    def __init__(self, master, list):
        super().__init__(master)
        self.list = list
        
        def add_commands():
            tplvl = AddCommand(master, list)
            self.add.configure(state = DISABLED) 
            master.wait_window(tplvl)
            self.add.configure(state = NORMAL)
            self.delete_all_items()
            self.display()




        def delete_item():
            if len(self.treeview.selection()) < 1:
                notification = NotificationWindow(self, 'select an item')
                return
            if len(list) < 1:
                notification = NotificationWindow(self, 'select an item')
                return
            if len(self.treeview.selection()) > 1:
                selected_list = []
                selected = self.treeview.selection()
                for items in selected:
                    item = list[int(items)]
                    selected_list.append(item)

                for dict in selected_list:
                    del(list[list.index(dict)])
                    
                self.delete_all_items()
                self.display()
                return
            selected = int(self.treeview.focus())
            del(list[selected])
            self.delete_all_items()
            self.display()
            return

        self.tree_frame = ttk.Frame(self)
        self.tree_frame.pack()
        self.scrollbar = ttk.Scrollbar(self.tree_frame, orient='vertical')
        self.scrollbar.pack(side= 'right', fill='y')
        self.treeview = ttk.Treeview(self.tree_frame, yscrollcommand= self.scrollbar.set)
        self.treeview['column'] = ('command', 'command type',  'caption/message', 'media')
        self.treeview.column('#0',width= 0, minwidth= 0, stretch= NO)
        self.treeview.column('command', width= 300, minwidth= 50)
        self.treeview.column('command type', width= 300, minwidth= 50)
        self.treeview.column('caption/message', width= 300, minwidth= 50)
        self.treeview.column('media', width= 300, minwidth= 50)
        self.treeview.heading('#0')
        self.treeview.heading('command', text= 'command')
        self.treeview.heading('command type', text= 'command type')
        self.treeview.heading('caption/message', text= 'caption/message')
        self.treeview.heading('media', text= 'media')
        self.treeview.pack()
        self.scrollbar.configure(command= self.treeview.yview) 
        self.display()
        #--------------------------------------------------------------------------------
        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(expand= 1, fill= 'x')
        self.add = ttk.Button(self, text = 'add command',command= add_commands)
        self.delete = ttk.Button(self, text = 'delete',command= delete_item)
        self.add.pack(side= RIGHT)
        self.delete.pack(side= LEFT)
        #--------------------------------------------------------------------------------------------------------------
    def delete_all_items(self):
        if len(self.treeview.get_children())< 1:
            return
        for item in self.treeview.get_children():
            self.treeview.delete(item)

    def display(self):
        id = 0
        for dic in self.list:
            if type(dic) is not dict:
                continue
            if dic.get('function') == 'send media group':
                self.treeview.insert(parent='', index= 'end', text='',iid = id, values= (dic.get('name'), dic.get('function'), None, dic.get('args').get('media')))
                id = id+1
            elif dic.get('function') == 'send message':
                self.treeview.insert(parent='', index= 'end', text='',iid = id, values= (dic.get('name'), dic.get('function'), dic.get('args').get('text'), None))
                id = id+1
            elif dic.get('function') == 'send photo' or 'send video' or 'send document':
                medias = ['photo', 'video', 'document']
                for media in medias:
                    if dic.get('args').get(media):
                        self.treeview.insert(parent='', index= 'end', text='',iid = id, values= (dic.get('name'), dic.get('function'), dic.get('args').get('caption'), dic.get('args').get(media)))
                id = id+1



class SendMessage(ttk.Frame):
    def __init__(self, master, cmd_list):
        super().__init__(master)
        def sendmsg():
            name = self.command_name.get()
            text = self.message.get('1.0', 'end-1c')
            function= 'send message'

            if len(name) < 1:
                self.nameerror.grid(column= 0, row= 0, sticky= 'w')
                self.nameerror.tkraise()
                threading.Thread(target= lambda: self.nameerror.after(5000, self.nameerror.grid_forget)).start()
                



            if len(name) > 0:
                self.nameerror.grid_forget()


            if len(text) < 1:
                self.messageerror.grid(column= 0, row= 0, sticky= 'w')
                self.messageerror.tkraise()
                threading.Thread(target= lambda: self.messageerror.after(5000, self.messageerror.grid_forget)).start()


            if len(text) > 0:
                self.messageerror.grid_forget()

            if len(text) > 4096:
                notification = NotificationWindow(self, f'chararchter {len(text)}/4096')
                return

            if len(name) and len(text) > 0:
                dictionary = {'name': name,
                    'function': function,
                    'args' :{'text': text}}
                cmd_list.append(dictionary)
                self.command_name.delete(0, END)
                self.message.delete('1.0', 'end')
                succesfully_added(master)
            else:
                return


        self.name_frame = ttk.Frame(self)
        self.message_frame = ttk.Frame(self)
        self.nameerror = ttk.Label(self.name_frame, text = 'Please insert a command name', foreground= 'red')
        self.messageerror = ttk.Label(self.message_frame, text = 'Please insert a message', foreground= 'red')
        self.cmd_label = ttk.Label(self.name_frame, text = ' Enter command name',)
        self.command_name = ttk.Entry(self.name_frame, width= 50)
        self.msg_label = ttk.Label(self.message_frame, text = 'Enter message')
        self.message = Text(self.message_frame, width= 40, height= 10, bg= '#555555', foreground= 'white')
        self.add = ttk.Button(self, text = 'add command',command= sendmsg)
        #--------------------------------------------------------------------
        self.name_frame.grid(column= 0, row= 0,sticky= 'w',pady= 10)
        self.message_frame.grid(column= 0, row= 1,sticky= 'w', pady= 10)
        self.cmd_label.grid(column= 0, row= 0, sticky= 'w')
        self.command_name.grid(column= 0, row= 1, sticky= 'w')
        self.msg_label.grid(column= 0, row= 0, sticky= 'w')
        self.message.grid(column= 0, row= 1)
        self.add.grid(column= 0, row= 2, pady= 10,)

class SendMedia(ttk.Frame):
    def __init__(self, master, cmd_list, media_dict):
        super().__init__(master)
        def sendmedia():
            name = self.command_name.get()
            media = self.media_entry.get()
            text = self.message.get('1.0', 'end-1c')
            function= media_dict.get('function')

            if len(name) < 1:
                self.cmd_label.grid_forget()
                self.nameerror.grid(column= 0, row= 0, sticky= 'w')
                self.nameerror.tkraise()
                threading.Thread(target= lambda: self.nameerror.after(5000, self.nameerror.grid_forget)).start()
                threading.Thread(target= lambda: self.cmd_label.after(5000, lambda: self.cmd_label.grid(column=0, row=0, sticky='w'))).start()



            if len(name) > 0:
                self.nameerror.grid_forget()


            if len(media) < 1:
                self.media_label.grid_forget()
                self.mediaerror.grid(column= 0, row= 0, sticky= 'w')
                self.mediaerror.tkraise()
                threading.Thread(target= lambda: self.mediaerror.after(5000, self.mediaerror.grid_forget)).start()
                threading.Thread(target= lambda: self.media_label.after(5000, lambda: self.media_label.grid(column=0, row=0, sticky='w'))).start()


            if len(media) > 0:
                self.mediaerror.grid_forget()

            if len(text) > 1024:
                notification = NotificationWindow(self, f'chararchter {len(text)}/1024')
                return

            if len(name) and len(media) > 0:
                dictionary = {'name': name,
                    'function': function,
                    'args' :{'caption': text, media_dict.get('type'): media}}
                cmd_list.append(dictionary)
                self.command_name.delete(0, END)
                self.media_entry.delete(0, END)
                self.message.delete('1.0', 'end')
                succesfully_added(master)
            else:
                return


        self.name_frame = ttk.Frame(self)
        self.message_frame = ttk.Frame(self)
        self.media_frame =ttk.Frame(self)
        self.nameerror = ttk.Label(self.name_frame, text = 'Please insert a command name', foreground= 'red')
        self.mediaerror = ttk.Label(self.media_frame, text = 'This field is riquered', foreground= 'red')
        self.cmd_label = ttk.Label(self.name_frame, text = ' Enter command name',)
        self.command_name = ttk.Entry(self.name_frame, width= 50)
        self.msg_label = ttk.Label(self.message_frame, text = 'Enter caption(optional)')
        self.message = Text(self.message_frame, width= 40, height= 10, bg= '#555555', foreground= 'white')
        self.media_label = ttk.Label(self.media_frame, text=media_dict.get('media label'))
        self.media_entry = ttk.Entry(self.media_frame, width = 50)
        self.add = ttk.Button(self, text = 'add command',command= sendmedia)
        #--------------------------------------------------------------------
        self.name_frame.grid(column= 0, row= 0,sticky= 'w',pady= 10)
        self.media_frame.grid(column= 0, row= 1,sticky= 'w',pady= 10)
        self.message_frame.grid(column= 0, row= 2,sticky= 'w', pady= 10)
        self.cmd_label.grid(column= 0, row= 0, sticky= 'w')
        self.command_name.grid(column= 0, row= 1, sticky= 'w')
        self.media_label.grid(column=0, row=0, sticky='w')
        self.media_entry.grid(column=0, row=1)
        self.msg_label.grid(column= 0, row= 0, sticky= 'w')
        self.message.grid(column= 0, row= 1)
        self.add.grid(column= 0, row= 3, pady= 10,)          


class SendMediaGroup(SendMedia):
    def __init__(self, master, cmd_list, media_dict):
        SendMedia.__init__(self, master, cmd_list, media_dict)
        def show_commands():
            app = Toplevel(master)
            app.resizable(False, FALSE)
            treeview = ttk.Treeview(app)
            treeview['columns'] = ('type', 'caption', 'media')
            treeview.column('#0',width= 0, minwidth= 0, stretch= NO)
            treeview.column('type', width= 120, minwidth= 25)
            treeview.column('caption', width= 120, minwidth= 25)
            treeview.column('media', width= 120, minwidth= 25)
            treeview.heading('#0', text='')
            treeview.heading('type', text= 'command')
            treeview.heading('caption', text= 'caption')
            treeview.heading('media', text= 'media')
            treeview.grid(column= 0, row= 0)
            def delete_item():
                if len(treeview.selection()) < 1:
                    notification = NotificationWindow(app, 'select an item')
                    return

                if len(self.cmd_list) < 1:
                    notification = NotificationWindow(app, 'select an item')
                    return
                if len(treeview.selection()) > 1:
                    selected = treeview.selection()
                    for each in selected:
                        items = treeview.item(each, 'values')
                        selected_dict = {'type':items[0],'caption': items[1], 'media': items[2]}
                        del(self.cmd_list[self.cmd_list.index(selected_dict)])
                        treeview.delete(each)
                        treeview.selection_clear()
                    return
                selected = treeview.focus()
                items = treeview.item(selected, 'values')
                selected_dict = {'type':items[0],'caption': items[1], 'media': items[2]}
                del(self.cmd_list[self.cmd_list.index(selected_dict)])
                treeview.delete(selected)
                treeview.selection_clear()
                return

            def delete_all_items():
                for item in treeview.get_children():
                    treeview.delete(item)
    

            def add_all_media():
                if len(self.cmd_list) <= 1:
                    notification = NotificationWindow(app, 'require more media')
                    return
                media = self.cmd_list.copy()
                
                name = self.command_name.get()
                dict = {
                    'name' : name, 
                    'function': 'send media group',
                    'args' : {'media' : media}
                }
                cmd_list.append(dict)
                self.cmd_list.clear()
                delete_all_items()
                self.name_frame.grid(column= 0, row= 0,sticky= 'w',pady= 10)
                self.command_name.delete(0, END)
                notification = NotificationWindow(app, 'media group added')
    

            idd = 0
            for cmd in self.cmd_list:
                treeview.insert(parent='', index= 'end', text='',iid = idd, values= (cmd.get('type'), cmd.get('caption'), cmd.get('media')))
                idd = idd + 1
            tree_buttons_frame = ttk.Frame(app)
            tree_buttons_frame.grid(column= 0, row= 1, sticky= 'nsew')
            del_button = ttk.Button(tree_buttons_frame, text= 'delete', command= delete_item)
            add_media_button = ttk.Button(tree_buttons_frame, text= 'add media group', command= add_all_media)
            del_button.grid(column= 0, row= 0, padx= 40)
            add_media_button.grid(column= 2, row= 0, padx= 40)


        def add_media():
            name = self.command_name.get()
            media = self.media_entry.get()
            type = self.type_box.get()
            text = self.message.get('1.0', 'end-1c')

            if len(name) < 1:
                self.cmd_label.grid_forget()
                self.nameerror.grid(column= 0, row= 0, sticky= 'w')
                self.nameerror.tkraise()
                threading.Thread(target= lambda: self.nameerror.after(5000, self.nameerror.grid_forget)).start()
                threading.Thread(target= lambda: self.cmd_label.after(5000, lambda: self.cmd_label.grid(column=0, row=0, sticky='w'))).start()
 
            if len(name) > 0:
                self.nameerror.grid_forget()
                self.name_frame.grid_forget()

            if len(media) < 1:
                self.media_label.grid_forget()
                self.mediaerror.grid(column= 0, row= 0, sticky= 'w')
                self.mediaerror.tkraise()
                threading.Thread(target= lambda: self.mediaerror.after(5000, self.mediaerror.grid_forget)).start()
                threading.Thread(target= lambda: self.media_label.after(5000, lambda: self.media_label.grid(column=0, row=0, sticky='w'))).start()

            if len(media) > 0:
                self.mediaerror.grid_forget()

            if len(text) > 1024:
                notification = NotificationWindow(master, f'chararchter {len(text)}/1024')
                return

            if len(self.cmd_list) == 10:
                notification = NotificationWindow(master, f'max media 10/10')
                return

            if len(media) > 0:
                dictionary = {
                    'type' : type,
                    'caption': text,
                    'media': media}
                self.cmd_list.append(dictionary)
                self.media_entry.delete(0, END)
                self.message.delete('1.0', 'end')
                succesfully_added(master)
            else:
                return
            
        types = ['photo', 'video']
        self.add.grid_forget()
        self.cmd_list = []
        self.type_frame = ttk.Frame(self)
        self.type_label = ttk.Label(self.type_frame, text= 'choose a file type')
        self.type_box = ttk.Combobox(self.type_frame, values= types, height= 5)
        self.type_box.current(0)
        self.buttons_frame = ttk.Frame(self)
        self.media_list = ttk.Button(self.buttons_frame, text= 'media list', command= show_commands)
        self.add_media = ttk.Button(self.buttons_frame, text= 'add media', command= add_media)
        #-----------------------------------------------------------------------
        self.type_frame.grid(column= 0, row= 3, pady= 10, sticky= 'w')
        self.type_label.grid(column= 0, row= 0, sticky= 'w')
        self.type_box.grid(column= 0, row= 1)
        self.buttons_frame.grid(column= 0, row= 4, padx= 10)
        self.media_list.grid(column= 0, row= 0, sticky= 'w')
        self.add_media.grid(column= 1, row= 0, sticky= 'e')


class AddCommand(Toplevel):
    def __init__(self, master, cmd_list):
        super().__init__(master)
        self.resizable(False, False)
        def choose_frame(event):
            frame = self.box.get()
            self.frames.get(frame).tkraise()

        self.send_msg = SendMessage(self, cmd_list)
        self.send_img = SendMedia(self, cmd_list, IMG_DICT)
        self.send_vid = SendMedia(self, cmd_list, VDO_DICT)
        self.send_doc = SendMedia(self, cmd_list, DOC_DICT)
        self.send_mdgr = SendMediaGroup(self, cmd_list, MEDGRP_DICT)

        self.frames = {
            'send message'     : self.send_msg,
            'send image'       : self.send_img,
            'send video'       : self.send_vid,
            'send file'        : self.send_doc,
            'send media group' : self.send_mdgr,
        }

        options = list(self.frames.keys())
        self.box = ttk.Combobox(self, values= options, width= 50)
        self.box.grid(column= 0, row= 0)
        self.box.current(0)
        self.box.bind('<<ComboboxSelected>>', choose_frame)
        
        for frame in self.frames:
            self.frames[frame].grid(column= 0, row= 1,sticky= 'nwes')
        self.send_msg.tkraise()

class MenuBar(ttk.Frame):
    def __init__(self, master, list):
        super().__init__(master)
        def hide_window():
            master.withdraw()
            menu = (pystray.MenuItem('quit',lambda: exit(master, icon)),pystray.MenuItem('show', lambda: show_window(master, icon)))
            image = Image.open('Telebot.ico')
            icon = pystray.Icon('Telegram bot manager',image, 'Telebot', menu)
            icon.run()

        def exit(master, icon):
            master.destroy()
            icon.stop()

        def show_window(master, icon):
            icon.stop()
            master.after(0, master.deiconify())


        def about():
            tplvl = About(master)
            self.about_menu.entryconfig('About', state = DISABLED)
            master.wait_window(tplvl)
            self.about_menu.entryconfig('About', state = NORMAL)

        self.menu_bar = Menu(master, background= 'black', foreground='white')
        master.config(menu= self.menu_bar)

        self.files_menu = Menu()
        self.menu_bar.add_cascade(label= 'Files', menu= self.files_menu)
        self.files_menu.add_command(label= 'Save commands',command=lambda: Settings.FileManager().save_as(list))
        self.files_menu.add_command(label= 'Load commands')
        self.files_menu.add_command(label= 'Get server files',)
        self.files_menu.add_command(label='Add command list')
        self.files_menu.add_command(label= 'Exit', command= quit)

        self.server_menu = Menu(self.menu_bar)
        self.menu_bar.add_cascade(label= 'Server', menu= self.server_menu)
        self.server_menu.add_command(label= 'Token')
        self.server_menu.add_command(label= 'Run bot')
        self.server_menu.add_command(label= 'Stop bot')
        self.server_menu.add_command(label= 'Run in background', command= hide_window)

        self.about_menu = Menu()
        self.menu_bar.add_cascade(label= 'About', menu= self.about_menu)
        self.about_menu.add_command(label= 'About', command= about)


class About(Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.resizable(False, False)
        frame = ttk.Frame(self)
        name = ttk.Label(frame, font= 'bold', text= 'Telegram Bot Manager', justify='center').pack(ipady= 20)
        label = ttk.Label(frame, text= ABOUT, justify= 'left').pack()
        frame.pack(ipadx= 20, ipady= 20)
        
    
class StatusBar(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.status_var = StringVar(value= 'loading')
        self.server_status = ttk.Label(self, textvariable= self.status_var )
        self.version = ttk.Label(self, text= f'version: {VERSION} ')
#-----------------------------------------------------------------------------------------
        self.server_status.pack(side= LEFT)
        self.version.pack(side= RIGHT)



class MainWindow(ThemedTk):
    def __init__(self, list):
        icon = getcwd() +'\Telebot.ico'
        super().__init__(theme= 'equilux')
        self.iconbitmap(icon)
        self.frame = ttk.Frame(self)
        self.frame.pack()
        self.status_bar = StatusBar(self)
        self.status_bar.pack(fill='x', expand=1, ipady= 10)
        self.token = TokenMenu(self.frame)
        self.manage =ManagementFrame(self.frame, list)
        self.menu = MenuBar(self, list)
        self.menu.server_menu.entryconfig('Token', command = self.show_token)
        self.manage.grid(column= 0, row= 0)

    def show_token(self):
        self.manage.grid_forget()
        self.token.grid(column= 0, row= 0) 
        self.menu.server_menu.entryconfig('Token', label = 'Commands')
        self.menu.server_menu.entryconfig('Commands', command = self.show_manage)
                

    def show_manage(self):
        self.token.grid_forget()
        self.manage.grid(column= 0, row= 0)
        self.menu.server_menu.entryconfig('Commands', label = 'Token')
        self.menu.server_menu.entryconfig('Token', command = self.show_token)


            
if __name__ == '__main__':
    cmd_list = []
    app = MainWindow(cmd_list)
    app.mainloop()