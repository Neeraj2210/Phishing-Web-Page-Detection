import os
import sys
from CREDIT_UTILITY.logger import logger
from CREDIT_UTILITY.Exception import CustomException
from CREDIT_UTILITY.entity.config_entity import (DataValidationConfig)
import pandas as pd

class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def validate_all_columns(self) -> bool:
        try:
            validation_status = None

            data = pd.read_csv(self.config.unzip_data_dir)
            all_cols = list(data.columns)

            all_schema = self.config.all_schema

            # Initialize validation status
            validation_status = True

            # Check for column presence and data type
            for col, dtype in all_schema.items():
                if col not in all_cols:
                    validation_status = False
                    break
                elif data[col].dtype != dtype:
                    validation_status = False
                    break

            # Write validation status to file
            with open(self.config.STATUS_FILE, 'w') as f:
                f.write(f"Validation status: {validation_status}")

            return validation_status
        
        except Exception as e:
            error = CustomException(e, sys)
            logger.info(error.error_message)
