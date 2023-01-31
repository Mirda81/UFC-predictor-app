from PIL import ImageTk, Image
from img_scraper import download_pic


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

    app.fighter1_combo.bind("<<ComboboxSelected>>", lambda event: show_fighter_image(app.fighter1_image_label,
                                                                                               app.fighter1_combo.get()),
                            add="+")

    app.fighter2_combo.bind("<KeyRelease>",
                            lambda event: app.fighter2_combo.config(
                                values=filter_names(fighter_list, app.fighter2_combo.get())))
    app.fighter2_combo.bind("<<ComboboxSelected>>", lambda event: show_fighter_image(app.fighter2_image_label,
                                                                                               app.fighter2_combo.get()),
                            add="+")