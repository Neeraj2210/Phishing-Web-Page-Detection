from src.CREDIT_UTILITY.logger import logger
from src.CREDIT_UTILITY.Exception import CustomException
from src.CREDIT_UTILITY.pipeline.Stage_01_data_Ingestion import DataIngestionTrainingPipeline
from src.CREDIT_UTILITY.pipeline.Stage_02_data_Validation import DataValidationTrainingPipeline


STAGE_NAME='Data Ingestion stage'
try:
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
    obj = DataIngestionTrainingPipeline()
    obj.main()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
        error = CustomException(e, sys)
        logger.info(error.error_message)

STAGE_NAME='Data Validation stage'
try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = DataValidationTrainingPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
        error = CustomException(e, sys)
        logger.info(error.error_message)
