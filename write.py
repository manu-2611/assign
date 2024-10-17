
import logging, json
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from config import RESULT_PATH
from datetime import datetime

class WriteFIle():

    def __init__(self,):
        self.file_path = f"{RESULT_PATH}result.json"

    def write_text_file(self, data):

        try:
            with open(self.file_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)
            logger.info(f"Data saved to {self.file_path} successfully.")

        except Exception as e:
            logger.error(f"Failed to save data to JSON: {e}")