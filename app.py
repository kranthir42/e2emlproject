from src.e2emlproject.logger import logging
from src.e2emlproject.exception import CustomException
import sys

if __name__ == "__main__":
    logging.info("The execution has started")
    
    try:
        a = 1/0
    except Exception as e:
        logging.info("custom exception")
        raise CustomException(e, sys)