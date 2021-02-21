import os
import tkinter as tk


def _create_square(self, x, y, side, width, **kwargs):
    return self.create_rectangle(x, y, x + side, y + side, width=width, **kwargs)

tk.Canvas.create_square = _create_square


def load_partitions():
    _, _, partitions = next(os.walk("./extended/"))
    partitions = [read_partition(partition) for partition in partitions]
    return partitions


def read_partition(filename):
    partition = []
    with open("./extended/" + filename) as file:
        for subset in file.readlines():
            subset = subset.strip()
            subset = list(map(int, subset.split()))
            partition.append(subset)
    return partition


class Viewing:
    COLORS = ["red", "green", "RoyalBlue1", "orange", "purple"]

    def __init__(self, root, side, width):
        super().__init__()

        canvas = tk.Canvas(root, width=4 * (side + width) + 2 * width,
                           height=46 * (side + width) + 2 * width,
                           highlightthickness=0)

        self.canvas = canvas
        self.N = 4 * 44 + 3
        self.side = side
        self.width = width
        self.partitions = load_partitions()
        self._i = tk.IntVar()
        self.squares = None

        self.draw_squares()
        self.display()

        canvas.bind('<Left>', self.previous)
        canvas.bind('<Right>', self.next)
        canvas.focus_set()

        label = tk.Label(root, textvariable=self._i, font=("Courier", 44))
        label.grid(column=1, row=1)
        canvas.grid(column=2, row=1)

        root.grid_rowconfigure(0, weight=2)
        root.grid_rowconfigure(1, weight=1)
        root.grid_rowconfigure(2, weight=2)
        root.grid_columnconfigure(0, weight=2)
        root.grid_columnconfigure(1, weight=1)
        root.grid_columnconfigure(2, weight=1)
        root.grid_columnconfigure(3, weight=2)

    @property
    def i(self):
        return self._i.get()

    @i.setter
    def i(self, value):
        self._i.set(value % len(self.partitions))

    def display(self):
        partition = self.partitions[self.i]
        for i, subset in enumerate(partition):
            color = self.COLORS[i]
            for n in subset:
                self.canvas.itemconfig(self.squares[n], fill=color)

    def draw_square(self, n):
        side = self.side + self.width
        mid = side // 2
        line, col = divmod(n + 1, 4)
        x = self.width + col * self.side
        y = self.width + line * self.side

        square = self.canvas.create_square(x, y, self.side, width=self.width)
        self.canvas.create_text(x + mid, y + mid, text=str(n))
        return square

    def draw_squares(self):
        self.squares = [None]
        for n in range(1, self.N + 1):
            square = self.draw_square(n)
            self.squares.append(square)

    def next(self, _):
        self.i += 1
        self.display()

    def previous(self, _):
        self.i -= 1
        self.display()

if __name__ == '__main__':
    side = 22
    width = 3

    root = tk.Tk()
    root.state("zoomed")

    Viewing(root, side, width)

    root.mainloop()
