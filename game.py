import tkinter as tk

from PIL import Image, ImageTk
from board import Board

clue_labels = ['Across', 'Down']
ACROSS, DOWN = clue_labels

def click_handler(r_ind, c_ind, game):
	def handle_click(event):
		print(r_ind, c_ind)
		clicked_frame = game.board_frame.grid_slaves(row=r_ind, column=c_ind)[0]
		if game.placing_blocks.get():
			game.block(r_ind, c_ind)
		clicked_frame.focus_set()
		if game.selected is None:
			game.select_sq(r_ind, c_ind, clicked_frame)
		else:
			r_sel, c_sel = game.selected
			sel_frame = game.board_frame.grid_slaves(row=r_sel, column=c_sel)[0]
			if (r_sel == r_ind and c_sel == c_ind):
				game.switch_sel_dir()
			else:
				game.select_sq(r_ind, c_ind, clicked_frame)
				game.deselect_sq(sel_frame)

		#print('square at row {} col {} was clicked'.format(r_ind, c_ind))
	return handle_click

def key_handler(r_ind, c_ind, game):
	def handle_key(event):
		c_inp = str(event.char)
		print(r_ind, c_ind, str(event.char))
		game.get_entry(r_ind, c_ind).val = c_inp
		game.update_square(r_ind, c_ind)
	return handle_key


