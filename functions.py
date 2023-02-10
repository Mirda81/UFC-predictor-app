from PIL import ImageTk, Image
from img_scraper import download_pic
from Fighter_class import Fighter
from keras.models import load_model
from predict import prediction
import pandas as pd
from process_helper import odds
import ttkbootstrap as tk
import numpy as np
from matplotlib import rcParams
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from math import pi


def filter_names(fighter_list, text):
    filtered_fighters1 = [fighter for fighter in fighter_list if text.lower() in fighter.lower()]
    return filtered_fighters1


def show_fighter_image(target, fighter):
    img = download_pic(fighter)
    target.config(image=img)
    target.image = img


def combos_handler(app, fighter_list, model):
    global Model_pred
    Model_pred = model
    app.fighter2_combo.config(values=fighter_list)
    app.fighter1_combo.config(values=fighter_list)

    app.fighter1_combo.bind("<KeyRelease>",
                            lambda event: app.fighter1_combo.config(
                                values=filter_names(fighter_list, app.fighter1_combo.get())))

    app.fighter1_combo.bind("<<ComboboxSelected>>", lambda event: Combo1_selected(app), add="+")

    app.fighter2_combo.bind("<KeyRelease>",
                            lambda event: app.fighter2_combo.config(
                                values=filter_names(fighter_list, app.fighter2_combo.get())))
    app.fighter2_combo.bind("<<ComboboxSelected>>", lambda event: Combo2_selected(app), add="+")


def check_combos_selected(c1, c2):
    return len(c1.get()) * len(c2.get()) != 0


def fill_informations(app, fighter, fighterNo):
    if fighterNo == 1:
        app.value_Age1.config(text=fighter.Age)
        app.value_Height1.config(text=fighter.Height)
        app.value_Weight1.config(text=fighter.Weight)
        app.value_Reach1.config(text=fighter.Reach)

        app.label_win_f1.config(text=fighter.Wins)
        app.value_KOTKO1.config(text=fighter.Win_striking)
        app.value_Dec1.config(text=fighter.Wins_Decision)
        app.value_sub1.config(text=fighter.Wins_ground)

        app.value_Losts1.config(text=fighter.Losts)
        app.value_KO_lost1.config(text=fighter.Lost_striking)
        app.value_Dec_lost1.config(text=fighter.Lost_Decision)
        app.label_sub_lost1.config(text=fighter.Lost_ground)
    if fighterNo == 2:
        app.value_Age2.config(text=fighter.Age)
        app.value_Height2.config(text=fighter.Height)
        app.value_Weight2.config(text=fighter.Weight)
        app.value_Reach2.config(text=fighter.Reach)

        app.label_win_f2.config(text=fighter.Wins)
        app.value_KOTKO2.config(text=fighter.Win_striking)
        app.value_Dec2.config(text=fighter.Wins_Decision)
        app.value_sub2.config(text=fighter.Wins_ground)

        app.value_Losts2.config(text=fighter.Losts)
        app.value_KO_lost2.config(text=fighter.Lost_striking)
        app.value_Dec_lost2.config(text=fighter.Lost_Decision)
        app.label_sub_lost2.config(text=fighter.Lost_ground)


def Combo1_selected(app):
    global Fighter1
    Fighter1 = Fighter(app.fighter1_combo.get())
    show_fighter_image(app.fighter1_image_label,
                       Fighter1.name)
    fill_informations(app, Fighter1, 1)
    app.update()
    if check_combos_selected(app.fighter1_combo, app.fighter2_combo):
        get_proba(app, app.fighter1_combo.get(), app.fighter2_combo.get())


def Combo2_selected(app):
    global Fighter2
    Fighter2 = Fighter(app.fighter2_combo.get())
    show_fighter_image(app.fighter2_image_label,
                       Fighter2.name)
    fill_informations(app, Fighter2, 2)
    app.update()
    if check_combos_selected(app.fighter1_combo, app.fighter2_combo):
        get_proba(app, app.fighter1_combo.get(), app.fighter2_combo.get())

def reset_values(app):
    make_decision(app, {}, 0, 0)
    probability_chart(app, 0, 0)
    app.label_odds_value1.config(text=str(0))
    app.label_odds_value2.config(text=str(0))
    app.label_odds_b_value1.config(text=str("NA"))
    app.label_odds_b_value2.config(text=str("NA"))
    app.label_best_b_value1.config(text="")
    app.label_best_b_value2.config(text="")
    app.value_value1.config(text="")
    app.value_value2.config(text="")
