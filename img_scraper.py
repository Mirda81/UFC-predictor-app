import requests
from bs4 import BeautifulSoup

# definujte vyhledávací dotaz

def download_pic(fighter):
    # poslat požadavek na vyhledávání
    url = f'https://www.ufc.com/athlete/' + fighter.replace(' ','-').lower()
    print(url)
    response = requests.get(url)

    # extrahování informací z HTML kódu
    soup = BeautifulSoup(response.content, 'html.parser')
    img_tags = soup.find_all('img',class_='hero-profile__image')

    # stáhnutí prvního obrázku
    img_url = img_tags[0]['src']
    response = requests.get(img_url)
    open('f1.PPM', 'wb').write(response.content)
    print("Image downloaded successfully!")

download_pic('Nate Diaz')