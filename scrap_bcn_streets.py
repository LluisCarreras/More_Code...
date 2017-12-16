# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 15:48:20 2017

@author: Lluís

This file scraps the meaning and more info of the streets of Barcelona and saves the data 
in a JSON file.

"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import json

# First, get the codes of the streets in Barcelona from a csv file downloaded from 
# http://opendata-ajuntament.barcelona.cat/data/es/dataset, and save them in a list.
street_codes = []
with open("CARRERER.csv", encoding="utf8") as street_codes_file:  
    for line in street_codes_file:
        code = line.split(",")[0]
        street_codes.append(code)
street_codes.pop(0)

# Scrap the info for every street and save it in a dictionary.
streets = {}
for i in street_codes:
    # The street codes must have 6 digits, adding zeroes to the left if necesary.
    code = ("00000" + i)[-6:]
    url = "http://w10.bcn.cat/APPS/nomenclator/ficha.do?codic=" + code + "&idioma=0"
    #"http://w10.bcn.cat/APPS/nomenclator/ficha.do?codic=029400&idioma=0"
    
    # Scrapping snipet...
    try:
        html = urlopen(url)
        bsObj = BeautifulSoup(html)
        tags_list = bsObj.findAll("td", {"class":"textonoticia"})
        text_list = [tag.get_text() for tag in tags_list] 
        streets[code] = text_list
    except:
        pass

# Save data in a JSON file.    
with open('BCN_nomenclator.json', 'w') as outfile:
    json.dump(streets, outfile, sort_keys=True, indent=4)