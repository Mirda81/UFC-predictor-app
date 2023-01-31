from tkinter import ttk
from tkinter import *
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
from process_helper import odds
from math import pi
from matplotlib import rcParams
from tkinter import messagebox


class FighterComparison(Frame):

    def __init__(self,master):
        super().__init__(master)
        self.master = master
        self.df = pd.read_csv('Preprocessing/df_skills.csv')
        self.df_odds = pd.read_csv('process_helper/df_odds.csv')
        self.red_corner_clr = "#BF1A2F"
        self.blue_corner_clr = "#22577A"
        self.create_fighter_frames()
        self.create_fighter_selectors()
        self.create_image_labels()
        self.model = load_model('model/model.h5')
        self.model.load_weights('model/my_model_weights.h5')  # to load
        self.middle_panel()
        self.create_val_labels()
        self.create_menu()

    def create_fighter_frames(self):
        # frame for fighter 1
        label_border1 = ttk.Label(self.master,relief="groove", background= self.red_corner_clr, foreground="red")
        label_border1.place(x=18, y=38, width=292, height=414)

        label_f1 = ttk.Label(self.master, relief="raised", background=self.red_corner_clr, borderwidth=5, foreground="red")
        label_f1.place(x=20, y=40, width=288, height=410)

        # frame for fighter 2
        label_border2 = ttk.Label(self.master,relief="groove", background=self.blue_corner_clr, foreground="blue")
        label_border2.place(x=480, y=38, width=292, height=414)

        label_f2 = ttk.Label(self.master, relief="raised", background=self.blue_corner_clr, borderwidth=5, foreground="red")
        label_f2.place(x=482, y=40, width=288, height=410)
        # frame dole
        label_dole = ttk.Label(self.master, background="white",relief="sunken", borderwidth=2, foreground="red")
        label_dole.place(x=0, y=452, width=800, height=395)
        # label decision
        self.label_decision_text = ttk.Label(self.master, text="Decision: ", background="black", foreground="yellow",
                                 font=("Helvetica", 12, "bold"))
        self.label_decision_text.place(x=18, y=10, width=75, height=20)
        self.label_decision = ttk.Label(self.master, text="", background="black", foreground="yellow",
                                 font=("Helvetica", 12, "bold"))
        self.label_decision.place(x=100, y=10, width=200, height=20)

        # label confidence level
        self.label_confidence_text = ttk.Label(self.master, text="Confidence level: ", background="black", foreground="yellow",
                                 font=("Helvetica", 12, "bold"))
        self.label_confidence_text.place(x=310, y=10, width=135, height=20)
        self.label_confidence = ttk.Label(self.master, text="", background="black", foreground="yellow",
                                 font=("Helvetica", 12, "bold"))
        self.label_confidence.place(x=460, y=10, width=70, height=20)

        # label confidence reason
        self.label_reason = ttk.Label(self.master, text="", background="black", foreground="yellow",
                                 font=("Helvetica", 12, "bold"))
        self.label_reason.place(x=550, y=10, width=230, height=20)


    def create_menu(self):
        self.menu = Menu(self.master, tearoff=0)
        self.master.config(menu=self.menu)
        self.menu.config(font=("calibri", 12, "bold"))
        self.menu.config(bd=3, relief=RAISED)
        self.menu.config(bg='black', fg='white')
        options_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Menu", menu=options_menu)
        options = ["Update data", "Update odds", "Exit"]
        for option in options:
            options_menu.add_command(label=option, command=lambda val=option: self.menu_select(val))

    def menu_select(self, value):
        if value == "Exit":
            self.master.destroy()
        if value == "Update odds":
            odds.download_odds()
            self.df_odds = pd.read_csv('df_odds.csv')
            self.fill_values(1)
            self.fill_values(2)
            messagebox.showinfo("Update completed", "Odds update has been completed.")
    def create_fighter_selectors(self):
        # create dropdown menu for selecting fighter 1
        self.fighter1_combo = ttk.Combobox(self.master, background="red")
        self.fighter1_combo.place(x=100, y=45, width=130,height=20)


        self.fighter1_combo.bind("<<ComboboxSelected>>",
                            lambda event: self.fill_values(1), add="+")

        # create dropdown menu for selecting fighter 2
        self.fighter2_combo = ttk.Combobox(self.master,background="blue")
        self.fighter2_combo.place(x=560, y=45, width=130,height=20)

        self.fighter2_combo.bind("<<ComboboxSelected>>",
                            lambda event: self.fill_values(2), add="+")

    def create_image_labels(self):
        # create Label widget for displaying the image of fighter 1
        self.fighter1_image_label = ttk.Label(self.master, background="white",relief="sunken")
        self.fighter1_image_label.place(x=38, y=70, width=250, height=250)

        # create Label widget for displaying the image of fighter 2
        self.fighter2_image_label = ttk.Label(self.master, background="white",relief="sunken")
        self.fighter2_image_label.place(x=500, y=70, width=250, height=250)


    def show_fighter_image(self, target, fighter):
        img = download_pic(fighter)
        target.config(image=img)
        target.image = img

    def middle_panel(self):
        # středový panel
        self.label_cara = ttk.Label(self.master, text="", background="gray", foreground="black", relief="groove", borderwidth=5)
        self.label_cara.place(x=310, y=38, width=170, height=414)
        # panel popisků
        self.label_Middle = ttk.Label(self.master, text="", background="black", foreground="white", relief="raised")
        self.label_Middle.place(x=360, y=38, width=70, height=414)

        # udaje vek atd
        x_f1= 325
        x_f2= 440
        w = 30
        barva = "grey"
        self.label_Age = ttk.Label(self.master, text="  Age", background="black", foreground="yellow",
                              font=("Helvetica", 12, "bold"))
        self.label_Age.place(x=365, y=60, width=60, height=25)

        self.value_Age1 = ttk.Label(self.master, text="", background=barva, foreground="yellow",
                              font=("Helvetica", 12, "bold"))
        self.value_Age1.place(x=x_f1, y=60, width=w, height=25)

        self.value_Age2 = ttk.Label(self.master, text=" ", background=barva, foreground="yellow",
                              font=("Helvetica", 12, "bold"))
        self.value_Age2.place(x=x_f2, y=60, width=w, height=25)
        # vyska
        self.label_Height = ttk.Label(self.master, text="Height", background="black", foreground="yellow",
                                 font=("Helvetica", 12, "bold"))
        self.label_Height.place(x=365, y=90, width=60, height=25)

        self.value_Height1 = ttk.Label(self.master, text="", background=barva, foreground="yellow",
                                 font=("Helvetica", 12, "bold"))
        self.value_Height1.place(x=x_f1-5, y=90, width=w+5, height=25)
        self.value_Height2 = ttk.Label(self.master, text="", background=barva, foreground="yellow",
                                 font=("Helvetica", 12, "bold"))
        self.value_Height2.place(x=x_f2-5, y=90, width=w+5, height=25)

        # vaha

        self.label_Weight = ttk.Label(self.master, text="Weight", background="black", foreground="yellow",
                                 font=("Helvetica", 12, "bold"))
        self.label_Weight.place(x=365, y=120, width=60, height=25)

        self.value_Weight1 = ttk.Label(self.master, text="", background=barva, foreground="yellow",
                                 font=("Helvetica", 12, "bold"))
        self.value_Weight1.place(x=x_f1-5, y=120, width=w+5, height=25)
        self.value_Weight2 = ttk.Label(self.master, text="", background=barva, foreground="yellow",
                                 font=("Helvetica", 12, "bold"))
        self.value_Weight2.place(x=x_f2-3, y=120, width=w+5, height=25)
        # dosah

        self.label_Reach = ttk.Label(self.master, text="Reach", background="black", foreground="yellow",
                                font=("Helvetica", 12, "bold"))
        self.label_Reach.place(x=365, y=150, width=60, height=25)

        self.value_Reach1 = ttk.Label(self.master, text="", background=barva, foreground="yellow",
                                font=("Helvetica", 12, "bold"))
        self.value_Reach1.place(x=x_f1-5, y=150, width=w+5, height=25)

        self.value_Reach2 = ttk.Label(self.master, text="", background=barva, foreground="yellow",
                                font=("Helvetica", 12, "bold"))
        self.value_Reach2.place(x=x_f2-5, y=150, width=w+5, height=25)

        # statistsiky wins
        self.label_win = ttk.Label(self.master, text="  Wins", background="black", foreground="#00FF00",
                              font=("Helvetica", 12, "bold"))
        self.label_win.place(x=365, y=190, width=60, height=25)

        self.label_win_f1 = ttk.Label(self.master, text="", background="gray", foreground="#00FF00",
                              font=("Helvetica", 12, "bold"))
        self.label_win_f1.place(x=x_f1+5, y=190, width=w, height=25)

        self.label_win_f2 = ttk.Label(self.master, text="", background="gray", foreground="#00FF00",
                              font=("Helvetica", 12, "bold"))
        self.label_win_f2.place(x=x_f2+5, y=190, width=w, height=25)

        # Ko/tko
        self.label_KOTKO = ttk.Label(self.master, text=" KO/TKO", background="black", foreground="#00FF00",
                                 font=("Helvetica", 10, "bold"))
        self.label_KOTKO.place(x=365, y=220, width=60, height=25)

        self.value_KOTKO1 = ttk.Label(self.master, text="", background=barva, foreground="#00FF00",
                                 font=("Helvetica", 11, "bold"))
        self.value_KOTKO1.place(x=x_f1+5, y=220, width=w, height=25)
        self.value_KOTKO2 = ttk.Label(self.master, text="", background=barva, foreground="#00FF00",
                                 font=("Helvetica", 11, "bold"))
        self.value_KOTKO2.place(x=x_f2+5, y=220, width=w, height=25)

        # dec
        self.label_Dec= ttk.Label(self.master, text="   DEC", background="black", foreground="#00FF00",
                                 font=("Helvetica", 10, "bold"))
        self.label_Dec.place(x=365, y=250, width=60, height=25)

        self.value_Dec1= ttk.Label(self.master, text="", background=barva, foreground="#00FF00",
                                 font=("Helvetica", 11, "bold"))
        self.value_Dec1.place(x=x_f1+5, y=250, width=w, height=25)
        self.value_Dec2= ttk.Label(self.master, text="", background=barva, foreground="#00FF00",
                                 font=("Helvetica", 11, "bold"))
        self.value_Dec2.place(x=x_f2+5, y=250, width=w, height=25)



        self.label_sub = ttk.Label(self.master, text="   SUB", background="black", foreground="#00FF00",
                                 font=("Helvetica", 10, "bold"))
        self.label_sub.place(x=365, y=280, width=60, height=25)

        self.value_sub1 = ttk.Label(self.master, text="", background=barva, foreground="#00FF00",
                                 font=("Helvetica", 11, "bold"))
        self.value_sub1.place(x=x_f1+5, y=280, width=w, height=25)

        self.value_sub2 = ttk.Label(self.master, text="", background=barva, foreground="#00FF00",
                                 font=("Helvetica", 11, "bold"))
        self.value_sub2.place(x=x_f2+5, y=280, width=w, height=25)
        # statistsiky losts
        self.label_Losts = ttk.Label(self.master, text="  Losts", background="black", foreground="red", font=("Helvetica", 12, "bold"))
        self.label_Losts.place(x=365, y=320, width=60, height=25)

        self.value_Losts1 = ttk.Label(self.master, text="", background=barva, foreground="red", font=("Helvetica", 10, "bold"))
        self.value_Losts1.place(x=x_f1+5, y=320, width=w, height=25)

        self.value_Losts2 = ttk.Label(self.master, text="", background=barva, foreground="red", font=("Helvetica", 10, "bold"))
        self.value_Losts2.place(x=x_f2+5, y=320, width=w, height=25)
        # KO/TOK
        self.label_KO_lost = ttk.Label(self.master, text=" KO/TKO", background="black", foreground="red",
                                 font=("Helvetica", 10, "bold"))
        self.label_KO_lost.place(x=365, y=350, width=60, height=25)

        self.value_KO_lost1 = ttk.Label(self.master, text="", background=barva, foreground="red",
                                 font=("Helvetica", 11, "bold"))
        self.value_KO_lost1.place(x=x_f1+5, y=350, width=w, height=25)
        self.value_KO_lost2 = ttk.Label(self.master, text="", background=barva, foreground="red",
                                 font=("Helvetica", 11, "bold"))
        self.value_KO_lost2.place(x=x_f2+5, y=350, width=w, height=25)
        # DEC
        self.label_Dec_lost = ttk.Label(self.master, text="   DEC", background="black", foreground="red",
                                 font=("Helvetica", 10, "bold"))
        self.label_Dec_lost.place(x=365, y=380, width=60, height=25)
        self.value_Dec_lost1 = ttk.Label(self.master, text="", background=barva, foreground="red",
                                 font=("Helvetica", 11, "bold"))
        self.value_Dec_lost1.place(x=x_f1+5, y=380, width=w, height=25)

        self.value_Dec_lost2 = ttk.Label(self.master, text="", background=barva, foreground="red",
                                 font=("Helvetica", 11, "bold"))
        self.value_Dec_lost2.place(x=x_f2+5, y=380, width=w, height=25)

        # sub
        self.label_sub_lost = ttk.Label(self.master, text="   SUB", background="black", foreground="red",
                                 font=("Helvetica", 10, "bold"))
        self.label_sub_lost.place(x=365, y=410, width=60, height=25)

        self.label_sub_lost1 = ttk.Label(self.master, text="", background=barva, foreground="red",
                                 font=("Helvetica", 11, "bold"))
        self.label_sub_lost1.place(x=x_f1+5, y=410, width=w, height=25)

        self.label_sub_lost2 = ttk.Label(self.master, text="", background=barva, foreground="red",
                                 font=("Helvetica", 11, "bold"))
        self.label_sub_lost2.place(x=x_f2+5, y=410, width=w, height=25)

    def create_val_labels(self):
        # proba
        self.label_pred_text1 = ttk.Label(self.master, text="Probability of win: ", background= self.red_corner_clr, foreground="black",
                                 font=("Helvetica", 12, "bold"))
        self.label_pred_text1.place(x=30, y=330, width=160, height=25)

        self.label_pred_value1= ttk.Label(self.master, text="", background = self.red_corner_clr, foreground="black",
                                 font=("Helvetica", 12, "bold"))
        self.label_pred_value1.place(x=185, y=330, width=100, height=25)

        self.label_pred_text2 = ttk.Label(self.master, text="Probability of win: ", background=self.blue_corner_clr, foreground="black",
                                     font=("Helvetica", 12, "bold"))
        self.label_pred_text2.place(x=500, y=330, width=160, height=25)

        self.label_pred_value2 = ttk.Label(self.master, text="", background=self.blue_corner_clr, foreground="black",
                                      font=("Helvetica", 12, "bold"))

        self.label_pred_value2.place(x=660, y=330, width=100, height=25)
        # f1 odds
        # calculated
        self.label_odds_text1 = ttk.Label(self.master, text="Calculated odds: ", background=self.red_corner_clr, foreground="black",
                                 font=("Helvetica", 12, "bold"))
        self.label_odds_text1.place(x=30, y=360, width=140, height=25)

        self.label_odds_value1= ttk.Label(self.master, text="", background=self.red_corner_clr, foreground="black",
                                 font=("Helvetica", 12, "bold"))
        self.label_odds_value1.place(x=185, y=360, width=100, height=25)
        # bookmaker ods
        self.label_odds_b_text1 = ttk.Label(self.master, text="Bookmakers odds: ", background=self.red_corner_clr, foreground="black",
                                 font=("Helvetica", 12, "bold"))
        self.label_odds_b_text1.place(x=30, y=390, width=150, height=25)

        self.label_odds_b_value1= ttk.Label(self.master, text="", background=self.red_corner_clr, foreground="black",
                                 font=("Helvetica", 12, "bold"))
        self.label_odds_b_value1.place(x=185, y=390, width=100, height=25)
        # best bookmaker
        self.label_best_b_text1 = ttk.Label(self.master, text="Best bookmaker: ", background=self.red_corner_clr, foreground="black",
                                 font=("Helvetica", 12, "bold"))
        self.label_best_b_text1.place(x=30, y=420, width=150, height=25)

        self.label_best_b_value1= ttk.Label(self.master, text="", background=self.red_corner_clr, foreground="black",
                                 font=("Helvetica", 10, "bold"))
        self.label_best_b_value1.place(x=185, y=420, width=100, height=25)
        # f2 odds
        # calculated
        self.label_odds_text2 = ttk.Label(self.master, text="Calculated odds: ", background=self.blue_corner_clr, foreground="black",
                                 font=("Helvetica", 12, "bold"))
        self.label_odds_text2.place(x=500, y=360, width=150, height=25)

        self.label_odds_value2= ttk.Label(self.master, text="",background= self.blue_corner_clr, foreground=self.blue_corner_clr,
                                 font=("Helvetica", 12, "bold"))
        self.label_odds_value2.place(x=660, y=360, width=100, height=25)
        # bookmakers odds
        self.label_odds_b_text2 = ttk.Label(self.master, text="Bookmakers odds: ", background=self.blue_corner_clr, foreground="black",
                                 font=("Helvetica", 12, "bold"))
        self.label_odds_b_text2.place(x=500, y=390, width=150, height=25)

        self.label_odds_b_value2= ttk.Label(self.master, text="", background=self.blue_corner_clr, foreground="black",
                                 font=("Helvetica", 12, "bold"))
        self.label_odds_b_value2.place(x=660, y=390, width=100, height=25)
        # best bookmaker
        self.label_best_b_text2 = ttk.Label(self.master, text="Best bookmaker: ", background=self.blue_corner_clr, foreground="black",
                                 font=("Helvetica", 12, "bold"))
        self.label_best_b_text2.place(x=500, y=420, width=150, height=25)

        self.label_best_b_value2= ttk.Label(self.master, text="", background=self.blue_corner_clr, foreground="black",
                                 font=("Helvetica", 10, "bold"))
        self.label_best_b_value2.place(x=660, y=420, width=100, height=25)

    def fill_values(self, num):
        self.fighter1 = self.fighter1_combo.get()
        self.fighter2 = self.fighter2_combo.get()
        if num ==1:
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
        if num ==2:
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
            self.pred1,self.pred2 = prediction(self.fighter1,self.fighter2, self.model)
            if self.pred1 > self.pred2:
                self.label_pred_value2.config(foreground="black")
                self.label_pred_value1.config(foreground="#00FF00")
            if self.pred2 > self.pred1:
                self.label_pred_value1.config(foreground="black")
                self.label_pred_value2.config(foreground="#00FF00")
            self.label_pred_value1.config(text=str(self.pred1) + ' %')
            self.label_pred_value2.config(text=str(self.pred2) +' %')
            self.label_odds_value1.config(text=str(round(1/(self.pred1/100),2)))
            self.label_odds_value2.config(text=str(round(1 / (self.pred2/100), 2)))
            self.odds_b = odds.get_odds(self.fighter1, self.fighter2, self.df_odds)

            if len(self.odds_b) !=0:
                self.label_odds_b_value1.config(text=str(str(self.odds_b['f1_min']) + " - " +  str(self.odds_b['f1_max'])))
                self.label_odds_b_value2.config(text=str(str(self.odds_b['f2_min']) + " - " +  str(self.odds_b['f2_max'])))
                self.label_best_b_value1.config(text=str(str(self.odds_b['bookmaker1'])))
                self.label_best_b_value2.config(text=str(str(self.odds_b['bookmaker2'])))
            else:
                self.label_odds_b_value1.config(text=str("NA"))
                self.label_odds_b_value2.config(text=str("NA"))
                self.label_best_b_value1.config(text="")
                self.label_best_b_value2.config(text="")

            self.probability_chart(self.pred1,self.pred2)
            self.skills_chart(self.fighter1,self.fighter2)
            self.make_decision()
    def probability_chart(self, probability1, probability2):
        fig, ax = plt.subplots(figsize=(4, 4), subplot_kw={'aspect': 'equal'},facecolor="white")
        ax.pie(x=(probability1, probability2), colors=["red", "blue"], autopct='%.00f%%',
               startangle=90,
               wedgeprops={'linewidth': 2, 'edgecolor': 'k'}, labeldistance=1.1,
               textprops={'fontsize': 10, 'weight': 'bold'})
        ax.add_artist(plt.Circle((0, 0), 0.35, fc='white', ec='black', lw=2))
        ax.annotate("% to win", xy=(0, 0), va="center", ha="center")
        plt.tight_layout(pad=0.5, w_pad=0.5, h_pad=0.5)
        ax.set_facecolor('black')

        # vložení grafu do formuláře
        canvas = FigureCanvasTkAgg(fig, master=self.master)
        canvas.get_tk_widget().place(x=40, y=455, width=320, height=270)
        canvas.draw()

    def skills_chart(self, fighter1, fighter2):
        # Define the categories and values
        rcParams['xtick.major.pad'] = '5'
        rcParams['ytick.major.pad'] = '5'
        categories = ['Ground defense', 'Ground attack', 'Striking defense', 'Striking attack', 'Stamina']
        values1 = self.df.loc[self.df['FIGHTER']==fighter1,["ground_def_skill","ground_att_skill", "stand_def_skill","stand_att_skill", "stamina"]].values.flatten().tolist()
        values2 = self.df.loc[
            self.df['FIGHTER'] == fighter2, ["ground_def_skill", "ground_att_skill", "stand_def_skill",
                                             "stand_att_skill", "stamina"]].values.flatten().tolist()
        # Create the figure
        fig = plt.figure()
        ax = fig.add_subplot(111, polar=True, facecolor='yellow')

        # Plot the data
        ax.plot(np.linspace(0, 2 * np.pi, len(categories), endpoint=False), values1, '-', linewidth=1, color='red')
        ax.plot(np.linspace(0, 2 * np.pi, len(categories), endpoint=False), values2, '-', linewidth=1, color='blue')
        ax.fill(np.linspace(0, 2 * np.pi, len(categories), endpoint=False), values1, alpha=0.5, color='red')
        ax.fill(np.linspace(0, 2 * np.pi, len(categories), endpoint=False), values2, alpha=0.5, color='blue')

        # Add labels
        ax.set_thetagrids(np.linspace(0, 360, len(categories), endpoint=False), categories, color='black')
        ax.grid(color='black')
        ax.set_theta_offset(-pi / 16)
        plt.ylim(0, 100)
        for spine in ax.spines.values():
            spine.set_edgecolor('black')
        ax.set_rlabel_position(45)
        # Show the plot
        canvas_skill = FigureCanvasTkAgg(fig, master=self.master)
        canvas_skill.get_tk_widget().place(x=420, y=455, width=320, height=270)
        canvas_skill.draw()
    def get_confidence(self):
        f1_fights = int(self.df_f1['Fights'])
        f2_fights = int(self.df_f2['Fights'])

        f1_weight = float(self.df_f1['WEIGHT_fighter']*0.4535)
        f2_weight = float(self.df_f2['WEIGHT_fighter']*0.4535)

        if abs(f1_weight-f2_weight) > 10:

            return("Low","Different weight division")


        if np.minimum(f1_fights,f2_fights)>=7:
            return ("High","")
        elif np.minimum(f1_fights,f2_fights)>=3:
            return("Medium","")
        else:
            return("Low","Not enough data")

    def make_decision(self):
        confidence = self.get_confidence()
        if confidence[0]=="Low":
            if len(self.odds_b)==0:
                self.label_decision.config(text="No odds found",foreground="red")
            else:
                self.label_decision.config(text="NO BET!",foreground="red")

            self.label_confidence.config(text=confidence[0],foreground="red")
            self.label_reason.config(text=confidence[1],foreground="red")
            return

        if len(self.odds_b)==0:
            self.label_decision.config(text="No odds found",foreground="red")


        else:
            if 1/(self.pred1/100) < self.odds_b["f1_max"]:
                self.label_decision.config(text=str(self.fighter1), foreground="#00FF00")
            elif 1/(self.pred2/100) < self.odds_b["f2_max"]:
                self.label_decision.config(text=str(self.fighter2), foreground="#00FF00")
            else:
                self.label_decision.config(text="NO BET!", foreground="red")

        barva= "orange" if confidence[0]=="Medium" else "#00FF00"
        self.label_confidence.config(text=confidence[0],foreground=barva)
        self.label_reason.config(text=confidence[1],foreground=barva)