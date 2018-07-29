import logging, py_libgit.settings
logger = logging.getLogger(__name__)

from py_libgit.core.tree_blob import TreeBlob
from py_libgit.core.repo import Repo

class Tree:
    def __init__(self):
        logger.info('Create the Tree object')
        self.repo = Repo()

    def create_tree(self):
        '''Create a new tree under the object directory to save the tree structure of the repository

        Return:
        the hash of the tree entry
        '''
        tree_entry = self.repo.create_tree()
        return tree_entry
