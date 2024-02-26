import os
import sys
from pathlib import Path
from urllib.request import Request
import zipfile
from CREDIT_UTILITY.logger import logger
from CREDIT_UTILITY.utils.common import get_size
from CREDIT_UTILITY.Exception import CustomException
from CREDIT_UTILITY.entity.config_entity import (DataIngestionConfig)

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_file(self):
        print("Source URL:", self.config.source_URL)
        print("Local path",self.config.local_data_file)
        retries = 3  # Number of retry attempts
        for attempt in range(retries):
            try:
                if not os.path.exists(self.config.local_data_file):
                    filename, headers = request.urlretrieve(
                    url=self.config.source_URL,
                    filename=self.config.local_data_file
                )
                    logger.info(f"{filename} downloaded with the following info: \n{headers}")
                else:
                    logger.info(f"File already exists of size: {get_size(Path(self.config.local_data_file))}")
            
            except Exception as e:
                 error = CustomException(e, sys)
                 logger.info(error.error_message)
       

    def extract_zip_file(self):
        """
        zip_file_path: str
        Extracts the zip file into the data directory
        Function returns None
        """
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)
  