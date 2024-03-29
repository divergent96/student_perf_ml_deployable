'''
Data ingestion component.
Contains all functions and code required to fetch and ready the data for processing.
'''
# Standard Libs
import os
import sys
from dataclasses import dataclass

# 
import pandas as pd
import numpy as np

# Custom imports
from src.exception import CustomException
from src.logger import logging

from src.components.data_transformation import DataTransformation, DataTransformationConfig 
from src.components.model_trainer import ModelTrainer, ModelTrainingConfig

# Sklearn
from sklearn.model_selection import train_test_split

# Misc

@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts','train.csv')
    test_data_path: str = os.path.join('artifacts','test.csv')
    raw_data_path: str = os.path.join('artifacts','data.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Start of Data ingestion.")
        try:
            df = pd.read_csv('notebook\data\data.csv')

            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok = True)

            df.to_csv(self.ingestion_config.raw_data_path, index = False, header = True)

            logging.info("Start Train test split")

            train_set, test_set = train_test_split(df, train_size = 0.8, random_state=7)

            train_set.to_csv(self.ingestion_config.train_data_path, index = False, header = True)
            test_set.to_csv(self.ingestion_config.test_data_path, index = False, header = True)

            logging.info("Train test split completed!")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        except Exception as e:
            raise CustomException(e,sys)

if __name__ == "main":
    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()

    data_transformation = DataTransformation()
    train_arr, test_arr,_ = data_transformation.get_data_transformer_object

    modeltrainer = ModelTrainer()
    print(modeltrainer.initiate_model_trainer(train_arr, test_arr))
    
