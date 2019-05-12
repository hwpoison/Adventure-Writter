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
APP_NAME = f"Adventure Writter [{__version__}]"
# Button text
TXT_HELP = "Ayuda"
TXT_FILE = "Archivo"
TXT_MENU_OPEN = "Abrir"
TXT_MENU_VIEW = "Ver"
TXT_ASK_EXIT = "Deseas salir?"
TXT_EXIT = "Salir"
TXT_ERROR = "Error"
TXT_ABOUT = "Acerca de..."
TXT_CLEARSCREEN = "Limpiar pantalla"
TXT_INEEDHELP = "Necesito ayuda"
TXT_RELOAD = "Recargar aventura"
TXT_ADVENTURE_END = 'La aventura ha terminado.'
TXT_CURRENT_STAGE = 'Escenario actual: '
# Message text
ABOUT_TEXT = f"Creado por {__autor__}\n\n\nhttps://netixzen.blogspot.com.ar/\n2019"
MSG_OPEN_ANOTHER_ADVENTURE = 'Ya hay una aventura en progreso, deseas cerrarla?'
MSG_FILE_CONTENT_ERROR = "El contenido del archivo no se reconoce."
MSG_INCOMPATIBLE_FILE = "Selecciona un archivo compatible"


class GameInterface(AdventureCore):

	def __init__(self, window):
		super().__init__()
		self.frame = Frame(window)
		self.userInput = StringVar()
		self.sbvCurrentStage = StringVar()
		self.sbvCurrentStatus = StringVar()
		self.init_user_interface()
		self.frame.pack()

	def init_user_interface(self):
		# TextBox Area
		scrollbar = Scrollbar(self.frame)
		scrollbar.pack(side=RIGHT, fill=Y)

		self.textBox = Text(self.frame,
							width=73,
							height=10,
							border=2,
							font='Calibri 15',
							yscrollcommand=scrollbar.set)
		self.textBox.config(state=DISABLED)
		scrollbar.config(command=self.textBox.yview)
		# User input area
		self.userEntry = Entry(self.frame,
							   textvariable=self.userInput,
							   width=52,
							   font="Calibri 20",
							   border=0,
							   state=DISABLED)

		self.textBox.pack(padx=10)
		self.userEntry.pack(padx=10, pady=10, side=LEFT)
		self.userEntry.focus_set()
		self.frame.after(100, lambda: self.animation(self.userEntry))
		self.frame.after(100, lambda: self.animation(self.textBox))

	def editTextBox(self):
		# this fragment is a joke xD
		def exec(*args, **kargs):
			args[0].textBox.config(state=NORMAL)
			self(*args, **kargs)
			args[0].textBox.config(state=DISABLED)
		return exec

	def updateStatusVars(self):
		if self.current_stage:
			self.sbvCurrentStage.set(
				TXT_CURRENT_STAGE + str(self.current_stage))

		if self.game_status_message:
			self.sbvCurrentStatus.set(self.game_status_message)
		else:
			self.sbvCurrentStatus.set('')

		if(self.in_game is False):
			self.sbvCurrentStage.set('')
			self.sbvCurrentStatus.set(TXT_ADVENTURE_END)
			self.userEntry.config(state=DISABLED)

	def getUserInputContent(self):
		return self.userInput.get()

	def clearUserInput(self):
		self.userInput.set('')

	@editTextBox
	def clearScreen(self):
		self.textBox.delete(.0, END)

	@editTextBox
	def updateScreen(self, text_list):
		self.textBox.insert(END, '\n'.join(
			[line for line in text_list]) + '\n')
		self.textBox.see('end')

	def getUserInput(self):
		action_text = self.getUserInputContent()
		self.clearUserInput()
		self.updateScreen(['>' + action_text])
		return action_text

	def enterAction(self):
		user_command = self.getUserInput()
		if(self.exec_action(user_command) is True):
			self.updateScreen(self.output_buffer)
		else:
			self.updateScreen(['No puedes hacer eso!'])
		self.updateStatusVars()

	def animation(self, elemento):
		for count in range(3):
			time.sleep(0.1)
			elemento['border'] = elemento['border'] + count
			elemento.update()

	def load_image(self, image_name):
		imagen = Image.open(image_name)
		photo = ImageTk.PhotoImage(imagen)
		return photo

