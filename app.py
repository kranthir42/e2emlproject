from src.e2emlproject.logger import logging
from src.e2emlproject.exception import CustomException
from src.e2emlproject.components.data_ingestion import DataIngestion, DataIngestionConfig
import sys

if __name__ == "__main__":
    logging.info("The execution has started")
    
    try:
        data_ingestion_config=DataIngestionConfig()
        data_ingestion = DataIngestion()
        train_data_path,test_data_path = data_ingestion.initiate_data_ingestion()
        
    except Exception as e:
        logging.info("custom exception")
        raise CustomException(e, sys)
   