from bs4 import BeautifulSoup
from requests import get
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import time

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
    
    driver_setup(url)
    driver = driver_setup(url)
    button_click(driver)
    site_scrolling(driver)
    imgs = html_acces(driver)
    image_download(imgs, userchoice_count)

def driver_setup(url):

    driver = webdriver.Safari()
    driver.maximize_window()
    driver.get(url)
    return(driver)
    
def button_click(driver):

    btn = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//button[text()="Load more photos"]')))
    btn.click()    

def site_scrolling(driver):
    
    time.sleep(2)
    scroll_pause_time = 1 
    screen_height = driver.execute_script("return window.screen.height;")  
    i = 1

    while True:
        
        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
        i += 1
        time.sleep(scroll_pause_time)
        scroll_height = driver.execute_script("return document.body.scrollHeight;")  
        if (screen_height) * i > scroll_height:
            break 

def html_acces(driver):

    soup = BeautifulSoup(driver.page_source, 'lxml')
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