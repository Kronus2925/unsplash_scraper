from requests import get
from bs4 import BeautifulSoup
import os
import shutil
import sys

userchoice_photo = str(input("What are you searching for ?\n"))
while True:
    try:
        userchoice_count = int(input("How many photos you whish to download?\n"))
    except:
        print("You must provide a number !\n")
    else:
        if isinstance(userchoice_count, int) == True:
            break
        else:
            continue
userchoice_foldername = userchoice_photo

url = f'https://unsplash.com/s/photos/{userchoice_photo}'


def getimg(userchoice_foldername, url):
    try:
        os.mkdir(os.path.join(os.getcwd(), userchoice_foldername))
    except:
        shutil.rmtree(os.path.join(os.getcwd(), userchoice_foldername))
    try:
        os.mkdir(os.path.join(os.getcwd(), userchoice_foldername))
    except:
        pass
    os.chdir(os.path.join(os.getcwd(), userchoice_foldername))
    global img
    global cnt
    page = get(url)
    soup = BeautifulSoup(page.content, 'lxml')
    img = soup.find_all('img', alt=True)
    cnt = 0
    return img,cnt

def imagescrape(img, cnt, userchoice_count):
    try:  
        for image in img:
            if  cnt < userchoice_count:
                cnt += 1
                lnk = image['src']
                name = image['alt']
                with open(name.replace(' ', '-').replace('/', '') + '.jpg', 'wb') as f:
                    im = get(lnk)
                    f.write(im.content)
                    print('Saving: ' + name + '.jpg')
    except:
        print("There is nothing to save, try again")          
        os.execl(sys.executable, sys.executable, *sys.argv)
        
getimg(userchoice_foldername, url)
imagescrape(img, cnt, userchoice_count)