def get_proba(app, fighter1, fighter2):
    if get_confidence()[1] == "Different weight division":
        reset_values(app)
        return
    df_odds = pd.read_csv('process_helper/df_odds.csv')
    skills_chart(app)
    pred1, pred2 = prediction(fighter1, fighter2, Model_pred)

    probability_chart(app, pred1, pred2)
    odds_b = odds.get_odds(fighter1, fighter2, df_odds)

    app.label_odds_value1.config(text=str(round(1 / (pred1 / 100), 2)))
    app.label_odds_value2.config(text=str(round(1 / (pred2 / 100), 2)))

    if len(odds_b) != 0:
        app.label_odds_b_value1.config(text=str(str(odds_b['f1_min']) + " - " + str(odds_b['f1_max'])))
        app.label_odds_b_value2.config(text=str(str(odds_b['f2_min']) + " - " + str(odds_b['f2_max'])))
        app.label_best_b_value1.config(text=str(str(odds_b['bookmaker1'])))
        app.label_best_b_value2.config(text=str(str(odds_b['bookmaker2'])))

        value1 = round(pred1 / 100 * odds_b['f1_max'] - 1, 2)
        value2 = round(pred2 / 100 * odds_b['f2_max'] - 1, 2)

        app.value_value1.config(text=value1)
        app.value_value2.config(text=value2)

        app.value_value1.config(foreground="red") if value1 <= 0 else app.value_value1.config(foreground="#00FF00")
        app.value_value2.config(foreground="red") if value2 <= 0 else app.value_value2.config(foreground="#00FF00")
    else:
        app.label_odds_b_value1.config(text=str("NA"))
        app.label_odds_b_value2.config(text=str("NA"))
        app.label_best_b_value1.config(text="")
        app.label_best_b_value2.config(text="")
        app.value_value1.config(text="")
        app.value_value2.config(text="")

    make_decision(app, odds_b, pred1, pred2)


def probability_chart(app, probability1, probability2):
    meter1 = tk.Meter(
        metersize=175,
        padding=5,
        amountused=0,
        metertype="full",
        subtext="% to win",
        interactive=False, bootstyle='success',
        meterthickness=15, stripethickness=5,
    )
    meter1.place(x=30, y=500)

    meter2 = tk.Meter(
        metersize=175,
        padding=5,
        amountused=0,
        metertype="full",
        subtext="% to win",
        interactive=False, bootstyle='success',
        meterthickness=15, stripethickness=5,
    )
    meter2.place(x=595, y=500)
    progres = 0
    while progres < 15:
        meter1.configure(amountused=round(progres * probability1 / 15, 2))
        meter2.configure(amountused=round(progres * probability2 / 15, 2))
        progres += 2
        app.update()
    meter1.configure(amountused=round(probability1, 2))
    meter2.configure(amountused=round(probability2, 2))
    app.update()


def make_decision(app, odds, pred1, pred2):
    confidence = get_confidence()
    if confidence[1] == "Different weight division":
        app.label_decision.config(text="", foreground="red")
        app.label_confidence.config(text="NA", foreground="red")
        app.label_reason.config(text=confidence[1], foreground="red")
        return
    if confidence[0] == "Low":
        if len(odds) == 0:
            app.label_decision.config(text="No odds found", foreground="red")
        else:
            app.label_decision.config(text="No value bet", foreground="red")

        app.label_confidence.config(text=confidence[0], foreground="red")
        return

    if len(odds) == 0:
        app.label_decision.config(text="No odds found", foreground="red")

    else:
        if 1 / (pred1 / 100) < odds["f1_max"]:
            app.label_decision.config(text=str(Fighter1.name), foreground="#00FF00")
        elif 1 / (pred2 / 100) < odds["f2_max"]:
            app.label_decision.config(text=str(Fighter2.name), foreground="#00FF00")
        else:
            app.label_decision.config(text="No value bet", foreground="red")

    barva = "orange" if confidence[0] == "Medium" else "#00FF00"
    app.label_confidence.config(text=confidence[0], foreground=barva)
    app.label_reason.config(text=confidence[1], foreground=barva)


def get_confidence():
    f1_fights = Fighter1.Fights
    f2_fights = int(Fighter2.Fights)

    f1_weight = Fighter1.Weight
    f2_weight = Fighter2.Weight

    if abs(f1_weight - f2_weight) > 10:

        return "Low", "Different weight division"

    else:

        if np.minimum(f1_fights, f2_fights) >= 7:
            return "High", ""
        elif np.minimum(f1_fights, f2_fights) >= 3:
            return "Medium", ""
        else:
            return "Low", "Lack of data"


def skills_chart(app):
    # Define the categories and values
    rcParams['xtick.major.pad'] = '5'
    rcParams['ytick.major.pad'] = '5'
    categories = ['Ground defense', 'Ground attack', 'Striking defense', 'Striking attack', 'Stamina']
    values1 = Fighter1.Skills_set
    values2 = Fighter2.Skills_set

    # Create the figure
    fig = plt.figure(facecolor='black')
    ax = fig.add_subplot(111, polar=True, facecolor='yellow')

    # Plot the data
    ax.plot(np.linspace(0, 2 * np.pi, len(categories), endpoint=False), values1, '-', linewidth=1, color='red')
    ax.plot(np.linspace(0, 2 * np.pi, len(categories), endpoint=False), values2, '-', linewidth=1, color='blue')
    ax.fill(np.linspace(0, 2 * np.pi, len(categories), endpoint=False), values1, alpha=0.3, color='red')
    ax.fill(np.linspace(0, 2 * np.pi, len(categories), endpoint=False), values2, alpha=0.3, color='blue')

    # Add labels
    ax.set_thetagrids(np.linspace(0, 360, len(categories), endpoint=False), categories, color='red')
    ax.grid(color='black')
    ax.set_theta_offset(-pi / 16)
    plt.ylim(0, 100)
    for spine in ax.spines.values():
        spine.set_edgecolor('red')
    ax.set_rlabel_position(45)
    # Show the plot
    canvas_skill = FigureCanvasTkAgg(fig, master=app.master)
    canvas_skill.get_tk_widget().place(x=210, y=455, width=370, height=270)
    canvas_skill.draw()
