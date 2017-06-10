#!/usr/bin/env python
# -*- coding: utf-8 -*-
#This code is built to run on both python and python3

import os, csv
from selenium import webdriver
from bs4 import BeautifulSoup


class Mango(object):
    #creating a class for mango.com
    def __init__(self):
        #lambda function to create soup of html code
        self._Soup = lambda htm: BeautifulSoup(htm,'html.parser')
        #static string variable with URL
        self._URL = 'http://shop.mango.com/DE'
        #static variable with lcoation of chromedriver
        self._chromedriver = "./chromedriver"
        #get products info when object is created
        self._products=self._getproducts()

    def _gethtml(self,url):
        #get html source code of the webpage using chromedriver
        os.environ["webdriver.chrome.driver"] = self._chromedriver
        driver = webdriver.Chrome(self._chromedriver)
        driver.get(url)
        htmsrc=driver.page_source
        driver.quit()
        return htmsrc

    def _getproducts(self):
        #loads the products and categories into a dictionary data structure
        soup = self._Soup(self._gethtml(self._URL))
        proddic={}

        proddic['damen']=proddic['herren']=proddic['violeta']=proddic['kinder']=[]
        for link in soup.findAll('a', href=True):
            lnk=link['href']
            if "accessoires" in link['href'] or "artikel" in link['href']:
                item=link['href'].split('/')
                try:
                    proddic[item[-3]].append(item[-1])
                except KeyError:
                    pass

        return (proddic)

    def _dict2csv(self,nm):
        #converting the dictionary of lists into a csv format
        with open(nm, 'w') as f:  # Just use 'w' mode in 3.x
            w = csv.writer(f,lineterminator='\n')
            w.writerow(self._products.keys())
            w.writerows(zip(*self._products.values()))

    def display(self):
        #To print the result in a dictionary format
        print (self._products)

    def getcsv(self,nm):
        #To create a csv file of the results
        self._dict2csv(nm)