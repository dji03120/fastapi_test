import sys,os
import logging
import traceback
import os, functools, io
from datetime import datetime
from logging.handlers import RotatingFileHandler


def get_rotating_logger(
    name: str       = "rotating_logger",
    max_bytes: int  = 1024 * 1024 * 50,  # 50MB
    backup_count: int = 5,
    level: int = logging.DEBUG
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        try:
            handler = RotatingFileHandler( 
                f"/var/log/ETRI_ANNOTATION/{name}.log", 
                maxBytes=max_bytes, backupCount=backup_count,
                encoding='utf-8' )
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        except (RuntimeError, ValueError, TypeError, AttributeError, KeyError, IndexError, OSError) as e: pass
    return logger



class MyLogger:
    def __init__(self, logger):
        self.logger = logger
    
    def info (self, msg): 
        if self.logger !=None : self.logger.info(msg)
        print(f"{str(datetime.now())} {msg}")

    def debug (self, msg): 
        if self.logger !=None : self.logger.debug(msg)
        print(f"{str(datetime.now())} {msg}")

    def error (self, msg): 
        if self.logger !=None : self.logger.error(msg)
        print(f"{str(datetime.now())} {msg}")
        
    def warning (self, msg):
        if self.logger !=None : self.logger.warning(msg)
        print(f"{str(datetime.now())} {msg}")





def try_except(logger=None, default_return=None, catch=(Exception,)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:    return func(*args, **kwargs)
            except catch as e:
                err_msg = f"[ERROR in {func.__name__}] {traceback.format_exc()}"
                if logger:  logger.error(err_msg)
                else:       print(err_msg)
                return default_return
        return wrapper
    return decorator





if __name__ == "__main__":
    logger = get_rotating_logger("test_logger2")
    logger = MyLogger(logger)

    @try_except(logger=logger)
    def hello():
        print("a"+1)

    hello()