class Game:

	def __init__(self, board):
		self.board = board

		## Tkinter stuff
		self.window = tk.Tk()
		self.board_frame = tk.Frame(master=self.window, width=400, height=400, bg="black")
		self.info_frame = tk.Frame(master=self.window, width=400, bg="blue")
		self.board_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
		self.info_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

		## state use for click logic
		self.selected = None # no square selected
		self.sel_dir = ACROSS

		## put pieces on board
		for r_ind, row in enumerate(self.board.board_lst):
			self.board_frame.columnconfigure(r_ind, weight=1, minsize=75) #, minsize=50
			self.board_frame.rowconfigure(r_ind, weight=1, minsize=75)
			for c_ind, piece in enumerate(row):

				c_handler = click_handler(r_ind, c_ind, self)
				k_handler = key_handler(r_ind, c_ind, self)
				frame = tk.Frame(master=self.board_frame, relief=tk.GROOVE, borderwidth=1, bg='white')
				frame.displayed_label = None
				frame.bind("<Key>", k_handler)

				frame.bind("<Button-1>", c_handler)
				frame.grid(row=r_ind, column=c_ind, sticky="nsew")

				frame.columnconfigure(0, weight=1, minsize=15)
				frame.rowconfigure(0, weight=1, minsize=15)
				clue_num_label = tk.Label(frame, text=' ')
				clue_num_label.place(x=0, y=0)
				#clue_num_label.grid(row=0, column=0, sticky='nw')
				#clue_num_label.pack(side = tk.TOP, fill=tk.X)
				frame.clue_num_label = clue_num_label
				#frame.grid(row=0, column=0, sticky='nw')


				#self.update_square(r_ind, c_ind)

		## Add info pane stuff 
		#self.turn_label = tk.Label(self.info_frame, text='Turn: White')
		#self.turn_label.grid(row=0, column=0, sticky='nsew')


		frame_canvas = tk.Frame(self.info_frame)
		frame_canvas.grid(row=0, column=0, padx=(0, 5), sticky='nw')
		frame_canvas.grid_rowconfigure(0, weight=1)
		frame_canvas.grid_columnconfigure(0, weight=1)
		# Set grid_propagate to False to allow 5-by-5 buttons resizing later
		frame_canvas.grid_propagate(False)

		# Add a canvas in that frame
		#canvas = tk.Canvas(frame_canvas, bg="yellow")
		#canvas.grid(row=0, column=0, sticky="news")

		# Link a scrollbar to the canvas
		#vsb = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
		#vsb.grid(row=0, column=1, sticky='ns')
		#canvas.configure(yscrollcommand=vsb.set)

		# Create a frame to contain the buttons
		#frame_labels = tk.Frame(canvas, bg="blue")
		#canvas.create_window((0, 0), window=frame_labels, anchor='nw')

		# Add 1 by 2 moves to the frame
		
		#TODO: call some kind of sync function here to make the clue boxes appear that match 
		#      the actual numbers on the board
		self.placing_blocks = tk.BooleanVar(False)
		self.ck = tk.Checkbutton(self.info_frame, text='Place Blocks',
			variable=self.placing_blocks, onvalue=1,
			 offvalue=0)
		self.title = tk.Label(self.info_frame, text='Crossword')
		self.title.grid(row=0, column=0, sticky='news')
		self.ck.grid(row=1, column=0, sticky='news')

		#self.update_all()

	def get_entry(self, r, c):
		return self.board.board_lst[r][c]

	def switch_sel_dir(self):
		if self.sel_dir == ACROSS:
			self.sel_dir = DOWN
		else:
			self.sel_dir = ACROSS

		#TODO: update graphics for row and column

	def update_square(self, row, col):
		entry = self.get_entry(row, col)

		frame = self.board_frame.grid_slaves(row=row, column=col)[0]

		# TODO: only need this on first run?
		handler = click_handler(row, col, self)
		frame.bind("<Button-1>", handler)

		if frame.displayed_label is not None:
			frame.displayed_label.pack_forget()
			frame.displayed_label.destroy()
			frame.displayed_label = None

		if entry.blocked:
			frame.config(bg='black')
			frame.clue_num_label.config(bg='black')
		else:
			frame.bg = 'white'

			#TODO: adapt font size to board
			#https://stackoverflow.com/questions/24440541/python-tkinter-expanding-fontsize-dynamically-to-fill-frame
			label = tk.Label(master=frame, text=entry.val.upper(), bg=frame.bg, font=("Helvetica", 30))
			#label['font'] = myFont
			label.bind("<Button-1>", handler)
			#label.grid(row=0, column=0, sticky='news')
			label.pack(fill=tk.BOTH, expand=True)

			frame.displayed_label = label


	def block(self, r_ind, c_ind):
		self.get_entry(r_ind, c_ind).toggle_blocked()
		self.update_square(r_ind, c_ind)

	def update_all(self):
		"""
		for txt in self.frame_labels.grid_slaves():
			txt.grid_forget()
			txt.destroy()

		mv_texts = clue_labels + self.board.clues_as_text()
		for i, mv_text in enumerate(mv_texts):
			row = (i//2)
			col = i % 2
			lbl = tk.Label(self.frame_labels, text=mv_text)
			if row == 0:
				lbl.config(bg='orange')
			lbl.grid(row=row, column=col, sticky='news')
		if col == 0:
			lbl = tk.Label(self.frame_labels, text='')
			lbl.grid(row=row, column=1, sticky='news')

		self.frame_labels.update_idletasks()
		

		# Set the canvas scrolling region
		self.moves_canvas.config(scrollregion=self.moves_canvas.bbox("all"))
		

		self.frame_labels
		for r_ind, row in enumerate(self.board.board_lst):
			frame = self.board_frame.grid_slaves(row=r_ind + 1, column=0)[0]
			letter_ind = r_ind if self.turn == BLACK else len(all_ranks) - r_ind - 1
			frame.lbl.config(text=all_ranks[letter_ind])
			for c_ind, piece in enumerate(row):
				self.update_square(r_ind, c_ind)

		"""

	def select_sq(self, r_ind, c_ind, frame):
		self.selected = (r_ind, c_ind)
		frame.config(highlightthickness=2)
		#frame.config(highlightbackground='red') # makes the border red

	def deselect_sq(self, frame):
		#self.selected = None
		frame.config(highlightthickness=0)
		

	def display_board(self):
		self.window.mainloop()


class Player:
	def get_move(board):
		return None

class HumanPlayer(Player):
	def get_move(board):
		return None

def play_game(board):
	pass
