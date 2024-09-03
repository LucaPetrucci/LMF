import logging

class CustomFormatter(logging.Formatter):
    """Logging colored formatter, adapted from https://stackoverflow.com/a/56944256/3638629"""

    grey = '\x1b[38;21m'
    blue = '\x1b[38;5;39m'
    yellow = '\x1b[38;5;226m'
    red = '\x1b[38;5;196m'
    bold_red = '\x1b[31;1m'
    reset = '\x1b[0m'

    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: self.blue + self.fmt + self.reset,
            logging.INFO: self.grey + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.bold_red + self.fmt + self.reset,
            logging.CRITICAL: self.red + self.fmt + self.reset
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
    


fmt = '%(asctime)s - [%(name)s] - %(levelname)s - %(message)s - (%(filename)s:%(lineno)d)'    
formatter = CustomFormatter(fmt)

# logging for LMF API
logger_LMF_API = logging.getLogger('LMF_API')
logger_LMF_API.setLevel(logging.DEBUG) 
console_handler_LMF_API = logging.StreamHandler() 
console_handler_LMF_API.setLevel(logging.DEBUG)  
console_handler_LMF_API.setFormatter(formatter)
logger_LMF_API.addHandler(console_handler_LMF_API)

#logging for LMF istance
logger_LMF_istance = logging.getLogger('LMF_istance')
logger_LMF_istance.setLevel(logging.DEBUG)  
console_handler_LMF_istance = logging.StreamHandler()  
console_handler_LMF_istance.setLevel(logging.DEBUG)  
console_handler_LMF_istance.setFormatter(formatter)
logger_LMF_istance.addHandler(console_handler_LMF_istance)

#logging for LPP
logger_LPP = logging.getLogger('LPP')
logger_LPP.setLevel(logging.DEBUG)  
console_handler_LPP = logging.StreamHandler()  
console_handler_LPP.setLevel(logging.DEBUG)  
console_handler_LPP.setFormatter(formatter)
logger_LPP.addHandler(console_handler_LPP)

#logging for NRPPa
logger_NRPPa = logging.getLogger('NRPPa')
logger_NRPPa.setLevel(logging.DEBUG) 
console_handler_NRPPa = logging.StreamHandler()  
console_handler_NRPPa.setLevel(logging.DEBUG)  
console_handler_NRPPa.setFormatter(formatter)
logger_NRPPa.addHandler(console_handler_NRPPa)

#logging for Location Algo.
logger_LocAlg = logging.getLogger('LOC-ALG')
logger_LocAlg.setLevel(logging.DEBUG)  
console_handler_LocAlg = logging.StreamHandler()  
console_handler_LocAlg.setLevel(logging.DEBUG)  
console_handler_LocAlg.setFormatter(formatter)
logger_LocAlg.addHandler(console_handler_LocAlg)

