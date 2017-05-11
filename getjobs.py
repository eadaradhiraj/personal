import sys
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException, WebDriverException
from bs4 import BeautifulSoup
import time

lang = ['You fluently speak English and German']
chromedriver = "./chromedriver"
Soup = lambda htm: BeautifulSoup(htm, 'html.parser')


def gethtmjs(skill, time_period):
    URL = "https://www.thelocal.de/jobs/Berlin/all/" + skill + "?date_posted=" + time_period
    try:
        try:
            driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
        except WebDriverException:
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
    listofjobs=[]
    soup = Soup(gethtmjs(skill='python', time_period='day'))
    for lnk in soup.find_all('a', {"class": "standardJobUrl"}):
        if ('data' in lnk.text or 'Data' in lnk.text or 'BI' in lnk.text or 'Business' in lnk.text or 'business' in lnk.text or 'analytics' in lnk.text or 'Analytics' in lnk.text or 'analyst' in lnk.text or 'Analyst' in lnk.text):
            if 'senior' not in lnk.text and 'Senior' not in lnk.text and 'lead' not in lnk.text and 'Lead' not in lnk.text:
                listofjobs.append(lnk['href'])

    soup = Soup(gethtmjs(skill='sql', time_period='day'))
    for lnk in soup.find_all('a', {"class": "standardJobUrl"}):
        if ('data' in lnk.text or 'Data' in lnk.text or 'BI' in lnk.text or 'Business' in lnk.text or 'business' in lnk.text or 'analytics' in lnk.text or 'Analytics' in lnk.text or 'analyst' in lnk.text or 'Analyst' in lnk.text):
            if 'senior' not in lnk.text and 'Senior' not in lnk.text and 'lead' not in lnk.text and 'Lead' not in lnk.text:
                listofjobs.append(lnk['href'])

    listofjobs = list(set(listofjobs))
    for e in listofjobs:
        print(e)

getjobs()
