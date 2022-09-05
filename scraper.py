from requests import get
from bs4 import BeautifulSoup
import os

def main_logic():

    userchoice_photo = input("What are you searching for ?\n")
    userchoice_foldername = userchoice_photo

    while True:
        try:
            userchoice_count = int(input("How many photos you whish to download?\n"))
            break
        except ValueError:
            print("You must provide a number !\n")
    try:
        os.mkdir(os.path.join(os.getcwd(), userchoice_foldername))
        os.chdir(os.path.join(os.getcwd(), userchoice_foldername))
    except:
        print('Failed to create directory, provided path already exists\n')
        os.chdir(os.path.join(os.getcwd(), userchoice_foldername))

    url = f'https://unsplash.com/s/photos/{userchoice_photo}'

    imgs = html_acces(url)
    image_download(imgs, userchoice_count)

def html_acces(url):
    
    page = get(url)
    soup = BeautifulSoup(page.content, 'lxml')
    imgs = soup.find_all('img',{'class' : 'YVj9w'}, alt=True)
    return imgs

def image_download(imgs, userchoice_count):

    for idx, image in enumerate(imgs):

        if  idx < userchoice_count:
            lnk = image['src']
            name = image['alt']
            with open(name.replace(' ', '-').replace('/', '') + '.jpg', 'wb') as f:
                im = get(lnk)
                f.write(im.content)
                print('Saving: ' + name + '.jpg')
        
main_logic()