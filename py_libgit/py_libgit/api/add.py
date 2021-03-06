import logging, py_libgit.settings
logger = logging.getLogger(__name__)

from py_libgit.core.repo import Repo

class Add:
    def __init__(self):
        logger.info('Create the Add object')
        self.repo = Repo()

    def create_blob(self, pathname):
        '''Create a new blob under the object directory that saves the actual file content

        Return:
        The hash of the blob object, which is also the filename

        Keyword arguments:
        pathname -- the name of the file to be added into the repo
        '''
        blob_hash = self.repo.add_objects(pathname)
        return blob_hash
