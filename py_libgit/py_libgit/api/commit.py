import logging, py_libgit.settings
logger = logging.getLogger(__name__)

from py_libgit.core.commit_blob import CommitBlob
from py_libgit.core.repo import Repo

class Commit:
    def __init__(self):
        logger.info('Create the Commit object')
        self.repo = Repo()

    def create_commit(self, author, commit_message, root_tree_entry):
        '''Create a new commit under the object directory to save the current working history

        Return:
        The hash of the commit entry
        '''
        commit_hash = self.repo.create_commit(author, commit_message, root_tree_entry)
        return commit_hash
