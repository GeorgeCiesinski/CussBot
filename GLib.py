import os
import logging

"""
George's Library of frequently used methods.
"""


def create_dir(path):

    try:
        os.mkdir(path)
    except OSError as error:
        logger.exception('Creation of the directory %f failed.' % path)
    except:
        logger.exception("Failed to configure scraper.")
        raise
    else:
        logger.info('Successfully created the directory %s.' % path)


# Log file directory goes here
log_file_directory = 'Logs/database.log'
# Logger setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# Formatter and FileHandler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s : %(message)s')
file_handler = logging.FileHandler(log_file_directory)
file_handler.setFormatter(formatter)
# Adds FileHandler to Logger
logger.addHandler(file_handler)
