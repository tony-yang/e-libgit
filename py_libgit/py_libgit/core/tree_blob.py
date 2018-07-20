import logging, py_libgit.settings
logger = logging.getLogger(__name__)

class TreeBlob:
    def __init__(self, repo):
        logger.info('Create the Tree object')
        self.repo = repo

    def create_tree(self):
        logger.info('Create a new tree')
        return '123'
