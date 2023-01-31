from tk_form import FighterComparison
from tkinter import *
from Fighter_class import Fighter
import pandas as pd
import functions
import ttkbootstrap as tk
from ttkbootstrap.constants import *

df_fighter = pd.read_csv('Preprocessing/df_skills.csv')

root = tk.Window(themename="cyborg")
root.title("Fights prediction")
root.config()
root.resizable(False, False)
root.geometry("800x750")
icon = PhotoImage(file="icon.png")
root.iconphoto(True, icon)
app = FighterComparison(root)

fighter_list = df_fighter['FIGHTER'].tolist()
# handle combo lists events
functions.combos_handler(app,fighter_list)



root.mainloop()

