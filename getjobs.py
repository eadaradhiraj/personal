import sys
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException
from bs4 import BeautifulSoup
import time

lang = ['You fluently speak English and German']

Soup = lambda htm: BeautifulSoup(htm, 'html.parser')


def gethtmjs(skill, time_period):
    URL = "https://www.thelocal.de/jobs/Berlin/all/" + skill + "?date_posted=" + time_period
    try:
        driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])
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

    jobs = []

    '''
    soup = Soup(gethtmjs(skill='python', time_period='week'))
    for lnk in soup.find_all('a', {"class": "standardJobUrl"}):
        if ('data' in lnk.text or 'Data' in lnk.text or 'BI' in lnk.text or 'Business' in lnk.text or 'business' in lnk.text or 'analytics' in lnk.text or 'Analytics' in lnk.text):
            if 'senior' not in lnk.text and 'Senior' not in lnk.text and 'lead' not in lnk.text and 'Lead' not in lnk.text:
                jobs.append(lnk['href'])
    '''

    soup = Soup(gethtmjs(skill='sql', time_period='week'))
    for lnk in soup.find_all('a', {"class": "standardJobUrl"}):
        if 'business' in lnk.text or 'Business' in lnk.text or 'report' in lnk.text or 'Report' in lnk.text:
            if 'Lead' not in lnk.text and 'lead' not in lnk.text and 'Senior' not in lnk.text and 'senior' not in lnk.text:
                print(lnk['href'])


getjobs()
