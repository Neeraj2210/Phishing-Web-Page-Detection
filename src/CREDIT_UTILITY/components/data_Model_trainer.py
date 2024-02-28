import pandas as pd
import os
import sys
from xgboost import XGBClassifier 
import joblib
from CREDIT_UTILITY.logger import logger
from CREDIT_UTILITY.Exception import CustomException
from CREDIT_UTILITY.entity.config_entity import ModelTrainerConfig


class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    
    def train(self):
        train_data = pd.read_csv(self.config.train_data_path)
        test_data = pd.read_csv(self.config.test_data_path)


        train_x = train_data.drop([self.config.target_column], axis=1)
        test_x = test_data.drop([self.config.target_column], axis=1)
        train_y = train_data[[self.config.target_column]]
        test_y = test_data[[self.config.target_column]]

        
        xgb_classifier = XGBClassifier(
                        learning_rate=self.config.learning_rate,
                        n_estimators=self.config.n_estimators,
                        max_depth=self.config.max_depth,
                        min_child_weight=self.config.min_child_weight,
                        gamma=self.config.gamma,
                        subsample=self.config.subsample,
                        colsample_bytree=self.config.colsample_bytree,
                        objective='binary:logistic',
                        nthread=-1,
                        seed=42
)

        xgb_classifier.fit(train_x, train_y)

        joblib.dump(xgb_classifier, os.path.join(self.config.root_dir, self.config.model_name))
        logger.info("Model Training Completed")