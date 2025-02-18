#Information executed by the function can be stored or logged here
import logging
import os
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log" #filename

log_path = os.path.join(os.getcwd(), "logs")#path to the log file

os.makedirs(log_path, exist_ok=True)

LOG_FILEPATH = os.path.join(log_path, LOG_FILE)


logging.basicConfig(
    level=logging.INFO,
    filename=LOG_FILEPATH,
    format = "[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
)