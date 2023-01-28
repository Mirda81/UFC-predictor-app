import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from img_scraper import download_pic
import pandas as pd
from keras.models import load_model
from predict import prediction
from form_helper import create_form
# načtení modelu
model = load_model('model.h5')
model.load_weights('my_model_weights.h5')  # to load
# vytvoření okna
root = tk.Tk()
root.title("Fighter Comparison")
root.config(bg="black")
root.resizable(False, False)
root.geometry("800x600")
df = pd.read_csv('fighter_total_stats.csv')
fighters= df['FIGHTER'].tolist()
def filter_fighters(*args):
    """Funkce pro filtrování seznamu bojovníků"""
    filter_text1 = fighter1_combo.get()
    filter_text2 = fighter2_combo.get()
    filtered_fighters1 = [fighter for fighter in fighters if filter_text1.lower() in fighter.lower()]
    filtered_fighters2 = [fighter for fighter in fighters if filter_text2.lower() in fighter.lower()]
    fighter1_combo.config(values=filtered_fighters1)
    fighter2_combo.config(values=filtered_fighters2)
    print(filter_text1)

# funkce pro zobrazení obrázku bojovníka
def show_fighter_image(fighter, number):
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
        fighter1_image_label.config(image=img)
        fighter1_image_label.image = img
    if number ==2:
        fighter2_image_label.config(image=img)
        fighter2_image_label.image = img
       # fighter1_image_label.pack()



# frame pro bokovníka 1
label_border1 = ttk.Label(root, background = "red",foreground = "red")
label_border1.place(x=18, y=48, width=292, height=404)

label_f1 = ttk.Label(root, relief="groove",background = "black",borderwidth = 5,foreground = "red")
label_f1.place(x=20, y=50, width=288, height=400)
# frame pro bokovníka 2
label_border2 = ttk.Label(root, background = "blue",foreground = "blue")
label_border2.place(x=480, y=48, width=292, height=404)

label_f2 = ttk.Label(root, relief="groove",background = "black",borderwidth = 5,foreground = "red")
label_f2.place(x=482, y=50, width=288, height=400)



# vytvoření rozbalovacího seznamu pro výběr bojovníka 1
#fighter1_label = ttk.Label(root, text="Fighter 1:",background="black",foreground="white")
fighter1_combo = ttk.Combobox(root, values=fighters)
#fighter1_label.place(x=20,y=20)
fighter1_combo.place(x=100,y=30, width=200)

# vytvoření rozbalovacího seznamu pro výběr bojovníka 2
#fighter2_label = ttk.Label(root, text="Fighter 2:",background="black",foreground="white")
fighter2_combo = ttk.Combobox(root, values=fighters)
#fighter2_label.place(x=480,y=20)
fighter2_combo.place(x=560,y=30, width=200)


# vytvoření Label widgetu pro zobrazení obrázku bojovníka 1
fighter1_image_label = ttk.Label(root,background="black")
fighter1_image_label.place(x=35,y=70, width=250, height=250)

# vytvoření Label widgetu pro zobrazení obrázku bojovníka 2
fighter2_image_label = ttk.Label(root,background="black")
fighter2_image_label.place(x=500,y=70, width=250, height=250)

#středový panel
label_cara = ttk.Label(root, text="",background="gray",foreground="black",relief="groove",borderwidth = 5)
label_cara.place(x=310, y=48,width=170,height=404)
#panel popisků
label_Middle= ttk.Label(root, text="",background="black",foreground="white",relief="raised")
label_Middle.place(x=360, y=48,width=70,height=404)

# udaje vek atd
label_Age= ttk.Label(root, text="  AGE",background="black",foreground="yellow",font=("Helvetica", 12, "bold"))
label_Age.place(x=365, y=60,width=60,height=25)

label_Height= ttk.Label(root, text="Height",background="black",foreground="yellow",font=("Helvetica", 12, "bold"))
label_Height.place(x=365, y=90,width=60,height=25)

label_Weight= ttk.Label(root, text="Weight",background="black",foreground="yellow",font=("Helvetica", 12, "bold"))
label_Weight.place(x=365, y=120,width=60,height=25)

label_Reach= ttk.Label(root, text="Reach",background="black",foreground="yellow",font=("Helvetica", 12, "bold"))
label_Reach.place(x=365, y=150,width=60,height=25)

# statistsiky wins
label_Age= ttk.Label(root, text=" Wins",background="black",foreground="green",font=("Helvetica", 14, "bold"))
label_Age.place(x=365, y=190,width=60,height=25)

label_Height= ttk.Label(root, text=" KO/TKO",background="black",foreground="green",font=("Helvetica", 10, "bold"))
label_Height.place(x=365, y=220,width=60,height=25)

label_Weight= ttk.Label(root, text="   DEC",background="black",foreground="green",font=("Helvetica", 10, "bold"))
label_Weight.place(x=365, y=250,width=60,height=25)
label_Weight= ttk.Label(root, text="   SUB",background="black",foreground="green",font=("Helvetica", 10, "bold"))
label_Weight.place(x=365, y=280,width=60,height=25)
# statistsiky losts
label_Age= ttk.Label(root, text="Losts",background="black",foreground="red",font=("Helvetica", 14, "bold"))
label_Age.place(x=365, y=320,width=60,height=25)

label_Height= ttk.Label(root, text=" KO/TKO",background="black",foreground="red",font=("Helvetica", 10, "bold"))
label_Height.place(x=365, y=350,width=60,height=25)

label_Weight= ttk.Label(root, text="   DEC",background="black",foreground="red",font=("Helvetica", 10, "bold"))
label_Weight.place(x=365, y=380,width=60,height=25)
label_Weight= ttk.Label(root, text="   SUB",background="black",foreground="red",font=("Helvetica", 10, "bold"))
label_Weight.place(x=365, y=410,width=60,height=25)

#predictions
label_Weight= ttk.Label(root, text="Probibility of win%: ",background="black",foreground="Green",font=("Helvetica", 10, "bold"))
label_Weight.place(x=30, y=330,width=130,height=25)


# napojení callbacku na událost změny výběru v rozbalovacím seznamu
fighter1_combo.bind("<KeyRelease>", filter_fighters)
fighter2_combo.bind("<KeyRelease>", filter_fighters)
fighter1_combo.bind("<<ComboboxSelected>>", lambda event: show_fighter_image(fighter1_combo.get(),1))
fighter2_combo.bind("<<ComboboxSelected>>", lambda event: show_fighter_image(fighter2_combo.get(),2),add="+")
fighter2_combo.bind("<<ComboboxSelected>>", lambda event: prediction(fighter1_combo.get(),fighter2_combo.get(),model),add="+")

# zobrazit okno
root.mainloop()
