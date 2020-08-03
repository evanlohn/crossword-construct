import tkinter as tk
from PIL import Image, ImageTk
from board import Board

clue_labels = ['Across', 'Down']
ACROSS, DOWN = clue_labels

def click_handler(r_ind, c_ind, game):
	def handle_click(event):
		print(r_ind, c_ind)
		clicked_frame = game.board_frame.grid_slaves(row=r_ind, column=c_ind)[0]
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
		canvas = tk.Canvas(frame_canvas, bg="yellow")
		canvas.grid(row=0, column=0, sticky="news")

		# Link a scrollbar to the canvas
		vsb = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
		vsb.grid(row=0, column=1, sticky='ns')
		canvas.configure(yscrollcommand=vsb.set)

		# Create a frame to contain the buttons
		frame_labels = tk.Frame(canvas, bg="blue")
		canvas.create_window((0, 0), window=frame_labels, anchor='nw')

		# Add 1 by 2 moves to the frame
		
		#TODO: call some kind of sync function here to make the clue boxes appear that match 
		#      the actual numbers on the board
		"""
		clue_dirs = [clue_labels]
		rows = len(clue_dirs)
		columns = len(clue_dirs[0])
		for i in range(0, rows):
		    for j in range(0, columns):

		        moves[i][j] = tk.Label(frame_labels, text=moves[i][j])
		        if i == 0:
		        	moves[i][j].config(bg='orange')
		        moves[i][j].grid(row=i, column=j, sticky='news')


		# Update buttons frames idle tasks to let tkinter calculate buttons sizes
		frame_labels.update_idletasks()
		self.frame_labels = frame_labels
		"""


		#TODO: probably don't want this? or just more than 5?
		"""
		# Resize the canvas frame to show exactly 5-by-5 labels and the scrollbar
		first5columns_width = sum([moves[0][j].winfo_width() for j in range(columns)])
		first5rows_height = moves[0][0].winfo_height() * 5
		frame_canvas.config(width=first5columns_width + vsb.winfo_width(),
		                    height=first5rows_height)

		"""

		# Set the canvas scrolling region
		canvas.config(scrollregion=canvas.bbox("all"))
		self.clues_canvas = canvas

		self.notif_label = tk.Label(self.info_frame, text='')


		self.update_all()

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
			frame.bg = 'black'
		else:
			frame.bg = 'white'
			label = tk.Label(master=frame, text=entry.val, bg=frame.bg)
			label.bind("<Button-1>", handler)
			label.pack(fill=tk.BOTH, expand=True)

			frame.displayed_label = label

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

	def create_move(self, src, dst):
		return Move(src, dst, self.board)

	def check_finished(self):
		

		in_check = self.board.in_check(self.turn)
		if not self.board.player_has_moves(self.turn):
			if in_check:
				self.notif_label.config(text='{} wins!'.format(human_colors[other(self.turn)]))
				self.board.notify_last_move_checkmate()
				print('The {} player wins!'.format(human_colors[other(self.turn)]))
			else:
				self.notif_label.config(text='stalemate!')
				print('Stalemate! It is a draw!!')
			self.notif_label.grid(row=2, column=0, sticky='news')
		elif in_check:
			self.notif_label.config(text='check!')
			self.notif_label.grid(row=2, column=0, sticky='news')
			self.board.notify_last_move_check()
		

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
