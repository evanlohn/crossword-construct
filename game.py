import tkinter as tk

from PIL import Image, ImageTk
from board import Board

clue_labels = ['Across', 'Down']
ACROSS, DOWN = clue_labels


#TODO: 
# 1) Serialize and read boards
# 2) maintain a "current direction", and when a letter is entered on the board,
#    select the next entry in that direction if not blocked
# 3) When a square on the board is clicked, find the corresponding clue 
#    (in the "current direction") and scroll to it (? maybe unecessary)
# 4) "Play mode" ?
def click_handler(r_ind, c_ind, game):
    def handle_click(event):
        #print(r_ind, c_ind)
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
        game.get_entry(r_ind, c_ind).val = c_inp
        game.update_square(r_ind, c_ind)
    return handle_key

def handle_text_change(clue):
    def handler(event):
        clue.text = event.widget.get('1.0', tk.END)
    return handler

def decrease_sz(board, game):
    def handler():
        board.decrease_sz()
        game.redraw_grid()
        game.update_all()
    return handler

def increase_sz(board, game):
    def handler():
        board.increase_sz()
        game.redraw_grid()
        game.update_all()
    return handler


class Game:

    def __init__(self, board):
        self.board = board

        ## Tkinter stuff
        self.window = tk.Tk()
        self.board_frame = tk.Frame(master=self.window, width=400, height=400, bg="black")
        self.info_frame = tk.Frame(master=self.window,width=400, bg="purple")
        #self.board_frame.grid(row=0, column=0, sticky='news')
        #self.info_frame.grid(row=0, column=1, sticky='news')
        self.board_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ## state use for click logic
        self.selected = None # no square selected
        self.sel_dir = ACROSS
        self.placing_blocks = tk.BooleanVar(False)

        self.redraw_grid()

        ## Add info pane stuff 
        #self.turn_label = tk.Label(self.info_frame, text='Turn: White')
        #self.turn_label.grid(row=0, column=0, sticky='nsew')

        """
        frame_canvas = tk.Frame(self.info_frame)
        frame_canvas.grid(row=0, column=0, padx=(0, 5), sticky='nw')
        frame_canvas.grid_rowconfigure(0, weight=1)
        frame_canvas.grid_columnconfigure(0, weight=1)
        # Set grid_propagate to False to allow 5-by-5 buttons resizing later
        frame_canvas.grid_propagate(False)
        """

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
        
        self.info_frame.grid_rowconfigure(0, weight=0)
        self.info_frame.grid_rowconfigure(1, weight=0)
        self.info_frame.grid_rowconfigure(2, weight=0)
        self.info_frame.grid_rowconfigure(3, weight=1)
        self.info_frame.grid_columnconfigure(0, weight=1, minsize=300)


        tmp_frame = tk.Frame(master=self.info_frame, relief=tk.GROOVE, bg='white')
        tmp_frame.grid(row=0, column=0, sticky='nsew')
        self.title = tk.Label(tmp_frame, relief=tk.GROOVE, text='Crossword')
        self.title.pack(side=tk.TOP, fill=tk.X, expand=True)

        tmp_frame = tk.Frame(master=self.info_frame, relief=tk.GROOVE, bg='white')
        tmp_frame.grid(row=1, column=0, sticky='nsew')
        self.ck = tk.Checkbutton(tmp_frame, relief=tk.GROOVE, text='Place Blocks',
            variable=self.placing_blocks, onvalue=1,
             offvalue=0)
        self.ck.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.size_frame = tk.Frame(master=self.info_frame, bg='green')
        self.size_frame.grid(row=2, column=0, sticky='nsew')


        self.larger = tk.Button(self.size_frame, text='larger', command=increase_sz(self.board, self))
        self.smaller = tk.Button(self.size_frame, text='smaller', command=decrease_sz(self.board, self))
        self.larger.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.smaller.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.board.sync_clues_with_board(list(range(self.board.rows)), list(range(self.board.cols)))

        self.parent_clues_frame = tk.Frame(self.info_frame)
        self.parent_clues_frame.grid(row=3, column=0, sticky='news')
        #self.parent_clues_frame.grid(row=2, column=0, pady=(5,0), sticky='news')

        self.parent_clues_frame.grid_rowconfigure(0, minsize=100, weight=1)
        self.parent_clues_frame.grid_columnconfigure(0, minsize=100, weight=1)
        # Set grid_propagate to False to allow 5-by-5 buttons resizing later
        #self.parent_clues_frame.grid_propagate(False)

        # Add a canvas in that frame
        canvas = tk.Canvas(self.parent_clues_frame, bg="green")
        canvas.grid(row=0, column=0, sticky="news")

        # Link a scrollbar to the canvas
        vsb = tk.Scrollbar(self.parent_clues_frame, orient="vertical", command=canvas.yview)
        vsb.grid(row=0, column=1, sticky='ns')
        canvas.configure(yscrollcommand=vsb.set)

        # Create a frame to contain the buttons
        frame_labels = tk.Frame(canvas, bg="blue")

        canvas.create_window((0, 0), window=frame_labels, anchor='nw')
        #frame_labels.pack(fill=tk.BOTH)
        #frame_labels.grid_rowconfigure(0, weight=1)
        #frame_labels.grid_columnconfigure(0, weight=1)
        #frame_labels.grid_columnconfigure(1,  weight=1)

        # Add 1 by 2 moves to the frame

        column_headers = [[ACROSS, DOWN]] #+ [['a', 'b'] for _ in range(10)]
        rows = len(column_headers)
        columns = len(column_headers[0])
        for i in range(0, rows):
            for j in range(0, columns):
                tmp_frame = tk.Frame(master=frame_labels, bg='white')
                tmp_frame.grid(row=i, column=j, sticky='nsew')
                #tmp_frame.update_idletasks()
                column_headers[i][j] = tk.Label(tmp_frame, text=column_headers[i][j])
                if i == 0:
                    column_headers[i][j].config(bg='orange')
                #column_headers[i][j].grid(row=i, column=j, sticky='news')
                column_headers[i][j].pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Update buttons frames idle tasks to let tkinter calculate buttons sizes
        frame_labels.update_idletasks()
        self.frame_labels = frame_labels

        # Resize the canvas frame to show exactly 5-by-5 labels and the scrollbar
        first5columns_width = sum([column_headers[0][j].winfo_width() for j in range(columns)])
        first5rows_height = column_headers[0][0].winfo_height() * 10
        #self.parent_clues_frame.config(height=400)
        #self.frame_labels.config(height=400)

        # Set the canvas scrolling region
        #canvas.config(scrollregion=self.frame_labels.bbox("all"))
        canvas.config(scrollregion=(0,0, 200,1000))
        self.canvas = canvas
        self.vsb = vsb
        self.update_all()

    def get_entry(self, r, c):
        return self.board.board_lst[r][c]

    def switch_sel_dir(self):
        if self.sel_dir == ACROSS:
            self.sel_dir = DOWN
        else:
            self.sel_dir = ACROSS

    def redraw_grid(self):
        for child in self.board_frame.winfo_children():
            child.grid_forget()
            child.destroy()

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
        self.board_frame.columnconfigure(len(self.board.board_lst), weight=0, minsize=0) #, minsize=50
        self.board_frame.rowconfigure(len(self.board.board_lst), weight=0, minsize=0)
        


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
            frame.clue_num_label.config(bg='white')
            txt = entry.clue_num if entry.clue_num is not None else ' '
            frame.clue_num_label.config(text=txt)

            #TODO: adapt font size to board
            #https://stackoverflow.com/questions/24440541/python-tkinter-expanding-fontsize-dynamically-to-fill-frame
            label = tk.Label(master=frame, text=entry.val.upper(), bg=frame.bg, font=("Helvetica", 30))
            #label['font'] = myFont
            label.bind("<Button-1>", handler)
            #label.grid(row=0, column=0, sticky='news')
            label.pack(fill=tk.BOTH, expand=True)
            frame.clue_num_label.lift(label)

            frame.displayed_label = label


    def block(self, r_ind, c_ind):
        self.get_entry(r_ind, c_ind).toggle_blocked()
        self.board.sync_clues_with_board([r_ind], [c_ind])
        self.update_square(r_ind, c_ind)

        # might just want to update_all to be safe
        self.update_all()
        """
        for r_ind, row in enumerate(self.board.board_lst):
            for c_ind, entry in enumerate(row):
                    entry = self.get_entry(r_ind, c_ind)
                    frame = self.board_frame.grid_slaves(row=r_ind, column=c_ind)[0]
                    txt = entry.clue_num if entry.clue_num is not None else ' '
                    frame.clue_num_label.config(text=txt)
        """



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
        """

        for r_ind, row in enumerate(self.board.board_lst):
            for c_ind, entry in enumerate(row):
                self.update_square(r_ind, c_ind)

        self.update_clues()

    def update_clues(self):
        for txt in self.frame_labels.grid_slaves():
            txt.grid_forget()
            txt.destroy()

        ac_lst, do_lst = self.board.clues_as_text()

        def create_clue_list(acr=True):
            if acr:
                header = ACROSS
                col = 0
                all_clues = ac_lst
            else:
                header = DOWN
                col = 1
                all_clues = do_lst

            lbl = tk.Label(self.frame_labels, text=header, bg='orange')
            lbl.grid(row=0, column=col, sticky='news')
            
            for row, clue in enumerate(all_clues):
                c_num, clue_obj = clue
                tmp_frame = tk.Frame(master=self.frame_labels, bg='yellow')
                tmp_frame.grid(row=row+1, column=col, sticky='news')

                num_txt = str(c_num) + '.'
                num_txt += ' ' * (4 - len(num_txt))
                assert len(num_txt) == 4, num_txt
                lbl = tk.Label(tmp_frame, text=num_txt, bg='gray')
                lbl.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

                txt = CustomText(tmp_frame, height=2, width=30)
                txt.insert(tk.INSERT, clue_obj.text)
                txt.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

                on_change = handle_text_change(clue_obj)
                txt.bind("<<TextModified>>", on_change)
        

        create_clue_list(True)
        create_clue_list(False)

        self.canvas.config(scrollregion=(0,0, 100,self.frame_labels.winfo_height() + 50))
        #print(self.frame_labels.winfo_height())


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

# major shoutout to https://stackoverflow.com/questions/40617515/python-tkinter-text-modified-callback
class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        """A text widget that report on internal widget commands"""
        tk.Text.__init__(self, *args, **kwargs)

        # create a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, command, *args):
        cmd = (self._orig, command) + args
        result = self.tk.call(cmd)

        if command in ("insert", "delete", "replace"):
            self.event_generate("<<TextModified>>")

        return result
