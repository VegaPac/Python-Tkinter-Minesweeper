from tkinter import *
import random
import time
import threading


class Cell:
    def __init__(self, root, mines_count, rows, columns):
        self.root = root
        self.width = 4
        self.height = self.width // 2

        self.game_active = True

        self.rows = rows
        self.columns = columns

        self.cells_count = 0
        self.cells = []
        self.cells_by_row = []
        self.cells_by_column = []

        self.zeros = []
        self.adjacent_to_zero_list = []
        self.joined_zero_list = []

        self.mines = []
        self.mine_count = mines_count

        self.score_count = self.mine_count
        self.score_label = Label()

        self.seconds = 0

        self.frame = Frame(self.root)
        self.frame.grid(row=self.rows, column=0, columnspan=self.columns)
        if self.columns > 10:
            self.filler = Label(self.frame, width=20)
            self.filler.grid(row=0, column=1)

        self.timer_label = Label()

        self.button_w = 0
        self.button_h = 0

        self.flag_image = PhotoImage(file="assets/flag32x32.png")
        self.mine_image = PhotoImage(file="assets/mine32x32.png")

        self.happy_face_image = PhotoImage(file="assets/happyface128x128.png")
        self.sad_face_image = PhotoImage(file="assets/sadface128x128.png")

        self.number1_image = PhotoImage(file="assets/numbers/number1.png")
        self.number2_image = PhotoImage(file="assets/numbers/number2.png")
        self.number3_image = PhotoImage(file="assets/numbers/number3.png")
        self.number4_image = PhotoImage(file="assets/numbers/number4.png")
        self.number5_image = PhotoImage(file="assets/numbers/number5.png")
        self.number6_image = PhotoImage(file="assets/numbers/number6.png")
        self.number7_image = PhotoImage(file="assets/numbers/number7.png")
        self.number8_image = PhotoImage(file="assets/numbers/number8.png")
        self.number9_image = PhotoImage(file="assets/numbers/number9.png")

    def cells_creator(self, rows=0, columns=0, is_flagged=False, is_mine=False, surrounding_count=0):
        row = 0
        column = 0
        while self.cells_count < rows * columns:
            button = Button(self.root, width=self.width, height=self.height)
            button.configure(command=lambda r=row, c=column: self.clicked(r, c))
            self.cells.append([row, column, surrounding_count, is_flagged, is_mine, button])
            if column + 1 == columns:
                row += 1
                column = 0
            else:
                column += 1

            self.cells_count += 1
            self.button_w = button.winfo_reqwidth() - 5
            self.button_h = self.button_w

    def grid_cells(self):
        x = 0
        for i in self.cells:
            button = self.cells[x][-1]
            button_row = int(i[0])
            button_column = int(i[1])
            button.grid(row=button_row, column=button_column)
            x += 1

    def mine_creator(self, mines_count):
        created_mines = 0
        while mines_count > created_mines:
            created_mines += 1
            chosen_mine = random.choice(self.cells)
            if chosen_mine in self.mines:
                created_mines -= 1
            # chosen_mine[-1].config(text="m")  # ACTIVATE TO SEE THE MINES
            chosen_mine[-2] = True
            self.mines.append(chosen_mine)

    def flag_binding(self):
        for cell in self.cells:
            cell[-1].bind("<Button-3>", lambda event, button=cell[-1]: self.flag_placement(event, button))
            cell[-1].config(width=4, height=2, padx=0, pady=0)

    def flag_placement(self, event, button):
        _ = event
        for cell in self.cells:
            if cell[-1] == button:
                if cell[3]:
                    # The player is removing a flag.
                    cell[3] = False
                    cell[-1].config(image="")
                    cell[-1].config(width=4, height=2, padx=0, pady=0)
                    self.score_count += 1
                    if cell[4]:
                        self.mine_count += 1
                elif self.score_count > 0:
                    # The player is placing a flag.
                    cell[3] = True
                    cell[-1].config(image=self.flag_image, width=30, height=33, padx=0, pady=0)
                    if cell[4]:
                        self.mine_count -= 1
                    self.score_count -= 1
                break

        # Update the score and check for victory.
        self.display_score()
        self.root.update()
        if self.mine_count == 0:
            self.game_active = False
            self.end_game(True)

    def surrounding_mine_counter(self):
        for i in self.cells:
            for element in self.cells:
                if element[0] in range(i[0] - 1, i[0] + 2):
                    if element[1] in range(i[1] - 1, i[1] + 2):
                        if element[-2]:
                            i[2] += 1
        self.zeros_counter()

    def zeros_counter(self):
        for i in self.cells:
            if i[2] == 0:
                self.zeros.append(i)

    def clicked(self, row, column):
        clicked_cell = None
        for cell in self.cells:
            if cell[0] == row and cell[1] == column:
                clicked_cell = cell
                break
        if clicked_cell in self.zeros:
            self.concatenate_reveal(clicked_cell)
        elif clicked_cell in self.mines:
            self.game_active = False
            self.end_game(False, clicked_cell)
        else:
            self.reveal_cell(clicked_cell)

    def reveal_cell(self, cell):
        cell[-1].destroy()
        if cell[-2]:
            cell[-1] = Label(self.root, image=self.mine_image)
        elif cell[2] == 1:
            cell[-1] = Label(self.root, image=self.number1_image)
        elif cell[2] == 2:
            cell[-1] = Label(self.root, image=self.number2_image)
        elif cell[2] == 3:
            cell[-1] = Label(self.root, image=self.number3_image)
        elif cell[2] == 4:
            cell[-1] = Label(self.root, image=self.number4_image)
        elif cell[2] == 5:
            cell[-1] = Label(self.root, image=self.number5_image)
        elif cell[2] == 6:
            cell[-1] = Label(self.root, image=self.number6_image)
        elif cell[2] == 7:
            cell[-1] = Label(self.root, image=self.number7_image)
        elif cell[2] == 8:
            cell[-1] = Label(self.root, image=self.number8_image)
        elif cell[2] == 9:
            cell[-1] = Label(self.root, image=self.number9_image)
        else:
            cell[-1] = Label(self.root, width=4, height=2)
        cell[-1].config(padx=2, pady=1)
        cell[-1].grid(row=cell[0], column=cell[1])

    def adjacent_to_zero(self):
        for zero in self.zeros:
            adjacent_to_zero = [zero]
            for cell in self.cells:
                if abs(zero[0] - cell[0]) == 1 or abs(zero[0] - cell[0]) == 0:
                    if abs(zero[1] - cell[1]) == 1 or abs(zero[1] - cell[1]) == 0:
                        if zero != cell:
                            adjacent_to_zero.append(cell)
            self.adjacent_to_zero_list.append(adjacent_to_zero)

    def group_zeros(self):
        visited = set()  # Keep track of visited zero groups
        grouped_zeros = []

        for i, zero_group in enumerate(self.adjacent_to_zero_list):
            if i in visited:
                continue  # Skip visited groups

            current_group = zero_group.copy()
            visited.add(i)

            for j in range(i + 1, len(self.adjacent_to_zero_list)):
                if j in visited:
                    continue  # Skip visited groups

                common_elements = [cell for cell in self.adjacent_to_zero_list[j] if cell in current_group]

                if common_elements:
                    current_group.extend(cell for cell in self.adjacent_to_zero_list[j] if cell not in current_group)
                    visited.add(j)

            grouped_zeros.append(current_group)

        self.joined_zero_list = grouped_zeros

    def concatenate_reveal(self, clicked_cell):
        for zero_group in self.joined_zero_list:
            if clicked_cell in zero_group:
                for cell in zero_group:
                    self.reveal_cell(cell)

    def end_game(self, game_status, clicked_cell=None):
        if game_status:
            victory_w = self.button_w * self.columns
            victory_h = self.button_h * self.rows
            for widget in self.root.winfo_children():
                widget.destroy()
            self.cells = []
            face_label = Label(self.root, image=self.happy_face_image, width=victory_w, height=victory_h, text="You Won", font=("DePixel Bold", 25), compound=BOTTOM)
            score_label = Label(self.root, font=("DePixel Bold", 8), text=f"Time: {self.seconds}")
            face_label.pack()
            score_label.pack()

        elif not game_status:
            for cell in self.cells:
                if cell != clicked_cell:
                    self.reveal_cell(cell)
            clicked_cell[-1].destroy()
            clicked_cell[-1] = Label(self.root, image=self.mine_image, bg="red")
            clicked_cell[-1].config(padx=2, pady=1)
            clicked_cell[-1].grid(row=clicked_cell[0], column=clicked_cell[1])
            self.root.update()
            time.sleep(3)
            victory_w = self.button_w * self.columns
            victory_h = self.button_h * self.rows
            for widget in self.root.winfo_children():
                widget.destroy()
            self.cells = []
            face_label = Label(self.root, image=self.sad_face_image, width=victory_w, height=victory_h, text="You Lost",
                               compound=BOTTOM, font=("DePixel Bold", 25))
            face_label.pack()

        play_again_button = Button(self.root, text="Play Again", font=("DePixel Bold", 8), padx=5, width=10, command=self.play_again)
        quit_button = Button(self.root, text="Quit", font=("DePixel Bold", 8), padx=5, width=10, command=exit)
        play_again_button.pack()
        quit_button.pack()
        self.root.update()

    def play_again(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        menu = Menu(self.root)
        menu.create_menu()

    def display_score(self):
        self.score_label.destroy()
        self.score_label = Label(self.frame, font=("DePixel Bold", 8), text=f"Remaining Mines: {self.score_count}")
        self.score_label.grid(row=0, column=0)
        self.root.update()

    def timer(self):
        self.timer_label = Label(self.frame, font=("DePixel Bold", 8), text=f"Time: {self.seconds}")
        self.timer_label.grid(row=0, column=2)
        while self.game_active:
            self.timer_label.config(text=f"Time: {self.seconds}")
            time.sleep(1)
            self.seconds += 1


class Menu:
    def __init__(self, root):
        self.root = root

        self.mines = 0
        self.rows = 0
        self.columns = 0

        self.easy_mode_divisor = 8
        self.medium_mode_divisor = 6
        self.hard_mode_divisor = 4

        self.small_size_rows = 10
        self.small_size_columns = 10
        self.medium_size_rows = 12
        self.medium_size_columns = 15
        self.large_size_rows = 12
        self.large_size_columns = 25

        self.frame = Frame(self.root)
        self.frame.pack()

        self.flag_image128 = PhotoImage(file="assets/flag32x32.png")

    def create_menu(self):
        title = Label(self.frame, text="MineSweeper", image=self.flag_image128, compound="right", font=("DePixel Bold", 15), padx=5, pady=5)

        size_label = Label(self.frame, text="Size: ", font=("DePixel Bold", 8))
        button_small = Button(self.frame, text="Small", font=("DePixel Bold", 8), command=lambda: self.set_board_size(self.small_size_rows, self.small_size_columns), padx=5, width=10)
        button_s_medium = Button(self.frame, text="Medium", font=("DePixel Bold", 8), command=lambda: self.set_board_size(self.medium_size_rows, self.medium_size_columns), padx=5, width=10)
        button_large = Button(self.frame, text="Large", font=("DePixel Bold", 8), command=lambda: self.set_board_size(self.large_size_rows, self.large_size_columns), padx=5, width=10)

        difficulty_label = Label(self.frame, text="Difficulty: ", font=("DePixel Bold", 8), padx=5)
        button_easy = Button(self.frame, text="Easy", font=("DePixel Bold", 8), command=lambda: self.set_difficulty(self.easy_mode_divisor), padx=5, width=10)
        button_d_medium = Button(self.frame, text="Medium", font=("DePixel Bold", 8), command=lambda: self.set_difficulty(self.medium_mode_divisor), padx=5, width=10)
        button_hard = Button(self.frame, text="Hard", font=("DePixel Bold", 8), command=lambda: self.set_difficulty(self.hard_mode_divisor), padx=5, width=10)

        title.grid(row=0, column=0, columnspan=4)
        size_label.grid(row=1, column=0)
        button_small.grid(row=1, column=1)
        button_s_medium.grid(row=1, column=2)
        button_large.grid(row=1, column=3)
        difficulty_label.grid(row=2, column=0)
        button_easy.grid(row=2, column=1)
        button_d_medium.grid(row=2, column=2)
        button_hard.grid(row=2, column=3)

    def set_board_size(self, rows=0, columns=0):
        self.rows = rows
        self.columns = columns
        self.run_game()

    def set_difficulty(self, difficulty=0):
        if self.rows * self.columns > 0:
            self.mines = self.rows * self.columns // difficulty
            self.run_game()

    def run_game(self):
        if self.mines > 0 and self.rows > 0 and self.columns > 0:
            for widget in self.root.winfo_children():
                widget.destroy()

            cell = Cell(self.root, self.mines, self.rows, self.columns)
            cell.cells_creator(self.rows, self.columns)
            cell.grid_cells()
            cell.mine_creator(mines_count=self.mines)
            cell.display_score()
            cell.surrounding_mine_counter()
            cell.flag_binding()
            cell.adjacent_to_zero()
            cell.group_zeros()

            timer = threading.Thread(target=cell.timer, daemon=True)
            timer.start()
