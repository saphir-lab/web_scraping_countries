# -*- coding: utf-8 -*-
__author__ = 'P. Saint-Amand'
__appname__ = 'get_countries'
# __appname__, _ = os.path.splitext(os.path.basename(__file__))
__version__ = 'V 0.0.1'

# Standard Python Modules
import os
from pathlib import Path
import requests
from typing import Any

# External Python Modules
import pandas as pd
from bs4 import BeautifulSoup

# Personal Python Modules
# import utils
from init import *

### Global Variables
OUT_FILE = os.path.join(OUT_DIR,"countries.csv")
LOG_FILE = None
URL_COUNTRIES = r"https://www.worldometers.info/geography/alphabetical-list-of-countries"
URL_WIKI = r"https://en.wikipedia.org/wiki/"

def get_countries(url:str) -> pd.DataFrame:
    df = pd.DataFrame()
    response = requests.get(url)
    logger.info(f"Get content of {url}")
    if response.status_code != 200:
        logger.warning(f"Response Code : {response.status_code}")    
    else:
        logger.log(LOGLEVEL_SUCCESS, f"Response Code : {response.status_code}")
        soup = BeautifulSoup(response.text, "html.parser")
        htmltable = soup.find( "table")
        countries = tableDataText(htmltable)
        df = pd.DataFrame(countries[1:], columns=countries[0], dtype='string')
        logger.debug("Sample data retrieved before transformation (top 5)")
        logger.debug(df.head(5).to_string())

        # Some Cleanup
        del df[df.columns[0]]   # Drop fifrst column (id)
        for column in df.columns.values:
            df[column] = df[column].str.replace(",", "", regex=False)    # Remove coma on all columns (as used as thousand separator fir numerics)
            if column == "Country":
                df[column] = df[column].str.replace("\"|'| \(.*\)","",regex=True).str.strip()   # Remove quote, double quote & content between parenthesis
            else:
               df[column] = df[column].fillna(0).astype(int)
        df["wiki_site"] = df["Country"].apply(lambda x: os.path.join(URL_WIKI, x.title().replace(" ", "_"))) # add a column with the expected link for wiki site
        logger.info("Sample data retrieved after transformation (top 5)")
        logger.info(df.head(5).to_string())   
    return df

def init_logger():
    global logger
    logger = get_logger(logger_name=__appname__, console_loglevel=LOGLEVEL_CONSOLE, file_loglevel=LOGLEVEL_FILE, logfile=LOG_FILE)
    logger.debug("Debug Mode Activated")

def save_to_csv(df:pd.DataFrame, outfile:Path, sep:str=",") -> None:
    df.to_csv(outfile, index=False, encoding="utf-8", sep=sep)
            
def tableDataText(table):    
    """Parses a html segment started with tag <table> followed 
    by multiple <tr> (table rows) and inner <td> (table data) tags. 
    It returns a list of rows with inner columns. 
    Accepts only one <th> (table header/data) in the first row.
    """
    def rowgetDataText(tr, coltag='td'): # td (data) or th (header)       
        return [td.get_text(strip=True) for td in tr.find_all(coltag)]  
    rows = []
    trs = table.find_all('tr')
    headerow = rowgetDataText(trs[0], 'th')
    if headerow: # if there is a header row include first
        rows.append(headerow)
        trs = trs[1:]
    for tr in trs: # for every table row
        rows.append(rowgetDataText(tr, 'td') ) # data row       
    return rows

def wiki_details_as_html(df:pd.DataFrame, url_column_name:str)-> None:
    """ Go to wiki page of each country & save the left frame with details as html file"""
    df["wiki_status"]=pd.Series(dtype='int')
    i=0
    for url in df[url_column_name]:
        response = requests.get(url)
        df["wiki_status"][i] = response.status_code
        logger.info(f"Get content of {url}")
        if response.status_code != 200:
            logger.warning(f"Response Code : {response.status_code}")    
        else:
            logger.log(LOGLEVEL_SUCCESS, f"Response Code : {response.status_code}")
            soup = BeautifulSoup(response.text, "html.parser")
            # htmltable = soup.find("table",{"class":"infobox ib-country vcard"})
            # htmltable = soup.find("table",{"class":"infobox"})  #Find the first table with class infobox
            outfile = os.path.join(DATA_DIR, df["Country"][i] + ".html")
            with open(outfile, 'w') as f:
                f.write(str(soup))
        i += 1
    return df

if __name__ == "__main__":
    CONSOLE.clear_screen()
    if BANNER_DISPLAY:
        print(CONSOLE.get_app_banner(selection="random", banner_lst=BANNERS, appversion=__version__, creator=__author__))
    init_logger()
    df_countries = get_countries(URL_COUNTRIES)
    save_to_csv(df=df_countries, outfile=OUT_FILE)
    df_countries = wiki_details_as_html(df_countries, "wiki_site")
    save_to_csv(df=df_countries, outfile=OUT_FILE)

