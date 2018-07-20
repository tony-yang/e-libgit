import logging, py_libgit.settings
logger = logging.getLogger(__name__)

from py_libgit.core.repo import Repo
from py_libgit.core.objects import Objects

class Add:
    def __init__(self):
        logger.info('Create the Add object')
        self.repo = Repo()
        self.objects = Objects(self.repo)

    def create_blob(self, pathname):
        '''Create a new blob under the object directory that saves the actual file content

        Return:
        The hash of the blob object, which is also the filename

        Keyword arguments:
        pathname -- the name of the file to be added into the repo
        '''
        self.pathname = pathname
        blob_hash = self.objects.create_objects(self.pathname)
        return blob_hash
