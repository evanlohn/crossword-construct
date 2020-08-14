# a simple chess board state stored as a 2-D array


class Board:

    def __init__(self, sz):
        self.rows, self.cols = sz, sz
        self.board_lst = [[Entry() for i in range(self.cols)] for j in range(self.rows)]
        self.ac_clue_list = [[] for i in range(self.rows)]
        self.do_clue_list = [[] for i in range(self.cols)]
        self.sync_clues_with_board(list(range(self.rows)), list(range(self.cols)))

    def increase_sz(self):
        self.rows += 1
        self.cols += 1
        for lst in self.board_lst:
            lst.append(Entry())
        self.board_lst.append([Entry() for _ in range(self.rows)])
        self.ac_clue_list.append([])
        self.do_clue_list.append([])
        self.sync_clues_with_board(list(range(self.rows)), list(range(self.cols)))

    def decrease_sz(self):
        if self.rows <= 2:
            return
        self.rows -= 1
        self.cols -= 1
        self.board_lst.pop(-1)
        for lst in self.board_lst:
            lst.pop(-1)

        self.ac_clue_list.pop(-1)
        self.do_clue_list.pop(-1)
        self.sync_clues_with_board(list(range(self.rows)), list(range(self.cols)))

    def is_wall(self, row, col):
        return row < 0 or col < 0 or self.board_lst[row][col].blocked

    def is_across_clue(self, row, col):
        return self.is_wall(row, col - 1)

    def is_down_clue(self, row, col):
        return self.is_wall(row - 1, col)

    def recalc_clue_nums(self):
        ctr = 1
        for row in range(self.rows):
            for col in range(self.cols):
                entry = self.board_lst[row][col]
                entry.clue_num = None
                if entry.blocked:
                    continue
                is_across = self.is_across_clue(row, col)
                is_down = self.is_down_clue(row, col)
                if is_across or is_down:
                    entry.clue_num = ctr
                    ctr += 1
        return

    def handle_clue_end(self, prev_clue_ind, row_clues, row, col, clue_start_col, across=True):
        found_clue = None
        if across:
            cond = lambda: row_clues[prev_clue_ind].start[1] < col
            endpoints = ((row, clue_start_col), (row, col))
        else:
            cond = lambda: row_clues[prev_clue_ind].start[0] < row
            endpoints = ((clue_start_col, col), (row, col))

        which = 1 if across else 0

        while prev_clue_ind < len(row_clues) and cond():
            prev_clue = row_clues[prev_clue_ind]
            prev_clue_ind += 1 # only consider each prev clue once
            pclue_end_col = prev_clue.end[which]
            if pclue_end_col > clue_start_col:
                #found overlap
                found_clue = prev_clue
                found_clue.set(endpoints[0], endpoints[1])
                break

        if found_clue is None:
            found_clue = Clue(endpoints[0], endpoints[1])

        return prev_clue_ind, found_clue

    #whee algorithm go brrr
    def sync_clues_with_board(self, rows_changed, cols_changed):
        self.recalc_clue_nums()

        for row in rows_changed:
            row_clues = self.ac_clue_list[row]
            new_row_clues = []
            prev_clue_ind = 0 # where to start looking for a matching clue
            clue_start_col = None
            for col in range(self.cols):
                entry = self.board_lst[row][col]
                if entry.blocked: # handle previous clue assignment
                    if clue_start_col is not None:
                        prev_clue_ind, found_clue = self.handle_clue_end(prev_clue_ind, row_clues, row, col, clue_start_col)
                        new_row_clues.append(found_clue)

                    clue_start_col = None
                    continue

                if self.is_across_clue(row, col): # found a clue starter
                    assert clue_start_col is None
                    clue_start_col = col
                entry.across_clue = None

            if clue_start_col is not None:
                # handle previous clue assignment
                _, found_clue = self.handle_clue_end(prev_clue_ind, row_clues, row, col+1, clue_start_col)
                new_row_clues.append(found_clue)

            self.ac_clue_list[row] = new_row_clues
            for row_clue in new_row_clues:
                self.board_lst[row_clue.start[0]][row_clue.start[1]].across_clue = row_clue

        for col in cols_changed:
            col_clues = self.do_clue_list[col]
            new_col_clues = []
            prev_clue_ind = 0 # where to start looking for a matching clue
            clue_start_row = None
            for row in range(self.rows):
                entry = self.board_lst[row][col]
                if entry.blocked: # handle previous clue assignment
                    if clue_start_row is not None:
                        prev_clue_ind, found_clue = self.handle_clue_end(prev_clue_ind, col_clues, row, col, clue_start_row, across=False)
                        new_col_clues.append(found_clue)

                    clue_start_row = None
                    continue

                if self.is_down_clue(row, col): # found a clue starter
                    assert clue_start_row is None
                    clue_start_row = row
                entry.down_clue = None

            if clue_start_row is not None:
                # handle previous clue assignment
                _, found_clue = self.handle_clue_end(prev_clue_ind, col_clues, row + 1, col, clue_start_row, across = False)
                new_col_clues.append(found_clue)

            self.do_clue_list[col] = new_col_clues
            for col_clue in new_col_clues:
                self.board_lst[col_clue.start[0]][col_clue.start[1]].down_clue = col_clue


    def clues_as_text(self):
        ac_flat = []
        for row, clue_list in enumerate(self.ac_clue_list):
            for clue in clue_list:
                c_num = self.board_lst[clue.start[0]][clue.start[1]].clue_num
                ac_flat.append((c_num, clue))

        do_flat = []
        for col, clue_list in enumerate(self.do_clue_list):
            for clue in clue_list:
                c_num = self.board_lst[clue.start[0]][clue.start[1]].clue_num
                do_flat.append((c_num, clue))

        return ac_flat, sorted(do_flat, key=lambda x: x[0])


class Clue:
    # represents a clue for a particular sequence of entries on the board
    def __init__(self, start, end):
        self.start = start #inclusive
        self.end = end #not inclusive
        self.text = ''

    def set(self, start, end):
        self.start = start
        self.end = end


class Entry:
    # represents a square on the board

    def __init__(self, val='', blocked=False):
        self.val = val # will normally be a letter or ''; could also be a string (rebus)
        self.blocked = blocked
        self.clue_num = None # separate from Clue because these can move around as the board changes
        self.across_clue = None
        self.down_clue = None

    def toggle_blocked(self):
        self.blocked = not self.blocked


