# -*- coding: utf-8 -*-
__author__ = 'P. Saint-Amand'
__appname__ = 'get_wiki_details'
# __appname__, _ = os.path.splitext(os.path.basename(__file__))
__version__ = 'V 0.0.1'


import os
import re
from init import *

import pandas as pd
from bs4 import BeautifulSoup

LOG_FILE = os.path.join(LOG_DIR,__appname__+".log")
LOGLEVEL_FILE = logging.WARNING
# LOGLEVEL_CONSOLE = logging.DEBUG
OUT_FILE = os.path.join(OUT_DIR,"countries_details.csv")
SAMPLE_FILE = "Afghanistan.html"

fields_txt=["Status", "Government", "Currency", "Driving side", "Calling code", "ISO 3166 code"]
fields_lst=["Capital", "Capitaland largest city", "Largest city", "Official languages", "Demonym(s)", "Internet TLD"]
fields_lst_and_pct=["Ethnic groups", "Religion", ]

def get_file_content(filename:Path=None):
    fullname = os.path.join(DATA_DIR,filename)
    with open(fullname,'r') as f:
            lines = f.readlines()
    content = "".join(lines)
    soup = BeautifulSoup(content, "html.parser")
    return soup

def get_tag_text(tag) -> str:
    if tag:
        return re.sub(r",|•|\[.*\]|","",tag.text).strip()       # remove comma, bullet(•), anything between square bracket [] & stip result
    else:
        return "None"

def get_tag_lst(tag) -> list:
    if tag:
        r=[]
        for string in tag.stripped_strings:
            string = re.sub(r",|•|\[.*\]|","",string).strip()
            if string:
                r.append(string)
        return r
    else:
        return []

def get_tag_string(tag):
    if tag and tag.strings:
        r=""
        for string in tag.stripped_strings:
            string = re.sub(r",|•|\[.*\]|","",string).strip()
            if string:
                r += string + "; "
        return r[:-2]
    else:
        return "None"

def get_tag_content(tag):
    if tag:
        if tag.children:
            r = ""
            for i, child in enumerate(tag.children):
                if child.string:
                    r += child.string
            return r
        else:
            return "!!! No Child :" + tag.text()
    else:
        return "None"

def init_logger():
    global logger
    logger = get_logger(logger_name=__appname__, console_loglevel=LOGLEVEL_CONSOLE, file_loglevel=LOGLEVEL_FILE, logfile=LOG_FILE)
    logger.debug("Debug Mode Activated")

def parse_all_countries() -> list[dict]:
    result=[]
    for filename in sorted(os.listdir(DATA_DIR)):
        if ".html" in filename:
            result.append(parse_one_country(filename=filename))
    return result

def parse_one_country(filename:Path=None) -> dict:
    logger.info(f"Get Details from file {filename}")
    soup = get_file_content(filename)
    htmltable = soup.find("table",{"class":"infobox"})  # Get the table located on the right frame
    country_dict={}
    country_dict["Country"]=filename[:-5]
    if not htmltable:
        logger.warning(f"File {filename} has no country details")
    else:
        trs = htmltable.find_all('tr')  
        for tr in trs: # for every table row
            th = get_tag_text(tr.find("th"))
            if th in fields_txt:
                td = get_tag_text(tr.find("td"))
                country_dict[th]=td
                logger.debug(f"- {th}: {td}")
            elif th in fields_lst:
                td = get_tag_lst(tr.find("td"))
                if th == "Capitaland largest city":
                    country_dict["Capital"]=td[0]
                    if ";" in td[-1]:
                        country_dict["Capital location"]=td[-1]                    
                    country_dict["Largest city"]=td[0]
                    if ";" in td[-1]:
                        country_dict["Largest city location"]=td[-1]
                    country_dict["Largest city is Capital"]=True
                elif th in ["Capital", "Largest city"]:
                    country_dict[f"{th}"]=td[0]
                    if ";" in td[-1]:
                        country_dict[f"{th} location"]=td[-1]
                    country_dict["Largest city is Capital"]=False
                else:
                    country_dict[f"{th}"]=td
                logger.debug(f"- {th}: {td}")
            else:
                pass

        logger.log(LOGLEVEL_SUCCESS, f"File {filename} parsed")
    return country_dict

def save_details_debug():
    for filename in sorted(os.listdir(DATA_DIR)):
        if ".html" in filename:
            logger.info(f"Get Details from file {filename}")
            fullname = os.path.join(DATA_DIR,filename)
            with open(fullname,'r') as f:
                    lines = f.readlines()
            content = "".join(lines)
            soup = BeautifulSoup(content, "html.parser")
            htmltable = soup.find("table",{"class":"infobox"})
            if not htmltable:
                logger.warning(f"File {filename} has no content")
            else:
                trs = htmltable.find_all('tr')
                countryname = filename[:-5]
                outfile = os.path.join(OUT_DIR,countryname+".txt")
                data_parsed = ""
                for tr in trs: # for every table row
                    data_parsed += f'- {get_tag_string(tr.find("th"))}: {get_tag_string(tr.find("td"))}\n'
                    # data_parsed += f'- {get_tag_text(tr.find("th"))}: {get_tag_text(tr.find("td"))}\n'
                    # print(get_tag_content(tr.find("th")))
                    # print(get_tag_content(tr.find("td")))
                    # print("-"*20)
                print(data_parsed)
                # with open(outfile, 'w') as f:
                #     f.write(data_parsed)
                logger.log(LOGLEVEL_SUCCESS, f"File {filename} parsed")

if __name__ == "__main__":
    CONSOLE.clear_screen()
    if BANNER_DISPLAY:
        print(CONSOLE.get_app_banner(selection="random", banner_lst=BANNERS, appversion=__version__, creator=__author__))
    init_logger()
    # result = parse_one_country(SAMPLE_FILE)
    all_countries = parse_all_countries()
    df = pd.DataFrame(all_countries)
    df.to_csv(OUT_FILE, encoding="UTF-8", index=False, sep=";", header=True, mode="w")