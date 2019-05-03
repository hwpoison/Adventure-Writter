import time
from tkinter import *
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
from AdventureCore import *
__autor__ = "srbill1996"
__version__ = "1.0"

WIDTH = 850
HEIGHT = 340
POSX = 300
POSY = 300
APP_NAME = f"Adventure Writter {__version__}"
#Button text
TXT_HELP = "Ayuda"
TXT_FILE = "Archivo"
TXT_MENU_OPEN = "Abrir"
TXT_MENU_VIEW = "Ver"
TXT_ASK_EXIT = "Deseas salir?"
TXT_EXIT = "Salir"
TXT_ERROR = "Error"
TXT_ABOUT = "Acerca de..."
TXT_CLEARSCREEN = "Clear screen"
TXT_INEEDHELP = "Necesito ayuda"
#Message text
ABOUT_TEXT = f"Creado por {__autor__}\n\n\nhttps://netixzen.blogspot.com.ar/\n2019"
MSG_OPEN_ANOTHER_ADVENTURE = 'Ya hay una aventura en progreso, deseas cerrarla?'
MSG_FILE_CONTENT_ERROR = "El contenido del archivo no se reconoce."
MSG_INCOMPATIBLE_FILE = "Selecciona un archivo compatible"


class UserInterface(Frame):
	
	def __init__(self):
		super().__init__()
		self.userInput = StringVar()
		self.init_user_interface()
		self.pack()

	def editTextBox(self):
		# this fragment is a joke xD
		def exec(*args, **kargs):
			args[0].textBox.config(state=NORMAL)
			self(*args, **kargs)
			args[0].textBox.config(state=DISABLED)
		return exec

	def getInputUser(self):
		return self.userInput.get()

	def load_image(self, image_name):
		imagen = Image.open(image_name)
		photo = ImageTk.PhotoImage(imagen)
		return photo

	def clearUserInput(self):
		self.userInput.set('')

	@editTextBox
	def updateScreen(self, text_list):
		self.textBox.insert(END, '\n'.join(
			[line for line in text_list]) + '\n')

	@editTextBox
	def clearScreen(self):
		self.textBox.delete(.0, END)

	def getUserInput(self):
		action_text = self.getInputUser()
		self.clearUserInput()
		self.updateScreen(['>' + action_text])
		return action_text

	def init_user_interface(self):
		# TextBox Area
		self.textBox = Text(self,
							width=73,
							height=10,
							border=2,
							font='Calibri 15')
		self.textBox.config(state=DISABLED)
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


class About():
	def __init__(self, parent):
		top = self.top = Toplevel(parent)
		top.iconbitmap('icon.ico')
		top.title(f"Acerca..")
		top.geometry("650x200")
		top.resizable(False, False)
		top.deiconify()
		imagen = Image.open("logo.png")
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

		top.grab_set()
		top.focus_force()


class GameGUI(AdventureCore):

	def __init__(self):
		super().__init__()
		self.window = Tk()
		self.user_interface = UserInterface()
		self.is_open = False
		self.init_menubar()
		self.init_statusbar()
		self.init_window()

	def load_stage_file(self, stage):
		if(super().load_stage_file(stage)):
			self.user_interface.clearScreen()
			self.statusBar.set('Estas en ' + str(self.current_stage))
			return True
		return False

	def close_window(self):
		exit = messagebox.askyesno(TXT_EXIT, TXT_ASK_EXIT)
		if(exit):
			self.window.quit()

	def enterAction(self):
		user_command = self.user_interface.getUserInput()
		if(self.exec_action(user_command) is True):
			self.user_interface.updateScreen(self.output_buffer)
		else:
			self.user_interface.updateScreen(['No puedes hacer eso!'])

	def init_window(self):
		self.window.iconbitmap('icon.ico')
		self.window.title(APP_NAME)
		self.window.resizable(0, 0)
		self.window.geometry(f'{WIDTH}x{HEIGHT}+{POSX}+{POSY}')
		self.user_interface.userEntry.bind('<KeyPress-Return>',
										   lambda x: self.enterAction())
		self.window.mainloop()

	def open_adventure(self):
		if(self.is_open):
			progress = messagebox.askyesno(
				'Atención', MSG_OPEN_ANOTHER_ADVENTURE)
			if(progress is False):
				return False

		get_dir = str(filedialog.askopenfile().name)
		adv_full_dir = re.findall(r'(.*)/(\w+)\.adventure+', get_dir)
		if(adv_full_dir):
			file_dir, file_name = adv_full_dir[0]
			if(self.load_adventure(file_dir, file_name)):
				self.user_interface.updateScreen(self.output_buffer)
				self.is_open = True
			else:
				messagebox.showerror(TXT_ERROR, MSG_FILE_CONTENT_ERROR)
		else:
			messagebox.showerror(TXT_ERROR, MSG_INCOMPATIBLE_FILE)

	def init_menubar(self):
		menuBar = Menu(self.window)
		# File Cascade
		file = Menu(menuBar, tearoff=0)
		file.add_command(label=TXT_MENU_OPEN, command=self.open_adventure)
		file.add_command(label=TXT_MENU_VIEW,
						 command=self.user_interface.getInputUser)
		file.add_command(label=TXT_CLEARSCREEN,
						 command=lambda: self.user_interface.clearScreen())

		file.add_separator()
		file.add_command(label=TXT_EXIT, command=self.close_window)
		# Help cascade
		help_menu = Menu(menuBar, tearoff=0)
		help_menu.add_command(label=TXT_INEEDHELP)
		help_menu.add_separator()
		help_menu.add_command(label=TXT_ABOUT, command=self.about)
		# Add cascades
		menuBar.add_cascade(label=TXT_FILE, menu=file)
		menuBar.add_cascade(label=TXT_HELP, menu=help_menu)
		self.window.config(menu=menuBar)

	def about(self):
		About(self.window)

	def init_statusbar(self):
		self.statusBar = StringVar()
		self.n = Label(self.window, bd=1, relief=SUNKEN, anchor=W,
					   textvariable=self.statusBar,
					   font=('arial', 9, 'normal'))
		self.n.pack(fill=X)


if __name__ == '__main__':
	gui = GameGUI()
