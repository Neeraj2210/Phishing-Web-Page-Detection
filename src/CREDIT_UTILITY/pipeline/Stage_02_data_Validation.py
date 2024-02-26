from CREDIT_UTILITY.config.configuration import ConfigurationManager
from CREDIT_UTILITY.components.data_validation import DataValidation
from CREDIT_UTILITY.Exception import CustomException
from CREDIT_UTILITY.logger import logger

STAGE_NAME='Data Validation stage'

class DataValidationTrainingPipeline:

    def __init__(self):
        pass

    def main(self):
        
            config = ConfigurationManager()
            data_validation_config = config.get_data_validation_config()
            data_validation = DataValidation(config=data_validation_config)
            data_validation.validate_all_columns()
        


if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = DataValidationTrainingPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        error = CustomException(e, sys)
        logger.info(error.error_message)
