import logging
import settings

# Set up logging.
logging.getLogger('').setLevel(logging.DEBUG)
formatter = logging.Formatter(
  '%(asctime)s %(levelname)-8s %(message)s', '%y/%m/%d %H:%M:%S'
)
file_logger = logging.FileHandler(settings.LOG_PATH, 'a')
file_logger.setFormatter(formatter)
logging.getLogger('').addHandler(file_logger)
