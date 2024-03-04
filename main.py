from src.CREDIT_UTILITY.logger import logger
from src.CREDIT_UTILITY.Exception import CustomException
from src.CREDIT_UTILITY.pipeline.Stage_01_data_Ingestion import DataIngestionTrainingPipeline
from src.CREDIT_UTILITY.pipeline.Stage_02_data_Validation import DataValidationTrainingPipeline
from src.CREDIT_UTILITY.pipeline.Stage_03_data_transformation import DataTransformationTrainingPipeline
from src.CREDIT_UTILITY.pipeline.Stage_04_Model_Trainer import ModelTrainerTrainingPipeline
from src.CREDIT_UTILITY.pipeline.Stage_05_Model_Evaluation import ModelEvaluationTrainingPipeline

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



STAGE_NAME='Data Transformation stage'
try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = DataTransformationTrainingPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")

except Exception as e:
        error = CustomException(e, sys)
        logger.info(error.error_message)


STAGE_NAME = "Model Trainer stage"

try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = ModelTrainerTrainingPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
        error = CustomException(e, sys)
        logger.info(error.error_message)



STAGE_NAME = "Model evaluation stage"
try:
   logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<") 
   data_ingestion = ModelEvaluationTrainingPipeline()
   data_ingestion.main()
   logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
except Exception as e:
        error = CustomException(e, sys)
        logger.info(error.error_message)



