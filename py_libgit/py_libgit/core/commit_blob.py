import logging, py_libgit.settings
logger = logging.getLogger(__name__)

import os

class CommitBlob:
    def __init__(self, repo):
        logger.info('Create an Commit object')

    def create_commit(self):
        logger.info('Create a new commit message')
        return '123'
