import sys
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from src.e2emlproject.logger import logging
from src.e2emlproject.exception import CustomException
from src.e2emlproject.utils import save_object
import os

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts', 'preprocessor.pkl')
    
class DataTrasnformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()
        
    def get_data_transformation_object(self):
        '''
        does your data transformation
        '''
        try:
            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course"
            ]
            num_pipeline = Pipeline(steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("scalar", StandardScaler())
            ])
            cat_pipeline = Pipeline(steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("onehot", OneHotEncoder()),
                ("scalar", StandardScaler(with_mean = False))
            ])
            
            logging.info(f"categorical columns: {categorical_columns}")
            logging.info(f"numerical columns: {numerical_columns}")
            
            preprocessor = ColumnTransformer(
                [("num_pipeline", num_pipeline, numerical_columns),
                 ("cat_pipeline", cat_pipeline, categorical_columns)
                ]
            )
            return preprocessor
        
        except Exception as e:
            raise CustomException(e, sys)
        
    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            logging.info("reading train and test df's")
            preprocessing_obj = self.get_data_transformation_object()
            target_col_name = "math_score"
            numerical_columns = ["writing_score", "reading_score"]
            input_features_train_df = train_df.drop(columns=[target_col_name], axis=1)
            target_feature_train_df = train_df[target_col_name]
            input_features_test_df = test_df.drop(columns=[target_col_name], axis=1)
            target_feature_test_df = test_df[target_col_name]
            logging.info("applying preprocessor on data")
            input_feature_train_arr = preprocessing_obj.fit_transform(input_features_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_features_test_df)
            
            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]
            logging.info("saving pickle file")
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )
            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )
            
        except Exception as e:
            raise CustomException(e, sys)
