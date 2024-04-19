from src.e2emlproject.logger import logging
from src.e2emlproject.exception import CustomException
from src.e2emlproject.components.data_ingestion import DataIngestion, DataIngestionConfig
from src.e2emlproject.components.data_transformation import DataTrasnformation, DataTransformationConfig
from src.e2emlproject.components.model_trainer import ModelTrainer,ModelTrainerConfig
import sys

if __name__ == "__main__":
    logging.info("The execution has started")
    
    try:
        # data_ingestion_config = DataIngestionConfig()
        data_ingestion = DataIngestion()
        train_data_path,test_data_path = data_ingestion.initiate_data_ingestion()
        #data_transformation_config = DataTransformationConfig()
        data_transformation =DataTrasnformation()
        train_arr, test_arr, _ = data_transformation.initiate_data_transformation(train_data_path, test_data_path)
        model_trainer = ModelTrainer()
        print(model_trainer.initiate_model_trainer(train_arr, train_arr))
        
    except Exception as e:
        logging.info("custom exception")
        raise CustomException(e, sys)
   