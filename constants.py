import logging
import os
from utils import Console

# Some interresting path
CUR_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(CUR_DIR,"data")
LOG_DIR = os.path.join(CUR_DIR,"log")
# LOGFILE = os.path.join(LOG_DIR,"main.log")
OUT_DIR = os.path.join(CUR_DIR,"out")

# Other Constants
BANNER = True
CONSOLE = Console(colored=True)
LOGLEVEL_SUCCESS = 15
LOGLEVEL_DISABLE = 99999
LOGLEVEL_CONSOLE = LOGLEVEL_SUCCESS
LOGLEVEL_FILE = LOGLEVEL_DISABLE
# LOGLEVEL_FILE = logging.DEBUG

# Constants Specific to this program
OUT_FILE = os.path.join(OUT_DIR,"countries.csv")
URL_COUNTRIES = r"https://www.worldometers.info/geography/alphabetical-list-of-countries"
URL_WIKI = r"https://en.wikipedia.org/wiki/"

# To generate Banner, visit https://patorjk.com/software/taag/#p=display&f=Graffiti&t=Type%20Something%20
banner_lst = [
r"""
   _____      _                           _        _           
  / ____|    | |                         | |      (_)          
 | |  __  ___| |_    ___ ___  _   _ _ __ | |_ _ __ _  ___  ___ 
 | | |_ |/ _ \ __|  / __/ _ \| | | | '_ \| __| '__| |/ _ \/ __|
 | |__| |  __/ |_  | (_| (_) | |_| | | | | |_| |  | |  __/\__ \
  \_____|\___|\__|  \___\___/ \__,_|_| |_|\__|_|  |_|\___||___/
                                                                    
""",
r"""
  ___  ____  ____     ___  _____  __  __  _  _  ____  ____  ____  ____  ___ 
 / __)( ___)(_  _)   / __)(  _  )(  )(  )( \( )(_  _)(  _ \(_  _)( ___)/ __)
( (_-. )__)   )(    ( (__  )(_)(  )(__)(  )  (   )(   )   / _)(_  )__) \__ \
 \___/(____) (__)    \___)(_____)(______)(_)\_) (__) (_)\_)(____)(____)(___/
""",
r"""
   ____  U _____ u  _____         ____   U  ___ u   _   _   _   _     _____    ____               U _____ u ____     
U /"___|u\| ___"|/ |_ " _|     U /"___|   \/"_ \/U |"|u| | | \ |"|   |_ " _|U |  _"\ u     ___    \| ___"|// __"| u  
\| |  _ / |  _|"     | |       \| | u     | | | | \| |\| |<|  \| |>    | |   \| |_) |/    |_"_|    |  _|" <\___ \/   
 | |_| |  | |___    /| |\       | |/__.-,_| |_| |  | |_| |U| |\  |u   /| |\   |  _ <       | |     | |___  u___) |   
  \____|  |_____|  u |_|U        \____|\_)-\___/  <<\___/  |_| \_|   u |_|U   |_| \_\    U/| |\u   |_____| |____/>>  
  _)(|_   <<   >>  _// \\_      _// \\      \\   (__) )(   ||   \\,-._// \\_  //   \\_.-,_|___|_,-.<<   >>  )(  (__) 
 (__)__) (__) (__)(__) (__)    (__)(__)    (__)      (__)  (_")  (_/(__) (__)(__)  (__)\_)-' '-(_/(__) (__)(__)                               
""",
r"""
 _______  _______ _________   _______  _______           _       _________ _______ _________ _______  _______ 
(  ____ \(  ____ \\__   __/  (  ____ \(  ___  )|\     /|( (    /|\__   __/(  ____ )\__   __/(  ____ \(  ____ \
| (    \/| (    \/   ) (     | (    \/| (   ) || )   ( ||  \  ( |   ) (   | (    )|   ) (   | (    \/| (    \/
| |      | (__       | |     | |      | |   | || |   | ||   \ | |   | |   | (____)|   | |   | (__    | (_____ 
| | ____ |  __)      | |     | |      | |   | || |   | || (\ \) |   | |   |     __)   | |   |  __)   (_____  )
| | \_  )| (         | |     | |      | |   | || |   | || | \   |   | |   | (\ (      | |   | (            ) |
| (___) || (____/\   | |     | (____/\| (___) || (___) || )  \  |   | |   | ) \ \_____) (___| (____/\/\____) |
(_______)(_______/   )_(     (_______/(_______)(_______)|/    )_)   )_(   |/   \__/\_______/(_______/\_______)
                                                                                                                                                  
""",
r"""
                                                                  
 (                )                            )                  
 )\ )      (   ( /(              (          ( /( (   (     (      
(()/(     ))\  )\())   (   (    ))\   (     )\()))(  )\   ))\ (   
 /(_))_  /((_)(_))/    )\  )\  /((_)  )\ ) (_))/(()\((_) /((_))\  
(_)) __|(_))  | |_    ((_)((_)(_))(  _(_/( | |_  ((_)(_)(_)) ((_) 
  | (_ |/ -_) |  _|  / _|/ _ \| || || ' \))|  _|| '_|| |/ -_)(_-< 
   \___|\___|  \__|  \__|\___/ \_,_||_||_|  \__||_|  |_|\___|/__/ 
""",
r"""                                                              
  ________        __                               __         .__               
 /  _____/  _____/  |_    ____  ____  __ __  _____/  |________|__| ____   ______
/   \  ____/ __ \   __\ _/ ___\/  _ \|  |  \/    \   __\_  __ \  |/ __ \ /  ___/
\    \_\  \  ___/|  |   \  \__(  <_> )  |  /   |  \  |  |  | \/  \  ___/ \___ \ 
 \______  /\___  >__|    \___  >____/|____/|___|  /__|  |__|  |__|\___  >____  >
        \/     \/            \/                 \/                    \/     \/              
""",
r"""
   ___                        
  / _ )___ ____  ___  ___ ____
 / _  / _ `/ _ \/ _ \/ -_) __/
/____/\_,_/_//_/_//_/\__/_/   
""",
r"""
 .---. .----..---.     .---.  .----. .-. .-..-. .-. .---. .----. .-..----. .----.
/   __}| {_ {_   _}   /  ___}/  {}  \| { } ||  `| |{_   _}| {}  }| || {_  { {__  
\  {_ }| {__  | |     \     }\      /| {_} || |\  |  | |  | .-. \| || {__ .-._} }
 `---' `----' `-'      `---'  `----' `-----'`-' `-'  `-'  `-' `-'`-'`----'`----'                                                 
""",
r"""
   ___     _                           _        _           
  / _ \___| |_    ___ ___  _   _ _ __ | |_ _ __(_) ___  ___ 
 / /_\/ _ \ __|  / __/ _ \| | | | '_ \| __| '__| |/ _ \/ __|
/ /_\\  __/ |_  | (_| (_) | |_| | | | | |_| |  | |  __/\__ \
\____/\___|\__|  \___\___/ \__,_|_| |_|\__|_|  |_|\___||___/                                    
""",
r"""
 ▄▄ • ▄▄▄ .▄▄▄▄▄     ▄▄·       ▄• ▄▌ ▐ ▄ ▄▄▄▄▄▄▄▄  ▪  ▄▄▄ ..▄▄ · 
▐█ ▀ ▪▀▄.▀·•██      ▐█ ▌▪▪     █▪██▌•█▌▐█•██  ▀▄ █·██ ▀▄.▀·▐█ ▀. 
▄█ ▀█▄▐▀▀▪▄ ▐█.▪    ██ ▄▄ ▄█▀▄ █▌▐█▌▐█▐▐▌ ▐█.▪▐▀▀▄ ▐█·▐▀▀▪▄▄▀▀▀█▄
▐█▄▪▐█▐█▄▄▌ ▐█▌·    ▐███▌▐█▌.▐▌▐█▄█▌██▐█▌ ▐█▌·▐█•█▌▐█▌▐█▄▄▌▐█▄▪▐█
·▀▀▀▀  ▀▀▀  ▀▀▀     ·▀▀▀  ▀█▄▀▪ ▀▀▀ ▀▀ █▪ ▀▀▀ .▀  ▀▀▀▀ ▀▀▀  ▀▀▀▀                                   
""",
r'''
  ▄████ ▓█████▄▄▄█████▓    ▄████▄   ▒█████   █    ██  ███▄    █ ▄▄▄█████▓ ██▀███   ██▓▓█████   ██████ 
 ██▒ ▀█▒▓█   ▀▓  ██▒ ▓▒   ▒██▀ ▀█  ▒██▒  ██▒ ██  ▓██▒ ██ ▀█   █ ▓  ██▒ ▓▒▓██ ▒ ██▒▓██▒▓█   ▀ ▒██    ▒ 
▒██░▄▄▄░▒███  ▒ ▓██░ ▒░   ▒▓█    ▄ ▒██░  ██▒▓██  ▒██░▓██  ▀█ ██▒▒ ▓██░ ▒░▓██ ░▄█ ▒▒██▒▒███   ░ ▓██▄   
░▓█  ██▓▒▓█  ▄░ ▓██▓ ░    ▒▓▓▄ ▄██▒▒██   ██░▓▓█  ░██░▓██▒  ▐▌██▒░ ▓██▓ ░ ▒██▀▀█▄  ░██░▒▓█  ▄   ▒   ██▒
░▒▓███▀▒░▒████▒ ▒██▒ ░    ▒ ▓███▀ ░░ ████▓▒░▒▒█████▓ ▒██░   ▓██░  ▒██▒ ░ ░██▓ ▒██▒░██░░▒████▒▒██████▒▒
 ░▒   ▒ ░░ ▒░ ░ ▒ ░░      ░ ░▒ ▒  ░░ ▒░▒░▒░ ░▒▓▒ ▒ ▒ ░ ▒░   ▒ ▒   ▒ ░░   ░ ▒▓ ░▒▓░░▓  ░░ ▒░ ░▒ ▒▓▒ ▒ ░
  ░   ░  ░ ░  ░   ░         ░  ▒     ░ ▒ ▒░ ░░▒░ ░ ░ ░ ░░   ░ ▒░    ░      ░▒ ░ ▒░ ▒ ░ ░ ░  ░░ ░▒  ░ ░
░ ░   ░    ░    ░         ░        ░ ░ ░ ▒   ░░░ ░ ░    ░   ░ ░   ░        ░░   ░  ▒ ░   ░   ░  ░  ░  
      ░    ░  ░           ░ ░          ░ ░     ░              ░             ░      ░     ░  ░      ░  
                          ░                                                                           
'''
]


if __name__ == "__main__":  
    CONSOLE.clear_screen()
    if BANNER:
        print(CONSOLE.get_app_banner(selection="random", banner_lst=banner_lst))

    print(f"- CUR_DIR: '{CUR_DIR}'")
    print(f"- DATA_DIR:'{DATA_DIR}'")
    print(f"- LOG_DIR: '{LOG_DIR}'")
    print(f"- OUT_DIR: '{OUT_DIR}'")
