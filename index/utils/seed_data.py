from django.db.backends.utils import logger
from index.services import SP500


def create_indices():
    """ Creates all Indices """
    logger.info('Creating Indices...')
    SP500().create_index()
    logger.info('Created Indices')


def create_constituents():
    """ Creates all of the Indices constituents """
    logger.info('Adding Indices constituents...')
    SP500().add_constituents()
    logger.info('Added Indices constituents')