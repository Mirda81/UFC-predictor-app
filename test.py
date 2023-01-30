from form_helper import FighterComparison
from tkinter import *

root = Tk()
root.title("Fights prediction")
root.config(bg="black")
root.resizable(False, False)
root.geometry("800x750")
icon = PhotoImage(file="icon.png")
root.iconphoto(True, icon)
app = FighterComparison(root)
root.mainloop()