class GameGUI(GameInterface):

	def __init__(self):
		self.window = Tk()
		super().__init__(window=self.window)
		self.is_open = False
		self.init_menubar()
		self.init_statusbar()
		self.load_test()
		self.init_window()

	def close_window(self):
		exit = messagebox.askyesno(TXT_EXIT, TXT_ASK_EXIT)
		if(exit):
			self.window.quit()

	def init_window(self):
		self.window.iconbitmap('icon.ico')
		self.window.title(APP_NAME)
		self.window.resizable(0, 0)
		self.window.geometry(f'{WIDTH}x{HEIGHT}+{POSX}+{POSY}')
		self.userEntry.bind('<KeyPress-Return>',
										   lambda x: self.enterAction())
		self.window.mainloop()

	def init_menubar(self):
		menuBar = Menu(self.window)
		# File Cascade
		file = Menu(menuBar, tearoff=0)
		file.add_command(label=TXT_MENU_OPEN, 
						command=self.open_adventure,
						accelerator="Ctrl+O")
		file.add_command(label=TXT_MENU_VIEW,
						 command=self.getUserInput)
		file.add_command(label=TXT_CLEARSCREEN,
						 command=lambda: self.clearScreen())
		file.add_command(label=TXT_RELOAD,
						 command=lambda: self.reload_adventure(),
						 accelerator="Ctrl+R")
		self.window.bind_all("<Control-r>", lambda x: self.reload_adventure())
		self.window.bind_all("<Control-o>", lambda x: self.open_adventure())
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

	def load_test(self):
		self.is_open = True
		self.clearScreen()
		self.stage_history = []
		self.load_adventure(
			'C:\\Users\\Guillermo\\Desktop\\Adventure Creator\\Adventure-Writter\\test_adventure', 'habitacion0')
		self.updateScreen(self.output_buffer)
		self.userEntry.config(state=NORMAL)
		self.updateStatusVars()

	def load_stage_file(self, stage):
		if(super().load_stage_file(stage)):
			self.clearScreen()
			self.updateStatusVars()
			return True
		return False

	def open_adventure(self):
		if(self.is_open or self.in_game):
			progress = messagebox.askyesno(
				'Atención', MSG_OPEN_ANOTHER_ADVENTURE)
			if(progress is False):
				return False
			else:
				self.in_game = False
				self.is_open = False

		get_dir = str(filedialog.askopenfile().name)
		adv_full_dir = re.findall(r'(.*)/(\w+)\.adventure+', get_dir)
		if(adv_full_dir):
			file_dir, file_name = adv_full_dir[0]
			if(self.load_adventure(file_dir, file_name)):
				self.updateScreen(self.output_buffer)
				self.is_open = True
				self.userEntry.config(state=NORMAL)
			else:
				messagebox.showerror(TXT_ERROR, MSG_FILE_CONTENT_ERROR)
		else:
			messagebox.showerror(TXT_ERROR, MSG_INCOMPATIBLE_FILE)

	def reload_adventure(self):
		self.load_test()
		print("reloaded at", time.strftime("%H:%M:%S %p"))

	def init_statusbar(self):
		self.sbCurrentStage = Label(self.window, bd=1, relief=SUNKEN, anchor=W,
									textvariable=self.sbvCurrentStage,
									font=('arial', 9, 'normal'))
		self.sbCurrentStatus = Label(self.window, bd=1, relief=SUNKEN, anchor=W,
									 textvariable=self.sbvCurrentStatus,
									 font=('arial', 9, 'normal'))

		self.sbCurrentStage.pack(ipadx=100, side="left")
		self.sbCurrentStatus.pack(ipadx=150, side="right")


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


if __name__ == '__main__':
	gui = GameGUI()
