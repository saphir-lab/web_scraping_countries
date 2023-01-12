# -*- coding: utf-8 -*-
__author__ = 'P. Saint-Amand'
__appname__ = 'get_countries'
# __appname__, _ = os.path.splitext(os.path.basename(__file__))
__version__ = 'V 0.0.1'

# Standard Python Modules
import logging
import os
from pathlib import Path
import requests
from typing import Any

# External Python Modules
from bs4 import BeautifulSoup

# Personal Python Modules
import utils
from constants import *

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

def init():
    """ Clear Screen, display banner & start the logger. """
    CONSOLE.clear_screen()
    if BANNER:
        print(CONSOLE.get_app_banner(selection="random", banner_lst=banner_lst, appversion=__version__, creator="Designed by " + __author__))
    global logger
    logger = get_logger(logger_name=__appname__, console_loglevel=LOGLEVEL_CONSOLE, file_loglevel=LOGLEVEL_FILE)
    logger.debug("Debug Mode Activated")

if __name__ == "__main__":
    init()