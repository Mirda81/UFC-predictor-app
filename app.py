from tk_form import FighterComparison
from tkinter import *
import pandas as pd
import functions
import ttkbootstrap as tk
from keras.models import load_model

df_fighter = pd.read_csv('Preprocessing/df_skills.csv')
model = load_model('model/model.h5')
model.load_weights('model/my_model_weights.h5')  # to load
root = tk.Window(themename="cyborg")
root.title("Fights prediction")
root.config()
root.resizable(False, False)
root.geometry("800x750")
icon = PhotoImage(file="icon.png")
root.iconphoto(False, icon)
app = FighterComparison(root)

fighter_list = df_fighter['FIGHTER'].tolist()
# handle combo lists events
functions.combos_handler(app, fighter_list, model)

root.mainloop()
