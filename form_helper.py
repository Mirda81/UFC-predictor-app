import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
from PIL import ImageTk, Image
import pandas as pd
from img_scraper import download_pic
from keras.models import load_model
from predict import prediction
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class FighterComparison(tk.Tk):
    def __init__(self):
        super().__init__()
        self.df = pd.read_csv('df_skills.csv')
        self.fighters = self.df['FIGHTER'].tolist()
        self.title("Fighter Comparison")
        self.config(bg="black")
        self.resizable(False, False)
        self.geometry("800x700")

        self.create_fighter_frames()
        self.create_fighter_selectors()
        self.create_image_labels()
        self.model = load_model('model.h5')
        self.model.load_weights('my_model_weights.h5')  # to load
        self.middle_panel()
        self.create_val_labels()

    def create_fighter_frames(self):
        # frame for fighter 1
        label_border1 = ttk.Label(self, background="red", foreground="red")
        label_border1.place(x=18, y=48, width=292, height=404)

        label_f1 = ttk.Label(self, relief="groove", background="red", borderwidth=5, foreground="red")
        label_f1.place(x=20, y=50, width=288, height=400)

        # frame for fighter 2
        label_border2 = ttk.Label(self, background="blue", foreground="blue")
        label_border2.place(x=480, y=48, width=292, height=404)

        label_f2 = ttk.Label(self, relief="groove", background="blue", borderwidth=5, foreground="red")
        label_f2.place(x=482, y=50, width=288, height=400)

    def create_fighter_selectors(self):
        # create dropdown menu for selecting fighter 1
        #self.fighter1_label = ttk.Label(self, text="Fighter 1:", background="black", foreground="white")
        self.fighter1_combo = ttk.Combobox(self, values=self.fighters)
        #self.fighter1_label.place(x=20, y=20)
        self.fighter1_combo.place(x=100, y=10, width=130,height=20)
        self.fighter1_combo.bind("<KeyRelease>", self.filter_fighters)
        self.fighter1_combo.bind("<<ComboboxSelected>>", lambda event: self.show_fighter_image(self.fighter1_combo.get(), 1), add="+")
        self.fighter1_combo.bind("<<ComboboxSelected>>",
                            lambda event: self.fill_values(), add="+")
        # create dropdown menu for selecting fighter 2
        #self.fighter2_label = ttk.Label(self, text="Fighter 2:", background="black", foreground="white")
        self.fighter2_combo = ttk.Combobox(self, values=self.fighters)
        #self.fighter2_label.place(x=480, y=20)
        self.fighter2_combo.place(x=560, y=10, width=130,height=20)
        self.fighter2_combo.bind("<KeyRelease>", self.filter_fighters)
        self.fighter2_combo.bind("<<ComboboxSelected>>", lambda event: self.show_fighter_image(self.fighter2_combo.get(), 2), add="+")
        self.fighter2_combo.bind("<<ComboboxSelected>>",
                            lambda event: self.fill_values(), add="+")

    def filter_fighters(self, *args):
        """Function for filtering the list of fighters"""
        filter_text1 = self.fighter1_combo.get()
        filter_text2 = self.fighter2_combo.get()
        filtered_fighters1 = [fighter for fighter in self.fighters if filter_text1.lower() in fighter.lower()]
        filtered_fighters2 = [fighter for fighter in self.fighters if filter_text2.lower() in fighter.lower()]
        self.fighter1_combo.config(values=filtered_fighters1)
        self.fighter2_combo.config(values=filtered_fighters2)

    def create_image_labels(self):
        # create Label widget for displaying the image of fighter 1
        self.fighter1_image_label = ttk.Label(self, background="white",relief="ridge")
        self.fighter1_image_label.place(x=38, y=70, width=250, height=250)

        # create Label widget for displaying the image of fighter 2
        self.fighter2_image_label = ttk.Label(self, background="white",relief="ridge")
        self.fighter2_image_label.place(x=500, y=70, width=250, height=250)


    def show_fighter_image(self, fighter, number):
        try:
            download_pic(fighter)
            img = Image.open("f1.PPM")
        except:
            img = Image.open("2.png")
            inverted_image = Image.new("RGB", img.size, (255, 255, 255))
            inverted_image.paste(img, (0, 0), img)
            img = inverted_image
        img = img.resize((250, 250), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        if number ==1:
            self.fighter1_image_label.config(image=img)
            self.fighter1_image_label.image = img
        if number ==2:
            self.fighter2_image_label.config(image=img)
            self.fighter2_image_label.image = img

    def middle_panel(self):
        # středový panel
        self.label_cara = ttk.Label(self, text="", background="gray", foreground="black", relief="groove", borderwidth=5)
        self.label_cara.place(x=310, y=48, width=170, height=404)
        # panel popisků
        self.label_Middle = ttk.Label(self, text="", background="black", foreground="white", relief="raised")
        self.label_Middle.place(x=360, y=48, width=70, height=404)

        # udaje vek atd
        x_f1= 325
        x_f2= 440
        w = 30
        barva = "grey"
        self.label_Age = ttk.Label(self, text="  AGE", background="black", foreground="yellow",
                              font=("Helvetica", 12, "bold"))
        self.label_Age.place(x=365, y=60, width=60, height=25)

        self.value_Age1 = ttk.Label(self, text="", background=barva, foreground="yellow",
                              font=("Helvetica", 12, "bold"))
        self.value_Age1.place(x=x_f1, y=60, width=w, height=25)

        self.value_Age2 = ttk.Label(self, text=" ", background=barva, foreground="yellow",
                              font=("Helvetica", 12, "bold"))
        self.value_Age2.place(x=x_f2, y=60, width=w, height=25)
        # vyska
        self.label_Height = ttk.Label(self, text="Height", background="black", foreground="yellow",
                                 font=("Helvetica", 12, "bold"))
        self.label_Height.place(x=365, y=90, width=60, height=25)

        self.value_Height1 = ttk.Label(self, text="", background=barva, foreground="yellow",
                                 font=("Helvetica", 12, "bold"))
        self.value_Height1.place(x=x_f1-5, y=90, width=w+5, height=25)
        self.value_Height2 = ttk.Label(self, text="", background=barva, foreground="yellow",
                                 font=("Helvetica", 12, "bold"))
        self.value_Height2.place(x=x_f2-5, y=90, width=w+5, height=25)

        # vaha

        self.label_Weight = ttk.Label(self, text="Weight", background="black", foreground="yellow",
                                 font=("Helvetica", 12, "bold"))
        self.label_Weight.place(x=365, y=120, width=60, height=25)

        self.value_Weight1 = ttk.Label(self, text="", background=barva, foreground="yellow",
                                 font=("Helvetica", 12, "bold"))
        self.value_Weight1.place(x=x_f1-5, y=120, width=w+5, height=25)
        self.value_Weight2 = ttk.Label(self, text="", background=barva, foreground="yellow",
                                 font=("Helvetica", 12, "bold"))
        self.value_Weight2.place(x=x_f2-3, y=120, width=w+5, height=25)
        # dosah

        self.label_Reach = ttk.Label(self, text="Reach", background="black", foreground="yellow",
                                font=("Helvetica", 12, "bold"))
        self.label_Reach.place(x=365, y=150, width=60, height=25)

        self.value_Reach1 = ttk.Label(self, text="", background=barva, foreground="yellow",
                                font=("Helvetica", 12, "bold"))
        self.value_Reach1.place(x=x_f1-5, y=150, width=w+5, height=25)

        self.value_Reach2 = ttk.Label(self, text="", background=barva, foreground="yellow",
                                font=("Helvetica", 12, "bold"))
        self.value_Reach2.place(x=x_f2-5, y=150, width=w+5, height=25)

        # statistsiky wins
        self.label_win = ttk.Label(self, text="  Wins", background="black", foreground="#00FF00",
                              font=("Helvetica", 12, "bold"))
        self.label_win.place(x=365, y=190, width=60, height=25)

        self.label_win_f1 = ttk.Label(self, text="", background="gray", foreground="#00FF00",
                              font=("Helvetica", 12, "bold"))
        self.label_win_f1.place(x=x_f1+5, y=190, width=w, height=25)

        self.label_win_f2 = ttk.Label(self, text="", background="gray", foreground="#00FF00",
                              font=("Helvetica", 12, "bold"))
        self.label_win_f2.place(x=x_f2+5, y=190, width=w, height=25)

        # Ko/tko
        self.label_KOTKO = ttk.Label(self, text=" KO/TKO", background="black", foreground="#00FF00",
                                 font=("Helvetica", 10, "bold"))
        self.label_KOTKO.place(x=365, y=220, width=60, height=25)

        self.value_KOTKO1 = ttk.Label(self, text="", background=barva, foreground="#00FF00",
                                 font=("Helvetica", 11, "bold"))
        self.value_KOTKO1.place(x=x_f1+5, y=220, width=w, height=25)
        self.value_KOTKO2 = ttk.Label(self, text="", background=barva, foreground="#00FF00",
                                 font=("Helvetica", 11, "bold"))
        self.value_KOTKO2.place(x=x_f2+5, y=220, width=w, height=25)

        # dec
        self.label_Dec= ttk.Label(self, text="   DEC", background="black", foreground="#00FF00",
                                 font=("Helvetica", 10, "bold"))
        self.label_Dec.place(x=365, y=250, width=60, height=25)

        self.value_Dec1= ttk.Label(self, text="", background=barva, foreground="#00FF00",
                                 font=("Helvetica", 11, "bold"))
        self.value_Dec1.place(x=x_f1+5, y=250, width=w, height=25)
        self.value_Dec2= ttk.Label(self, text="", background=barva, foreground="#00FF00",
                                 font=("Helvetica", 11, "bold"))
        self.value_Dec2.place(x=x_f2+5, y=250, width=w, height=25)



        self.label_sub = ttk.Label(self, text="   SUB", background="black", foreground="#00FF00",
                                 font=("Helvetica", 10, "bold"))
        self.label_sub.place(x=365, y=280, width=60, height=25)

        self.value_sub1 = ttk.Label(self, text="", background=barva, foreground="#00FF00",
                                 font=("Helvetica", 11, "bold"))
        self.value_sub1.place(x=x_f1+5, y=280, width=w, height=25)

        self.value_sub2 = ttk.Label(self, text="", background=barva, foreground="#00FF00",
                                 font=("Helvetica", 11, "bold"))
        self.value_sub2.place(x=x_f2+5, y=280, width=w, height=25)
        # statistsiky losts
        self.label_Losts = ttk.Label(self, text="  Losts", background="black", foreground="red", font=("Helvetica", 12, "bold"))
        self.label_Losts.place(x=365, y=320, width=60, height=25)

        self.value_Losts1 = ttk.Label(self, text="", background=barva, foreground="red", font=("Helvetica", 10, "bold"))
        self.value_Losts1.place(x=x_f1+5, y=320, width=w, height=25)

        self.value_Losts2 = ttk.Label(self, text="", background=barva, foreground="red", font=("Helvetica", 10, "bold"))
        self.value_Losts2.place(x=x_f2+5, y=320, width=w, height=25)
        # KO/TOK
        self.label_KO_lost = ttk.Label(self, text=" KO/TKO", background="black", foreground="red",
                                 font=("Helvetica", 10, "bold"))
        self.label_KO_lost.place(x=365, y=350, width=60, height=25)

        self.value_KO_lost1 = ttk.Label(self, text="", background=barva, foreground="red",
                                 font=("Helvetica", 11, "bold"))
        self.value_KO_lost1.place(x=x_f1+5, y=350, width=w, height=25)
        self.value_KO_lost2 = ttk.Label(self, text="", background=barva, foreground="red",
                                 font=("Helvetica", 11, "bold"))
        self.value_KO_lost2.place(x=x_f2+5, y=350, width=w, height=25)
        # DEC
        self.label_Dec_lost = ttk.Label(self, text="   DEC", background="black", foreground="red",
                                 font=("Helvetica", 10, "bold"))
        self.label_Dec_lost.place(x=365, y=380, width=60, height=25)
        self.value_Dec_lost1 = ttk.Label(self, text="", background=barva, foreground="red",
                                 font=("Helvetica", 11, "bold"))
        self.value_Dec_lost1.place(x=x_f1+5, y=380, width=w, height=25)

        self.value_Dec_lost2 = ttk.Label(self, text="", background=barva, foreground="red",
                                 font=("Helvetica", 11, "bold"))
        self.value_Dec_lost2.place(x=x_f2+5, y=380, width=w, height=25)

        # sub
        self.label_sub_lost = ttk.Label(self, text="   SUB", background="black", foreground="red",
                                 font=("Helvetica", 10, "bold"))
        self.label_sub_lost.place(x=365, y=410, width=60, height=25)

        self.label_sub_lost1 = ttk.Label(self, text="", background=barva, foreground="red",
                                 font=("Helvetica", 11, "bold"))
        self.label_sub_lost1.place(x=x_f1+5, y=410, width=w, height=25)

        self.label_sub_lost2 = ttk.Label(self, text="", background=barva, foreground="red",
                                 font=("Helvetica", 11, "bold"))
        self.label_sub_lost2.place(x=x_f2+5, y=410, width=w, height=25)

    def create_val_labels(self):
        # proba
        self.label_pred_text1 = ttk.Label(self, text="Probability of win%: ", background="red", foreground="black",
                                 font=("Helvetica", 12, "bold"))
        self.label_pred_text1.place(x=30, y=330, width=160, height=25)

        self.label_pred_value1= ttk.Label(self, text="", background="red", foreground="black",
                                 font=("Helvetica", 12, "bold"))
        self.label_pred_value1.place(x=195, y=330, width=100, height=25)

        self.label_pred_text2 = ttk.Label(self, text="Probability of win%: ", background="blue", foreground="black",
                                     font=("Helvetica", 12, "bold"))
        self.label_pred_text2.place(x=500, y=330, width=160, height=25)

        self.label_pred_value2 = ttk.Label(self, text=": ", background="blue", foreground="black",
                                      font=("Helvetica", 12, "bold"))
        self.label_pred_value2.place(x=665, y=330, width=100, height=25)
        # odds
        self.label_odds_text1 = ttk.Label(self, text="Calculated odds: ", background="red", foreground="black",
                                 font=("Helvetica", 11, "bold"))
        self.label_odds_text1.place(x=30, y=360, width=110, height=25)

        self.label_odds_value1= ttk.Label(self, text="", background="red", foreground="black",
                                 font=("Helvetica", 11, "bold"))
        self.label_odds_value1.place(x=150, y=360, width=100, height=25)

        self.label_odds_text2 = ttk.Label(self, text="Calculated odds: ", background="blue", foreground="black",
                                 font=("Helvetica", 11, "bold"))
        self.label_odds_text2.place(x=500, y=360, width=110, height=25)

        self.label_odds_value2= ttk.Label(self, text="", background="blue", foreground="black",
                                 font=("Helvetica", 11, "bold"))
        self.label_odds_value2.place(x=620, y=360, width=100, height=25)

    def fill_values(self):
        self.fighter1 = self.fighter1_combo.get()
        self.fighter2 = self.fighter2_combo.get()
        if len(self.fighter1) > 3:
            self.df_f1 = self.df[self.df['FIGHTER'] == self.fighter1]

            self.value_Age1.config(text=int(self.df_f1['AGE']))
            self.value_Height1.config(text=round(float((self.df_f1['HEIGHT_fighter']*2.54))/100,2))
            self.value_Weight1.config(text=round(float(self.df_f1['WEIGHT_fighter']*0.4535),1))
            self.value_Reach1.config(text=round(float((self.df_f1['REACH_fighter']*2.54))/100,2))

            self.label_win_f1.config(text=int(self.df_f1['Win']))
            self.value_KOTKO1.config(text=int(self.df_f1['Win-striking']))
            self.value_Dec1.config(text=int(self.df_f1['Win_Decision']))
            self.value_sub1.config(text=int(self.df_f1['Win-ground']))

            self.value_Losts1.config(text=int(self.df_f1['Lost']))
            self.value_KO_lost1.config(text=int(self.df_f1['Lost-striking']))
            self.value_Dec_lost1.config(text=int(self.df_f1['Lost_Decision']))
            self.label_sub_lost1.config(text=int(self.df_f1['Lost-ground']))

            self.fights_f1 = self.df_f1['Fights']
        if len(self.fighter2) > 3:
            self.df_f2 = self.df[self.df['FIGHTER'] == self.fighter2]

            self.value_Age2.config(text=int(self.df_f2['AGE']))
            self.value_Height2.config(text=round(float((self.df_f2['HEIGHT_fighter']*2.54))/100,2))
            self.value_Weight2.config(text=round(float(self.df_f2['WEIGHT_fighter']*0.4535),1))
            self.value_Reach2.config(text=round(float((self.df_f2['REACH_fighter'] * 2.54)/100), 2))

            self.value_Dec2.config(text=int(self.df_f2['Win_Decision']))
            self.label_win_f2.config(text=int(self.df_f2['Win']))
            self.value_KOTKO2.config(text=int(self.df_f2['Win-striking']))
            self.value_sub2.config(text=int(self.df_f2['Win-ground']))

            self.value_Losts2.config(text=int(self.df_f2['Lost']))
            self.value_KO_lost2.config(text=int(self.df_f2['Lost-striking']))
            self.value_Dec_lost2.config(text=int(self.df_f2['Lost_Decision']))
            self.label_sub_lost2.config(text=int(self.df_f2['Lost-ground']))

            self.fights_f2 = self.df_f2['Fights']

        if len(self.fighter1) * len(self.fighter2) !=0:
            print(len(self.fighter1) , len(self.fighter1))
            pred1,pred2 = prediction(self.fighter1,self.fighter2, self.model)
            if pred1 > pred2:
                self.label_pred_value2.config(foreground="black")
                self.label_pred_value1.config(foreground="#00FF00")
            if pred2 > pred1:
                self.label_pred_value1.config(foreground="black")
                self.label_pred_value2.config(foreground="#00FF00")
            self.label_pred_value1.config(text=str(pred1))
            self.label_pred_value2.config(text=str(pred2))
            self.label_odds_value1.config(text=str(round(1/(pred1/100),2)))
            self.label_odds_value2.config(text=str(round(1 / (pred2/100), 2)))
            self.probability_chart(pred1,pred2)
            print(np.min([int(self.fights_f1),int(self.fights_f2)]))
    def probability_chart(self, probability1, probability2):
        data = [60, 40]
        colors = ['red', 'blue']
        fig, ax = plt.subplots(figsize=(4, 4), subplot_kw={'aspect': 'equal'},facecolor="black")
        ax.pie(x=(probability1, probability2), colors=["red", "blue"], autopct='%.00f%%',
               startangle=90,
               wedgeprops={'linewidth': 2, 'edgecolor': 'k'}, labeldistance=1.1,
               textprops={'fontsize': 10, 'weight': 'bold'})
        ax.add_artist(plt.Circle((0, 0), 0.35, fc='white', ec='black', lw=2))
        ax.annotate("% to win", xy=(0, 0), va="center", ha="center")
        plt.tight_layout(pad=0.5, w_pad=0.5, h_pad=0.5)
        ax.set_facecolor('black')

        # vložení grafu do formuláře
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().place(x=0, y=455, width=270, height=270)
        canvas.draw()


