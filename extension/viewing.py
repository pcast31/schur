import os
import tkinter as tk


def _create_square(self, x, y, side, width, **kwargs):
    return self.create_rectangle(x, y, x + side, y + side, width=width, **kwargs)

tk.Canvas.create_square = _create_square


def load_partitions(folder, names_folder=None):
    if names_folder is None:
        names_folder = folder

    _, _, partitions = next(os.walk(names_folder))
    partitions.sort()

    partitions = [read_partition(folder + '/' + partition)
                  for partition in partitions]
    return partitions


def read_partition(path):
    partition = []
    with open(path) as file:
        for subset in file.readlines():
            subset = subset.strip()
            subset = list(map(int, subset.split()))
            partition.append(subset)
    return partition


class Viewing:
    COLORS = ["red", "green4", "DarkOrange1", "deep sky blue", "DarkOrchid1"]

    def __init__(self, root, side, width):
        super().__init__()

        canvas = tk.Canvas(root, width=4 * (side + width) + 2 * width,
                           height=46 * (side + width) + 2 * width,
                           highlightthickness=0)

        self.root = root
        self.canvas = canvas
        self._i = tk.IntVar()
        self.label = tk.Label(root, textvariable=self._i, font=("Courier", 44))

        self.side = side
        self.width = width
        self.font = ('Times', -(9 * self.side // 16))
        self.squares = None

        self.N = 4 * 44 + 3
        self.partitions = load_partitions('extended')
        self.base_partitions = load_partitions('partitions', 'extended')

        self.draw_squares()
        self.display()
        self.canvas_actions()
        self.grid()

    @property
    def i(self):
        return self._i.get()

    @i.setter
    def i(self, value):
        self._i.set(value % len(self.partitions))

    def canvas_actions(self):
        self.canvas.tag_bind("square", "<Enter>", self.on_enter)
        self.canvas.tag_bind("square", "<Leave>", self.on_leave)

        self.canvas.bind('<Left>', self.previous)
        self.canvas.bind('<Right>', self.next)

        self.canvas.focus_set()

    def display(self):
        partition = self.partitions[self.i]
        for i, subset in enumerate(partition):
            color = self.COLORS[i]
            for n in subset:
                self.canvas.itemconfig(self.squares[n], fill=color)

        for line in range(1, 45):
            for text_id in self.canvas.find_withtag(f"L{line}"):
                self.canvas.itemconfig(text_id, fill='black')
                self.canvas.itemconfig(text_id, font=self.font)
        self.on_enter()

    def draw_square(self, n):
        side = self.side + self.width
        mid = side // 2 - self.width // 2

        line, col = divmod(n + 1, 4)
        x = self.width + col * self.side
        y = self.width + line * self.side

        square = self.canvas.create_square(x, y, self.side, width=self.width,
                                           tags="square")
        self.canvas.create_text(x + mid, y + mid, text=str(n), state='disabled',
                                font=self.font, tags=f"L{line}")
        return square

    def draw_squares(self):
        self.squares = [None]
        for n in range(1, self.N + 1):
            square = self.draw_square(n)
            self.squares.append(square)

    def find_lines(self, line):
        if line == 0 or line == 45:
            return

        for subset in self.base_partitions[self.i]:
            if line in subset:
                subset = subset
                break

        target = line + 1
        for i, a in enumerate(subset):
            for j in range(i, len(subset)):
                b = subset[j]
                tot = a + b
                if tot > target:
                    break
                if a != b and a + b == target:
                    yield a
                    yield b

    def find_text_ids(self):
        try:
            square_id = self.canvas.find_withtag('current')[0]
        except:
            return
        n = self.squares.index(square_id)
        line = (n + 1) // 4

        for line in self.find_lines(line):
            for text_id in self.canvas.find_withtag(f"L{line}"):
                yield text_id

    def grid(self):
        self.label.grid(column=1, row=1)
        self.canvas.grid(column=2, row=1)

        self.root.grid_rowconfigure(0, weight=2)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=2)
        self.root.grid_columnconfigure(0, weight=2)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_columnconfigure(3, weight=2)

    def next(self, *args):
        self.i += 1
        self.display()

    def on_enter(self, *args):
        font = (self.font[0], self.font[1], 'bold')

        for text_id in self.find_text_ids():
            self.canvas.itemconfig(text_id, fill='yellow')
            self.canvas.itemconfig(text_id, font=font)

    def on_leave(self, *args):
        for text_id in self.find_text_ids():
            self.canvas.itemconfig(text_id, fill='black')
            self.canvas.itemconfig(text_id, font=self.font)

    def previous(self, *args):
        self.i -= 1
        self.display()


if __name__ == '__main__':
    root = tk.Tk()
    root.state("zoomed")

    width = 2
    side = root.winfo_screenheight() // 46 - width + 1

    Viewing(root, side, width)

    root.mainloop()
