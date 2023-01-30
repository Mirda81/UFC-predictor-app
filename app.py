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

app.fighter1_combo.config(values=fighter_list)
app.fighter2_combo.config(values=fighter_list)
app.fighter1_combo.bind("<KeyRelease>",
                        lambda event: app.fighter1_combo.config(values=functions.filter_names(fighter_list,app.fighter1_combo.get())))
app.fighter2_combo.bind("<KeyRelease>",
                        lambda event: app.fighter2_combo.config(values=functions.filter_names(fighter_list,app.fighter2_combo.get())))

root.mainloop()

