import random
import time
from tkinter import *
import threading


class Piece:
    width = 20
    canvas = None

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.i = None

    def copy(self, piece):
        self.x, self.y, self.i = piece.x, piece.y, piece.i

    def is_equal(self, piece):
        return self.x == piece.x and self.y == piece.y

    def move(self, vx, vy):
        self.x, self.y = self.x + Piece.width * vx, self.y + Piece.width * vy

    def draw(self):
        self.i = Piece.canvas.create_rectangle(self.x, self.y, self.x + Piece.width, self.y + Piece.width, fill="green")

    def erase(self):
        Piece.canvas.delete(self.i)


class App:
    loc = ["blue", "red", "yellow", "purple", "pink"]
    width = 600
    height = 650

    def __init__(self):
        self.gameCanvas = self.playFrame = self.homeFrame = self.playButton = None
        self.vx = self.vy = self.scoreLabel = self.statusFrame = None
        self.treatP = self.snake = self.endP = self.startP = self.paused = None
        self.window = Tk()
        self.window.title('Snake by SrinSxit')
        self.make_play_frame()
        self.make_home_frame()
        self.pause_game()

        class Thread(threading.Thread):
            def __init__(self, app_ptr):
                threading.Thread.__init__(self)
                self.app_ptr = app_ptr

            def run(self):
                while True:
                    time.sleep(0.1)
                    if not self.app_ptr.paused:
                        self.app_ptr.update()

        self.th = Thread(self)
        self.th.setDaemon(True)
        self.th.start()

    def make_home_frame(self):
        # add widgets of home frame
        self.homeFrame = Frame(self.window, width=App.width, height=App.height)
        self.homeFrame.grid(row=0, column=0)
        self.playButton = Button(self.homeFrame, text="Play", command=self.resume_game)
        self.playButton.place(relx=0.5, rely=0.5, anchor=CENTER)

    def make_play_frame(self):
        # add widgets of play frame
        self.playFrame = Frame(self.window, width=App.width, height=App.height)
        self.playFrame.grid(row=0, column=0)
        # children of main game frame
        self.make_status_frame()
        self.gameCanvas = Piece.canvas = Canvas(self.playFrame, width=App.width, height=App.width, bg="black")
        self.gameCanvas.pack()
        self.playFrame.bind('<Left>', lambda e: self.move('L'))
        self.playFrame.bind('<Right>', lambda e: self.move('R'))
        self.playFrame.bind('<Up>', lambda e: self.move('U'))
        self.playFrame.bind('<Down>', lambda e: self.move('D'))
        self.make_game()

    def make_status_frame(self):
        self.statusFrame = Frame(self.playFrame, width=App.width, height=App.height - App.width)
        self.statusFrame.pack()
        self.statusFrame.grid_propagate(False)
        Grid.rowconfigure(self.statusFrame, index=0, weight=1)
        Grid.columnconfigure(self.statusFrame, index=0, weight=1)
        Grid.columnconfigure(self.statusFrame, index=1, weight=1)
        Grid.columnconfigure(self.statusFrame, index=2, weight=1)
        Button(self.statusFrame, text="Home", command=self.reset_game).grid(row=0, column=0, sticky="ewns", padx=5,
                                                                            pady=5)
        self.scoreLabel = Label(self.statusFrame, text="")
        self.scoreLabel.grid(row=0, column=1, sticky="ewns", padx=5, pady=5)
        Button(self.statusFrame, text="Pause", command=self.pause_game).grid(row=0, column=2, sticky="ewns", padx=5,
                                                                             pady=5)

    def display_home(self):
        self.homeFrame.lift()
        self.homeFrame.focus()

    def display_play(self):
        self.playFrame.lift()
        self.playFrame.focus()

    def pause_game(self):
        self.paused = True
        self.display_home()

    def resume_game(self):
        self.paused = False
        self.display_play()

    def make_game(self):
        self.startP = Piece(
            Piece.width * random.randint(App.width // Piece.width // 3, 2 * App.width // Piece.width // 3),
            Piece.width * random.randint(App.width // Piece.width // 3, 2 * App.width // Piece.width // 3))
        self.startP.draw()
        self.endP = Piece(0, 0)
        self.snake = [self.startP]
        self.gen_treat()
        self.vx = random.randint(0, 1)
        if self.vx == 0:
            self.vy = 1
        else:
            self.vy = 0

    def reset_game(self):
        length = len(self.snake)
        self.endP.erase()
        self.treatP.erase()
        for i in range(length):
            self.snake[i].erase()
        self.make_game()
        self.pause_game()

    def gen_treat(self):
        while True:
            self.treatP = Piece(Piece.width * random.randint(0, App.width // Piece.width - 1),
                                Piece.width * random.randint(0, App.width // Piece.width - 1))
            for piece in self.snake:
                if piece.is_equal(self.treatP):
                    break
            else:
                break
        self.treatP.draw()
        self.gameCanvas.itemconfig(self.treatP.i, fill=App.loc[random.randint(0, len(App.loc) - 1)])

    def move(self, direction):
        if not self.paused:
            if direction == 'L':
                self.vx, self.vy = -1, 0
            elif direction == 'R':
                self.vx, self.vy = 1, 0
            elif direction == 'U':
                self.vx, self.vy = 0, -1
            elif direction == 'D':
                self.vx, self.vy = 0, 1

    def snake_inside(self):
        x, y = self.startP.x, self.startP.y
        return 0 <= x <= App.width - Piece.width and 0 <= y <= App.width - Piece.width

    def update(self):
        length = len(self.snake)
        if length > 1 and self.startP.is_equal(self.endP) or not self.snake_inside():
            self.scoreLabel.config(text="Score : " + str(length - 1) + "\nGame Over")
            self.paused = True
            return
        for i in range(1, length):
            if self.startP.is_equal(self.snake[i]) or self.startP.is_equal(self.endP) or not self.snake_inside():
                self.scoreLabel.config(text="Score : " + str(length - 1) + "\nGame Over")
                self.paused = True
                return
        self.scoreLabel.config(text="Score : " + str(length - 1))
        if self.startP.is_equal(self.treatP):
            self.treatP.erase()
            self.treatP.copy(self.snake[length - 1])
            self.snake.append(self.treatP)
            length = length + 1
            self.gen_treat()
        self.endP.copy(self.snake[length - 1])
        for i in range(length - 1, 0, -1):
            self.snake[i].copy(self.snake[i - 1])
        self.startP.move(self.vx, self.vy)
        self.startP.draw()
        self.endP.erase()


foo = App()
foo.window.mainloop()