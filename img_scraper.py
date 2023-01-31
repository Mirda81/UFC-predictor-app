import requests
from bs4 import BeautifulSoup
from PIL import ImageTk, Image

def download_pic(fighter):
    # poslat požadavek na vyhledávání
    url = f'https://www.ufc.com/athlete/' + fighter.replace(' ','-').lower()
    print(url)
    response = requests.get(url)

    # extrahování informací z HTML kódu
    soup = BeautifulSoup(response.content, 'html.parser')
    img_tags = soup.find_all('img',class_='hero-profile__image')
    if len(img_tags)==0:
        img = Image.open("2.png")
        inverted_image = Image.new("RGB", img.size, (255, 255, 255))
        inverted_image.paste(img, (0, 0), img)
        img = inverted_image
    else:
        # stáhnutí prvního obrázku
        img_url = img_tags[0]['src']
        response = requests.get(img_url)
        open('f1.PPM', 'wb').write(response.content)
        img = Image.open("f1.PPM")
    img = img.resize((250, 250), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    return img



