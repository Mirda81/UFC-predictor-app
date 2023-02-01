from PIL import ImageTk, Image
from img_scraper import download_pic
from Fighter_class import Fighter

def filter_names(fighter_list, text):
    filtered_fighters1 = [fighter for fighter in fighter_list if text.lower() in fighter.lower()]
    return filtered_fighters1

def show_fighter_image(target, fighter):
    img = download_pic(fighter)
    target.config(image=img)
    target.image = img

def combos_handler(app,fighter_list):
    app.fighter2_combo.config(values=fighter_list)
    app.fighter1_combo.config(values=fighter_list)

    app.fighter1_combo.bind("<KeyRelease>",
                            lambda event: app.fighter1_combo.config(
                                values=filter_names(fighter_list, app.fighter1_combo.get())))

    app.fighter1_combo.bind("<<ComboboxSelected>>", lambda event: Combo1_selected(app), add="+")

    app.fighter2_combo.bind("<KeyRelease>",
                            lambda event: app.fighter2_combo.config(
                                values=filter_names(fighter_list, app.fighter2_combo.get())))
    app.fighter2_combo.bind("<<ComboboxSelected>>", lambda event: Combo2_selected(app),add="+")

def fill_informations(app, fighter, fighterNo):
    if fighterNo ==1:
        app.value_Age1.config(text=fighter.Age)
        app.value_Height1.config(text =fighter.Height)
        app.value_Weight1.config(text =fighter.Weight )
        app.value_Reach1.config(text =fighter.Reach)

        app.label_win_f1.config(text =fighter.Wins)
        app.value_KOTKO1.config(text = fighter.Win_striking)
        app.value_Dec1.config(text = fighter.Wins_Decision)
        app.value_sub1.config(text = fighter.Wins_ground)

        app.value_Losts1.config(text = fighter.Losts)
        app.value_KO_lost1.config(text =fighter.Lost_striking)
        app.value_Dec_lost1.config(text =fighter.Lost_Decision)
        app.label_sub_lost1.config(text = fighter.Lost_ground)
    if fighterNo ==2:
        app.value_Age2.config(text=fighter.Age)
        app.value_Height2.config(text =fighter.Height)
        app.value_Weight2.config(text =fighter.Weight )
        app.value_Reach2.config(text =fighter.Reach)

        app.label_win_f2.config(text =fighter.Wins)
        app.value_KOTKO2.config(text = fighter.Win_striking)
        app.value_Dec2.config(text = fighter.Wins_Decision)
        app.value_sub2.config(text = fighter.Wins_ground)

        app.value_Losts2.config(text = fighter.Losts)
        app.value_KO_lost2.config(text =fighter.Lost_striking)
        app.value_Dec_lost2.config(text =fighter.Lost_Decision)
        app.label_sub_lost2.config(text = fighter.Lost_ground)

def Combo1_selected(app):
    global Fighter1
    Fighter1 = Fighter(app.fighter1_combo.get())
    show_fighter_image(app.fighter1_image_label,
                       Fighter1.name)
    fill_informations(app, Fighter1, 1)

def Combo2_selected(app):
    global Fighter2
    Fighter2 = Fighter(app.fighter2_combo.get())
    show_fighter_image(app.fighter2_image_label,
                       Fighter2.name)
    fill_informations(app, Fighter2, 2)
