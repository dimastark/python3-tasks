"""End of the game and working with scoreboard"""
import tkinter as tk
import re
import start


def get_scores():
    """Read scores"""
    scr = []
    pars = re.compile(r'[\w\s\d]+?: \d+')
    try:
        file = open("scores.txt", encoding='utf-8')
    except IOError:
        scr.append("No scores")
    else:
        try:
            for line in file:
                if pars.match(line):
                    scr.append(line[:-1])
            scr = dict(zip(scr, scr)).values()
            scr = sorted(scr, key=lambda x: int(x.split(' ')[-1]), reverse=True)
        finally:
            file.close()
    return scr

def end(score):
    """End of the game with 'score' scores

       Args:
         score: count of points in end of the game
    """
    def scores_write():
        """Write scores"""
        name = str(nick.get())
        if len(name) > 20 and len(name) > 0:
            return None
        file = open("scores.txt", mode='a', encoding='utf-8')
        try:
            file.write(name+': '+str(score)+'\n')
        finally:
            file.close()
        root.destroy()

    def rest_write():
        """Write scores"""
        scores_write()
        start.main()

    root = tk.Tk()
    frame = tk.Frame(root)
    lab1 = tk.Label(frame, text="Enter your name (max: 20)", font="Arial 12")
    nick = tk.Entry(frame, bd=5, width=40)
    send = tk.Button(frame, text="Send and close", command=scores_write)
    rest = tk.Button(frame, text="Send and restart", command=rest_write)
    listbox = tk.Listbox(root, width=60)
    frame.pack()
    lab1.pack()
    nick.pack()
    send.pack(side="left")
    rest.pack(side="right")
    listbox.pack()
    scr = get_scores()
    for line in scr:
        listbox.insert(tk.END, line)
    root.mainloop()


