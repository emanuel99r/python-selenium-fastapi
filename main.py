from fastapi import FastAPI, BackgroundTasks, HTTPException, Form, Request
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from PIL import ImageFile
import urllib.request as urllib
from selenium.common.exceptions import NoSuchElementException,ElementNotInteractableException

#import ImageFile

app = FastAPI()
#result=""
templates = Jinja2Templates(directory='templates')
@app.get("/")
def form_post(request: Request):
    result_dropdown = ""
    result_image = ""
    return templates.TemplateResponse('template.html', context={'request': request, 'result': result_image+", "+result_dropdown})

@app.post('/', response_class=HTMLResponse)
def form_post(request: Request, fname: str = Form(...)):
    global link
    link = fname
    print(fname)
    evaluate_page()
    dropdown()
    return templates.TemplateResponse('template.html', context={'request': request, 'result': result_image+","+result_dropdown})

def evaluate_page():
    global driver
    global result_image
    global result_dropdown
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    prefs = {"profile.managed_default_content_settings.images":2}
    chrome_options.headless = True


    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(link)
 
    sleep(1)
    

    try:
        link_image = driver.find_element_by_xpath("//img[@class='width-2-3 medium-up-width-100 inline-block']").get_attribute("src")
        if (getsizes(link_image)[0]) < 15000:
            global result_image
            result_image = "Images not high resolution"
            return result_image
        else:
            result_image = "Good resolution"
            return result_image
         
    except NoSuchElementException:
        result_image = "Wrong page"
        return result_image
    

def getsizes(uri):
    file = urllib.urlopen(uri)
    size = file.headers.get("content-length")
    if size: size = int(size)
    p = ImageFile.Parser()
    while 1:
        data = file.read(1024)
        if not data:
            break
        p.feed(data)
        if p.image:
            return size, p.image.size
            break
    file.close()
    return size, None

def dropdown():
    try:

        action = webdriver.ActionChains(driver)
        element = driver.find_element_by_xpath("//a[@class='relative inline-block symbol-report']")
        action.move_to_element(element)
        action.perform()
        sleep(1)
        global result_dropdown
        driver.find_element_by_xpath("//img[@class='width-100 margin-bottom-xsmall shadow-light']").click()
        
        result_dropdown = "Javascript dropdown good"
        return result_dropdown
        
    except ElementNotInteractableException:
        result_dropdown = "Javascript dropdown not working properly"
        return result_dropdown
    except NoSuchElementException:
        result_dropdown = "Wrong page"
        return result_dropdown