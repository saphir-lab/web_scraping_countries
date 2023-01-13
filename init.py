import logging
import os
from pathlib import Path
from banners import BANNERS
from utils import Console
from utils import ColorLogger, ColorLoggerOptions

# Some interresting path
CUR_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(CUR_DIR,"data")
LOG_DIR = os.path.join(CUR_DIR,"log")
# LOGFILE = os.path.join(LOG_DIR,"main.log")
OUT_DIR = os.path.join(CUR_DIR,"out")

# Other Constants
BANNER_DISPLAY = True
BANNER_SELECTION = "random"
CONSOLE = Console(colored=True)
LOGLEVEL_SUCCESS = 15
LOGLEVEL_DISABLE = 99999
LOGLEVEL_CONSOLE = LOGLEVEL_SUCCESS
LOGLEVEL_FILE = LOGLEVEL_DISABLE
# LOGLEVEL_FILE = logging.DEBUG

def get_logger(logger_name:str=None, console_loglevel:int=LOGLEVEL_SUCCESS, file_loglevel:int=LOGLEVEL_DISABLE, logfile:Path=None) -> ColorLogger:
    if not logger_name:
        logger_name, _ = os.path.splitext(os.path.basename(__file__))
    if not logfile and file_loglevel != LOGLEVEL_DISABLE:
        logfile = os.path.join(LOG_DIR,logger_name+".log")
    logging.addLevelName(LOGLEVEL_SUCCESS, 'SUCCESS')
    log_options = ColorLoggerOptions(logfile_name=logfile, console_logging_level=console_loglevel, logfile_logging_level=file_loglevel)
    logger = ColorLogger(name=logger_name, options=log_options)
    # save_logger_options(log_options)
    return logger

if __name__ == "__main__":  
    CONSOLE.clear_screen()
    if BANNER_DISPLAY:
        print(CONSOLE.get_app_banner(selection="random", banner_lst=BANNERS))

    print(f"- CUR_DIR: '{CUR_DIR}'")
    print(f"- DATA_DIR:'{DATA_DIR}'")
    print(f"- LOG_DIR: '{LOG_DIR}'")
    print(f"- OUT_DIR: '{OUT_DIR}'")
