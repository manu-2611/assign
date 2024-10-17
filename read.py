import os,json, math, logging, time
from config import LIST_OF_KEYS, RETRY_COUNT, MAX_WORKER, CHUNK_SIZE
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from concurrent.futures import ThreadPoolExecutor, as_completed


class Calculation:
    def __init__(self, json_obj):
        self.json_obj = json_obj
        self.keys = LIST_OF_KEYS
        self.error_count= 0
        self.processed_count= 0

    def safe_sqrt(self, number):
         return math.sqrt(number)

        # if not isinstance(number, (int, float)):
        #     logger.warning(f"Attempted to compute square root of an invalid number type: {number}")
        #     return None
        
        # if number <= 0:
        #     logger.warning(f"Attempted to compute square root of an invalid number: {number}")
        #     return None

        # else:

    def retry_sqrt(self, number, retries=RETRY_COUNT):
        """
        Attempt to compute the square root of a number with a predefined retry mechanism.

        Args:
            number (float): The number to calculate the square root of.
            retries (int): The maximum number of retry attempts for invalid inputs.

        Returns:
            float or None: The square root of the number if successful; None if all attempts fail.
        """
        attempt = 0
        while attempt < retries:
            try:
                if attempt == 0:
                    result = self.safe_sqrt(number)

                elif attempt == 1:
                    result = self.safe_sqrt(int(number))

                elif attempt == 2:
                    result = self.safe_sqrt(abs(number))

                if result is not None:
                    return result
                
            except:
            
                attempt += 1
                logger.info(f"Retrying... Attempt {attempt} for number: {number}")
                time.sleep(1)

        logger.error(f"Failed to compute square root after {retries} attempts for number: {number}")
        return None

    def process_chunk(self, chunk):
        results = []

        for obj in chunk:
            number = obj.get(self.keys[0])
            result = self.retry_sqrt(number=number)

            if result is None:
                self.error_count += 1
            else:
                self.processed_count += 1

            results.append({"original_value": number, "calculated_value": result})

            if self.error_count >= 10:
                logger.error(f"Execution stopped due to too many errors. "
                             f"Errors: {self.error_count}, "
                             f"Processed Data: {self.processed_count}, "
                             f"Remaining Data: {len(chunk) - self.processed_count}")
                return results   # Stop processing this chunk if errors exceed 10

        return results

    def calculate_sqrt(self):
        """Calculate square roots for values in the provided JSON object."""
        json_obj = self.json_obj
        key_name = self.keys[0]  
        
        if not any(obj.get(key_name) is not None for obj in json_obj):
            logger.warning("NO MATCHING KEY FOUND")
            return None
        
        results = []
        chunk_size = CHUNK_SIZE
        max_workers = MAX_WORKER
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Split the json_obj into chunks of up to 100
            futures = []
            for i in range(0, len(json_obj), chunk_size):
                chunk = json_obj[i:i + chunk_size]
                futures.append(executor.submit(self.process_chunk, chunk))

            for future in as_completed(futures):
                chunk_results = future.result()
                if chunk_results is not None:
                    results.extend(chunk_results)

                    # Check if the last chunk stopped processing due to errors
                    if len(chunk_results) < len(chunk):  # Fewer results means it hit error count limit
                        logger.info("Processing stopped due to too many errors in a chunk.")
                        break  # Exit the loop if errors limit was hit

        logger.info("All numbers processed up to the error limit.")
        return results


class GetFiles():

    def __init__(self, path):
        self.path = path
        pass

    def get_list_of_all_files(self):

        list_of_files = os.listdir(self.path)
        return list_of_files

class ReadFIle():

    def __init__(self, file_name):
        self.file_name = file_name
        pass


    def read_json(self):
        with open(self.file_name, "r") as json_file:
            json_obj = json.load(json_file)
            return json_obj


        pass