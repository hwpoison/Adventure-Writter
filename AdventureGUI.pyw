import os
import sys
import time
import configparser

from tkinter import *
from tkinter import messagebox, filedialog, font
try:
    from PIL import Image, ImageTk
except ImportError:
    print("Use to install PIL Lib: pip3 install PIL")
    sys.exit(1)

from adventure.advMain import advMain


__autor__ = "Guillermo Giménez"
__version__ = "1.2"

APP_NAME = f"Adventure Writter {__version__}"
ABOUT_TEXT = f"Creado por {__autor__}\n\n\nhttps://netixzen.blogspot.com.ar/\nPython 3.6/Tkinter 8.6☺2019"


config = configparser.ConfigParser()
if(config.read("config.ini")):
    gui_text = config['TEXT']
else:
    messagebox.showerror("ERROR!", vbn)
    sys.exit(-1)


class GameInterface():
    """
    ===Text Box===== self.textBox
    ===UserInput==== self.userEntry

    self.animatedText : Animated print text (disabled)
    """

    def __init__(self, window):
        self.adventure = advMain()

        self.frame = Frame(window)
        self.userInput = StringVar()
        self.sbvCurrentStage = StringVar()
        self.sbvCurrentStatus = StringVar()
        self.init_user_interface()
        self.frame.pack()
        self.adventure.DEBUG_INFO = True
        self.adventure.loadDictionary(config['GUI']['dictionary'])
        if config['GUI']['animated_text'] == 'True':
            self.animatedText = True
        else:
            self.animatedText = False

    def init_user_interface(self):
        # TextBox Area
        scrollbar = Scrollbar(self.frame)
        self.textBox = Text(self.frame,
                            width=73,
                            height=10,
                            border=2,
                            font='Calibri 15',
                            yscrollcommand=scrollbar.set)
        self.textBox.config(state=DISABLED, wrap="word")
        scrollbar.config(command=self.textBox.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        # Font styles
        self.textBox.tag_config('userInput', foreground='#4B1160',
                                font=('times new roman bold', 16))
        self.textBox.tag_config('failAction',
                                font=('times new roman', 16), foreground='red')
        self.textBox.tag_config('adventureText', font=('times new roman', 16))

        # User input area
        self.userEntry = Entry(self.frame,
                               textvariable=self.userInput,
                               width=67,
                               font=('times new roman', 16),
                               border=0,
                               state=DISABLED)
        self.textBox.pack(padx=10)
        self.userEntry.pack(padx=10, pady=10, side=LEFT)
        self.userEntry.focus_set()
        self.userEntry['border'] = 3
        self.textBox['border'] = 3
        # self.frame.after(100, lambda: self.animation(self.userEntry))
        # self.frame.after(100, lambda: self.animation(self.textBox))

    def editTextBox(self):
        # this fragment is a joke xD
        def exec(*args, **kargs):
            args[0].textBox.config(state=NORMAL)
            self(*args, **kargs)
            args[0].textBox.config(state=DISABLED)
        return exec

    def updateStatusVars(self):
        if self.adventure.current_stage:
            self.sbvCurrentStage.set(
                gui_text['txt_current_stage'] + str(self.adventure.current_stage))
        if self.adventure.game_status_message:
            self.sbvCurrentStatus.set(self.adventure.game_status_message)
        else:
            self.sbvCurrentStatus.set('')
        if(self.adventure.in_game is False):
            self.sbvCurrentStage.set('')
            self.sbvCurrentStatus.set(gui_text['txt_adventure_end'])
            self.userEntry.config(state=DISABLED)

    def getUserInputContent(self):
        return self.userInput.get()

    def clearUserInput(self):
        self.userInput.set('')

    @editTextBox
    def clearScreen(self):
        self.textBox.delete(.0, END)

    @editTextBox
    def updateScreen(self, text_list, tag=''):
        text_line = '\n'.join([line for line in text_list])
        if self.animatedText is False:
            self.textBox.insert(END, text_line, tag)
        else:
            for fragment in text_line.split(' '):
                time.sleep(0.01)  # print animation velocity in ms
                self.textBox.insert(END, fragment + ' ', tag)
                self.textBox.update()
                self.textBox.see('end')

        self.textBox.insert(END, '\n')
        self.textBox.see('end')

    def getUserInput(self):
        action_text = self.getUserInputContent()
        self.clearUserInput()
        self.updateScreen(['[' + action_text.capitalize() + ']'], 'userInput')
        return action_text

    def enterAction(self):
        user_command = self.getUserInput()
        execute_action = self.adventure.executeAction(user_command)
        if execute_action:
            self.updateScreen(self.adventure.output_buffer, 'adventureText')
        elif execute_action is False:
            self.updateScreen([f"{gui_text['txt_action_once']} {user_command}!"], 'failAction')
        else:
            self.updateScreen([gui_text['txt_you_cant']], 'failAction')
        for action in self.adventure.game_actions.values():
            print(action['name'])
        self.updateStatusVars()
        self.showGameImage()

    def animation(self):
        for count in range(3):
            time.sleep(0.01)
            self.updateScreen(["algo"], scape='')
            self.textBox.update()


class GameGUI(GameInterface):
    """
                    Root Window self.main_window
                    ====MenuBar====
                    <Game Interface>
                    ==StatusBar====
    """

    def __init__(self):
        self.main_window = Tk()
        super().__init__(window=self.main_window)
        self.WIDTH = 850
        self.HEIGHT = 340
        self.POSX = 300
        self.POSY = 300
        self.init_menubar()
        self.init_statusbar()
        self.init_window()
        self.is_open = False
        self.is_test_context = True
        self.current_adventure = None
        if(self.is_test_context):
            self.load_test()
        self.main_window.mainloop()

    def close_window(self):
        exit = messagebox.askyesno(gui_text['menu_help'], gui_text['msg_exit'])
        if(exit):
            self.main_window.quit()

    def init_window(self):
        self.main_window.iconbitmap('assets/icon.ico')
        self.main_window.title(APP_NAME)
        self.main_window.resizable(0, 0)
        self.main_window.geometry(f'{self.WIDTH}x{self.HEIGHT}+{self.POSX}+{self.POSY}')
        self.userEntry.bind('<KeyPress-Return>',
                            lambda x: self.enterAction())

    def showGameImage(self):
        if self.adventure.game_show_image:
            image_path = self.adventure.current_directory + \
                "/" + self.adventure.game_show_image
            ImageBox(self.main_window, image_path)
            self.adventure.game_show_image = None

    def init_menubar(self):
        menuBar = Menu(self.main_window)
        # File Cascade
        file = Menu(menuBar, tearoff=0)
        file.add_command(label=gui_text['menu_open'],
                         command=self.open_adventure,
                         accelerator="Ctrl+O")
        file.add_command(label=gui_text['menu_view'],
                         command=self.getUserInput)
        file.add_command(label=gui_text['menu_clear_screen'],
                         command=lambda: self.clearScreen())
        file.add_command(label=gui_text['menu_reload'],
                         command=lambda: self.reload_adventure(),
                         accelerator="Ctrl+R")
        self.main_window.bind_all(
            "<Control-r>", lambda x: self.reload_adventure())
        self.main_window.bind_all(
            "<Control-o>", lambda x: self.open_adventure())
        file.add_separator()
        file.add_command(
            label=gui_text['menu_exit'], command=self.close_window)

        # Help cascade
        help_menu = Menu(menuBar, tearoff=0)
        help_menu.add_command(
            label=gui_text['menu_i_need_help'], command=lambda: self.help())
        help_menu.add_separator()
        help_menu.add_command(label=gui_text['menu_about'], command=self.about)

        # Add cascades
        menuBar.add_cascade(label=gui_text['menu_file'], menu=file)
        menuBar.add_cascade(label=gui_text['menu_help'], menu=help_menu)
        self.main_window.config(menu=menuBar)

    def about(self):
        About(self.main_window)

    def help(self):
        Help(self.main_window)

    def load_test(self):
        self.is_open = False
        self.clearScreen()
        adv_test_dir = os.getcwd() + '/test_adventure/test.adventure'
        #adv_test_dir = os.getcwd() + '/La casa de Yoel/inicio.adventure'
        if(self.current_adventure is None):
            self.current_adventure = adv_test_dir
        self.open_adventure(reload=True)
        self.userEntry.config(state=NORMAL)
        self.updateStatusVars()
        self.showGameImage()

    def open_adventure(self, reload=False):
        """open adventure in gui"""
        if self.is_open or self.adventure.in_game:
            progress = messagebox.askyesno(
                'Atención', gui_text['msg_open_another_adventure'])
            if(progress is False):
                return False
            else:
                self.adventure.in_game = False
                self.is_open = False
        self.clearScreen()
        if reload:
            get_dir = self.current_adventure
        else:
            get_dir = str(filedialog.askopenfile().name)
        adv_full_dir = re.findall(r'(.*)/(\w+)\.adventure+', get_dir)
        self.current_adventure = get_dir
        if adv_full_dir:
            file_dir, file_name = adv_full_dir[0]
            if(self.adventure.openAdventure(file_name, adventure_dir=file_dir)):
                if(self.adventure.adventure_name):
                    self.main_window.title(self.adventure.adventure_name)
                self.updateScreen(
                    self.adventure.output_buffer, tag='adventureText')
                self.is_open = True
                self.userEntry.config(state=NORMAL)
            else:
                messagebox.showerror(
                    gui_text['menu_help'], gui_text['msg_file_content_error'])
        else:
            messagebox.showerror(
                gui_text['msg_error_title'], gui_text['msg_incompatible_file'])

    def reload_adventure(self):
        if(self.is_open):
            if(self.adventure.in_game):
                self.adventure.finishAdventure()
            if(self.is_test_context):
                self.load_test()
            else:
                self.open_adventure(reload=True)
        print("adventure reloaded at", time.strftime("%H:%M:%S %p"))

    def init_statusbar(self):
        self.sbCurrentStage = Label(self.main_window, bd=1, relief=SUNKEN, anchor=W,
                                    textvariable=self.sbvCurrentStage,
                                    font=('arial', 9, 'normal'))
        self.sbCurrentStatus = Label(self.main_window, bd=1, relief=SUNKEN, anchor=W,
                                     textvariable=self.sbvCurrentStatus,
                                     font=('arial', 9, 'normal'))

        self.sbCurrentStage.pack(ipadx=100, side="left")
        self.sbCurrentStatus.pack(ipadx=150, side="right")


class About():
    def __init__(self, parent):
        top = self.top = Toplevel(parent)
        top.iconbitmap('icon.ico')
        top.title(gui_text['about_title'])
        top.geometry("650x200")
        top.resizable(False, False)
        top.deiconify()
        imagen = Image.open("assets/logo.png")
        photo = ImageTk.PhotoImage(imagen)
        title = Label(top,
                      font="Algerian 25",
                      text=APP_NAME)
        about_text = Label(top,
                           text=ABOUT_TEXT,
                           font="Calibri 15")

        logo = Label(top, image=photo)
        logo.image = photo
        logo.pack(side="left")
        title.pack(side="top", pady=10)
        about_text.pack()
        top.grab_set()  # toplevel
        top.focus_force()  # force focus window


class Help():
    def __init__(self, parent):
        top = self.top = Toplevel(parent)
        top.iconbitmap('icon.ico')
        top.title(gui_text['help_title'])
        top.geometry("650x200")
        top.resizable(False, False)
        top.deiconify()

        textHelp = Text(top)
        textHelp.tag_config("title", font=('Czar', 17))
        textHelp.tag_config("text", font=('Arial', 13))
        helpTitle = "\t\tBienvenido a Adventure Writter!"
        helpText = "\nUn software para creación de aventuras conversacionales"
        helpText += "de una manera rapida y personalizable."
        helpText += ""
        textHelp.insert("end", helpTitle, 'title')
        textHelp.insert("end", helpText, "text")
        textHelp.pack()
        textHelp.config(state="disabled", wrap='word')
        top.grab_set()  # toplevel
        top.focus_force()  # force focus window


class ImageBox():
    def __init__(self, parent, imagen, full_screen=False):
        image_window = self.image_window = Toplevel(parent)
        self.full_screen = full_screen
        self.image_window.attributes("-fullscreen", self.full_screen)
        self.image_window.bind("<Escape>", self.disable_fullscreen)
        self.image_window.resizable(0, 0)
        image_window.title("...")
        imagen_show = Image.open(imagen)
        photo = ImageTk.PhotoImage(imagen_show)
        label = Label(self.image_window, image=photo)
        label.image = photo
        label.pack()
        image_window.grab_set()

    def disable_fullscreen(self, event=None):
        self.image_window.attributes("-fullscreen", False)

    def load_image(self, image_name):

        return photo


if __name__ == '__main__':
    gui = GameGUI()
