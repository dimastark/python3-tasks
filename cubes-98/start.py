"""Start of the lines game"""


from tkinter import Scale, Label, Button, Tk
from tkinter import HORIZONTAL as H
import lines
import scores


def main():
    """Configurate the game"""
    def start_game():
        """Starting"""
        rng = rang.get()
        cmb = combo.get()
        clr = colors.get()
        if cmb <= rng:
            root.destroy()
            score = lines.game(rng, cmb, clr)
            if score:
                scores.end(score)

    root = Tk()
    rang = Scale(root, orient=H, length=300, from_=5, to=20, resolution=1)
    combo = Scale(root, orient=H, length=300, from_=3, to=10, resolution=1)
    colors = Scale(root, orient=H, length=300, from_=3, to=8, resolution=1)
    lab1 = Label(root, text="Rang of the field", font="Arial 12")
    lab2 = Label(root, text="Size of combo-line (<=rang)", font="Arial 12")
    lab3 = Label(root, text="Colors count", font="Arial 12")
    start = Button(root, text="Start", command=start_game)
    lab1.pack()
    rang.pack()
    lab2.pack()
    combo.pack()
    lab3.pack()
    colors.pack()
    start.pack()
    root.mainloop()

if __name__ == "__main__":
    main()
