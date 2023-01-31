from tk_form import FighterComparison
from tkinter import *
from Fighter_class import Fighter
import pandas as pd
import functions

df_fighter = pd.read_csv('Preprocessing/df_skills.csv')

root = Tk()
root.title("Fights prediction")
root.config(bg="black")
root.resizable(False, False)
root.geometry("800x750")
icon = PhotoImage(file="icon.png")
root.iconphoto(True, icon)
app = FighterComparison(root)

fighter_list = df_fighter['FIGHTER'].tolist()
# handle combo lists events
functions.combos_handler(app,fighter_list)



root.mainloop()

