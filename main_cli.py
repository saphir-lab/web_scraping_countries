# -*- coding: utf-8 -*-
__author__ = 'P. Saint-Amand'
__appname__ = 'get_countries'
# __appname__, _ = os.path.splitext(os.path.basename(__file__))
__version__ = 'V 0.0.1'

# Standard Python Modules
import csv
import logging
import os
from pathlib import Path
import requests
from typing import Any

# External Python Modules
import pandas as pd
import typer
from bs4 import BeautifulSoup

# Personal Python Modules
import utils
from constants import *

### Global Variables
all_args={}

def callback_outdir(value:Path) -> Path:
    if value and not value.is_dir() and os.path.splitext(value)[1]:
        raise typer.BadParameter(f"outdir must be a DIRECTORY (not a file)")
    return value

def callback_version(value:bool) -> None:
    if value:
        print(CONSOLE.get_app_banner(selection="random", banner_lst=banner_lst, appversion=__version__, creator="Designed by " + __author__))
        raise typer.Exit()

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

def get_logger(logger_name:str=None, console_loglevel:int=LOGLEVEL_SUCCESS, file_loglevel:int=LOGLEVEL_DISABLE, logfile:Path=None) -> utils.ColorLogger:
    if not logfile and file_loglevel != LOGLEVEL_DISABLE:
        logfile = os.path.join(LOG_DIR,__appname__+".log")
    if not logger_name:
        logger_name, _ = os.path.splitext(os.path.basename(__file__))

    
    logging.addLevelName(LOGLEVEL_SUCCESS, 'SUCCESS')
    log_options = utils.ColorLoggerOptions(logfile_name=logfile, console_logging_level=console_loglevel, logfile_logging_level=file_loglevel)
    logger = utils.ColorLogger(name=__appname__, options=log_options)
    # save_logger_options(log_options)
    return logger

def init(banner=True):
    """ Clear Screen, display banner & start the logger. """
    CONSOLE.clear_screen()
    if banner:
        print(CONSOLE.get_app_banner(selection="random", banner_lst=banner_lst, appversion=__version__, creator="Designed by " + __author__))
    if all_args["debug"]:
        LOGLEVEL_CONSOLE = LOGLEVEL_SUCCESS
    else:
        LOGLEVEL_CONSOLE = LOGLEVEL_DISABLE
    if all_args["logfile"]:
        LOGLEVEL_FILE = logging.DEBUG
    else:
        LOGLEVEL_FILE = LOGLEVEL_DISABLE
    global logger
    logger = get_logger(logger_name=__appname__, console_loglevel=LOGLEVEL_CONSOLE, file_loglevel=LOGLEVEL_FILE, logfile=all_args["logfile"])
    logger.debug("Debug Mode Activated")

def main(outfile:Path = typer.Option(OUT_FILE, "--outfile", "-o", exists=False, resolve_path=True, show_default="countries.csv", help="File Name of the output file"),
        banner:bool = typer.Option(True, help="Display a banner at start of the program", rich_help_panel="Customization and Utils"),
        debug:bool = typer.Option(False, help="Enable debug mode on the console", rich_help_panel="Customization and Utils"),
        logfile:Path = typer.Option(None, "--logfile", "-l", exists=False, resolve_path=True,  help="logfile of detailed activities (debug mode)", rich_help_panel="Customization and Utils"),
        version:bool = typer.Option(False, "--version", "-v", callback=callback_version, is_eager=True, help="Display version of the program", rich_help_panel="Customization and Utils")
        ) -> None:
    # Put all arguments in a dictionnary & perform extra validation or default value assigment
    # Needed in order to be able to compare/use value of other parameters, what was not possible using callback procedure
    all_args["outfile"]=outfile
    all_args["banner"]=banner
    all_args["debug"]=debug
    all_args["logfile"]=logfile
    all_args["version"]=version
    
    init(banner=all_args["banner"])
    validate_params()
    ### TODO: Add you code here below ###
    df_countries = get_countries(URL_COUNTRIES)
    save_to_csv(df=df_countries, outfile=all_args["outfile"])
    wiki_details_as_html(df_countries, "wiki_site")

    # End of program
    if all_args["logfile"]:
        logger.log(LOGLEVEL_SUCCESS, f'logfile available on : {all_args["logfile"]}')

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

def validate_params() -> None:
    ### TODO: Add exra validation if needed

    # Display Debug information about parameters    
    all_args_str=""
    for k,v in all_args.items():
        all_args_str += f"  - {k}: {v}\n"
    logger.debug(f"Parameters :\n{all_args_str}")

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
            htmltable = soup.find("table",{"class":"infobox ib-country vcard"})
            outfile = os.path.join(DATA_DIR, df["Country"][i] + ".html")
            with open(outfile, 'w') as f:
                f.write(str(htmltable))
        i += 1
        save_to_csv(df=df, outfile=all_args["outfile"])

if __name__ == "__main__":
    CONSOLE.clear_screen()
    typer.run(main)
