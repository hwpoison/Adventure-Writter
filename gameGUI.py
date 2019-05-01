import time
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from AdventureCore import *

WIDTH = 850
HEIGHT = 340
POSX = 300
POSY = 300
WINDOW_TITLE = "Adventure"


class UserInterface(Frame):

    def __init__(self):
        super().__init__()
        self.userInput = StringVar()
        self.init_user_interface()
        self.pack()

    def getInputUser(self):
        return self.userInput.get()

    def load_image(self, image_name):
        imagen = Image.open(image_name)
        photo = ImageTk.PhotoImage(imagen)
        return photo

    def clearUserInput(self):
        self.userInput.set('')

    def updateScreen(self, current_input):
        self.textBox.insert(END, '\n'.join([line for line in current_input]) + '\n')

    def clearScreen(self):
        self.textBox.delete(.0,END)

    def getUserInput(self):
        action_text = self.getInputUser()
        self.clearUserInput()
        self.updateScreen(['>' + action_text])
        return action_text

    def init_user_interface(self):
        # TextBox Area
        print(dir(self.load_image("imagen.jpg")))
        self.textBox = Text(self,
                       width=73,
                       height=10,
                       border=2,
                       font='Calibri 15')

        # User input area
        self.userEntry = Entry(self,
                      textvariable=self.userInput,
                      width=52,
                      font="Calibri 20",
                      border=0)

        self.textBox.pack(padx=10)
        self.userEntry.pack(padx=10, pady=10, side=LEFT)
        self.userEntry.focus_set()
        self.after(100, lambda: self.animacion(self.userEntry))
        self.after(100, lambda: self.animacion(self.textBox))
    
    def animacion(self, elemento):
        for count in range(3):
            time.sleep(0.1)
            elemento['border'] = elemento['border'] + count
            elemento.update()

class GameGUI(AdventureCore):

    def __init__(self):
        super().__init__()
        self.adventure_dir  = 'test_adventure\\'
        self.window = Tk()
        self.user_interface = UserInterface()
        self.init_menubar()
        self.init_statusbar()
        self.start_game()
        self.init_window()

    def start_game(self):
        self.game_vars = {}
        self.game_actions = {}
        self.load_stage_file('habitacion0') #start
        self.user_interface.updateScreen(self.current_output)
        print("Escenario cargado..")
 
    def load_stage_file(self, stage):
        super().load_stage_file(self.adventure_dir + stage)
        self.user_interface.clearScreen()
        self.statusBar.set('Estas en ' + self.current_stage)

    def close_window(self):
        exit = messagebox.askyesno("Salir", "Deseas salir?")
        if(exit):
            self.window.quit()

    def enterAction(self):
        user_command = self.user_interface.getUserInput()
        if(self.exec_action(user_command) is True):
            self.user_interface.updateScreen(self.current_output)
        else:
            self.user_interface.updateScreen(['No puedes hacer eso!'])
        
    def init_window(self):
        self.window.title(WINDOW_TITLE)
        self.window.resizable(0, 0)
        self.window.geometry(f'{WIDTH}x{HEIGHT}+{POSX}+{POSY}')
        # self.window.bind('<KeyPress-Return>',
        # 				 lambda x: self.close_window())
        self.user_interface.userEntry.bind('<KeyPress-Return>',
                lambda x: self.enterAction())
        self.window.mainloop()

    def init_menubar(self):
        menuBar = Menu(self.window)
        # File Cascade
        file = Menu(menuBar, tearoff=0)
        file.add_command(label="Abrir")
        file.add_command(label="Ver",
                         command=self.user_interface.getInputUser)

        file.add_separator()
        file.add_command(label="Salir", command=self.close_window)
        #Help cascade
        help_menu = Menu(menuBar, tearoff=0)
        help_menu.add_command(label="Necesito ayuda")
        help_menu.add_separator()
        help_menu.add_command(label="Acerca de...", command=self.about)
        # Add cascades
        menuBar.add_cascade(label="Archivo", menu=file)
        menuBar.add_cascade(label="Ayuda", menu=help_menu)
        self.window.config(menu=menuBar)
   
    def about(self):
        aboutText="Creado por Guillermo Giménez\nhttps://netixzen.blogspot.com.ar\n<2019>"
        messagebox.showinfo("Información", aboutText)

    def init_statusbar(self):
        self.statusBar=StringVar()        
        self.n= Label(self.window, bd=1, relief=SUNKEN, anchor=W,
                           textvariable=self.statusBar,
                           font=('arial',9,'normal'))
        self.n.pack(fill=X)      

if __name__ == '__main__':
    gui = GameGUI()
    gui.start_game()
