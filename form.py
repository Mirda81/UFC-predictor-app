import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from img_scraper import download_pic
# vytvoření okna
root = tk.Tk()
root.title("Fighter Comparison")
root.config(bg="white")
root.resizable(False, False)
root.geometry("800x600")

def filter_fighters(*args):
    """Funkce pro filtrování seznamu bojovníků"""
    filter_text = fighter1_combo.get()
    filtered_fighters = [fighter for fighter in fighters if filter_text.lower() in fighter.lower()]
    fighter1_combo.config(values=filtered_fighters)
    print(filter_text)

# funkce pro zobrazení obrázku bojovníka
def show_fighter_image(fighter, number):
    download_pic(fighter)
    img = Image.open("f1.PPM")
    img = img.resize((300, 250), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    if number ==1:
        fighter1_image_label.config(image=img)
        fighter1_image_label.image = img
    if number ==2:
        fighter2_image_label.config(image=img)
        fighter2_image_label.image = img
       # fighter1_image_label.pack()

fighters = ["Nate Diaz", "Conor McGregor"]
# vytvoření rozbalovacího seznamu pro výběr bojovníka 1
fighter1_label = ttk.Label(root, text="Fighter 1:",background="black",foreground="white")
fighter1_combo = ttk.Combobox(root, values=fighters)
fighter1_label.place(x=20,y=20)
fighter1_combo.place(x=100,y=20, width=100)

# vytvoření rozbalovacího seznamu pro výběr bojovníka 2
fighter2_label = ttk.Label(root, text="Fighter 2:",background="black",foreground="white")
fighter2_combo = ttk.Combobox(root, values=fighters)
fighter2_label.place(x=20,y=50)
fighter2_combo.place(x=100,y=50, width=100)


# vytvoření Label widgetu pro zobrazení obrázku bojovníka 1
fighter1_image_label = ttk.Label(root,background="white")
fighter1_image_label.place(x=20,y=90, width=280, height=250)

# vytvoření Label widgetu pro zobrazení obrázku bojovníka 2
fighter2_image_label = ttk.Label(root,background="white")
fighter2_image_label.place(x=480,y=90, width=300, height=250)

# napojení callbacku na událost změny výběru v rozbalovacím seznamu
fighter1_combo.bind("<KeyRelease>", filter_fighters)
fighter1_combo.bind("<<ComboboxSelected>>", lambda event: show_fighter_image(fighter1_combo.get(),1))
fighter2_combo.bind("<<ComboboxSelected>>", lambda event: show_fighter_image(fighter2_combo.get(),2))


# zobrazit okno
root.mainloop()
