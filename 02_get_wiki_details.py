# -*- coding: utf-8 -*-
__author__ = 'P. Saint-Amand'
__appname__ = 'get_wiki_details'
# __appname__, _ = os.path.splitext(os.path.basename(__file__))
__version__ = 'V 0.0.1'


import os
import re
from bs4 import BeautifulSoup
from init import *

LOG_FILE = os.path.join(LOG_DIR,__appname__+".log")
LOGLEVEL_FILE = logging.WARNING

def get_tag_text(tag):
    if tag:
        # return re.sub(r",|\[\d*\]|","",tag.text).replace("\n\n","\n").strip()
        return re.sub(r",|\[\d*\]|","",tag.text).strip()
    else:
        return "None"

def init_logger():
    global logger
    logger = get_logger(logger_name=__appname__, console_loglevel=LOGLEVEL_CONSOLE, file_loglevel=LOGLEVEL_FILE, logfile=LOG_FILE)
    logger.debug("Debug Mode Activated")

def save_details():
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
                    data_parsed += f'- {get_tag_text(tr.find("th"))}: {get_tag_text(tr.find("td"))}\n'
                with open(outfile, 'w') as f:
                    f.write(data_parsed)
                logger.log(LOGLEVEL_SUCCESS, f"File {filename} parsed")

if __name__ == "__main__":
    CONSOLE.clear_screen()
    if BANNER_DISPLAY:
        print(CONSOLE.get_app_banner(selection="random", banner_lst=BANNERS, appversion=__version__, creator=__author__))
    init_logger()
    save_details()
    