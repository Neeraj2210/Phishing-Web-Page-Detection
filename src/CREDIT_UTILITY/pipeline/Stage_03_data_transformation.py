from CREDIT_UTILITY.config.configuration import ConfigurationManager
from CREDIT_UTILITY.components.data_tranformation import DataTransformation
from CREDIT_UTILITY.Exception import CustomException
from CREDIT_UTILITY.logger import logger
from pathlib import Path


STAGE_NAME = "Data Transformation stage"

class DataTransformationTrainingPipeline:
    def __init__(self):
        pass


    def main(self):
        try:
            with open(Path("artifacts/data_validation/status.txt"), "r") as f:
                status = f.read().split(" ")[-1]

            if status == "True":
                config = ConfigurationManager()
                data_transformation_config = config.get_data_transformation_config()
                data_transformation = DataTransformation(config=data_transformation_config)
                data_transformation.train_test_spliting()
                data_transformation.inititate_data_transformation()
        except Exception as e:
                error = CustomException(e, sys)
                logger.info(error.error_message)





if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = DataTransformationTrainingPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
            error = CustomException(e, sys)
            logger.info(error.error_message)