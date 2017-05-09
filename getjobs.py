import sys
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException
from bs4 import BeautifulSoup
import time

Soup = lambda htm: BeautifulSoup(htm,'html.parser')
chromedriver = "./chromedriver"
time_periods = ['month','day']

URL="https://www.thelocal.de/jobs/Berlin/all/python?date_posted=day"

def gethtm():
    try:
        driver = webdriver.Chrome(chromedriver)
        driver.get(URL)

        while True:
            try:
                time.sleep(5)
                el = driver.find_element_by_class_name('load_more').click()
            except NoSuchElementException:
                break

        htmsrc = driver.page_source
        driver.quit()
        return (htmsrc)
    except NoSuchWindowException:
        sys.exit('The window closed unexpectedly.')

def getjobs():
    soup = Soup(gethtm())
    for lnk in soup.find_all('a', { "class" : "standardJobUrl" }):
        if ('data' in lnk.text or 'Data' in lnk.text or 'BI' in lnk.text or 'Business' in lnk.text or 'business' in lnk.text or 'analytics' in lnk.text or 'Analytics' in lnk.text):
            if 'senior' not in lnk.text and 'Senior' not in lnk.text and 'lead' not in lnk.text and 'Lead' not in lnk.text:
                print(lnk['href'])

getjobs()
