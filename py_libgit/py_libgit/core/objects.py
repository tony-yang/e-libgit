import logging, py_libgit.settings
logger = logging.getLogger(__name__)

import os
from py_libgit.core.object import Object

class Objects:
    def __init__(self, repo):
        logger.info('Create an Objects object')
        self.pwd = os.getcwd()
        self.repo = repo

    def create_objects_dir(self, repo_name, bare_repo=False):
        '''Create the objects directory for holding the git objects

        Keyword arguments:
        repo_name -- the name of the repository
        bare_repo -- specify if this is a bare repo (default False)
        '''
        if bare_repo:
            objects_dir = os.path.join(self.pwd, repo_name, 'objects')
        else:
            objects_dir = os.path.join(self.pwd, repo_name, '.git', 'objects')

        os.makedirs(objects_dir, mode=0o644)

    def create_object(self, pathname):
        full_pathname = os.path.join(self.pwd, pathname)
        blob_object = Object(self.repo)
        content_hash = blob_object.create_blob_object(pathname)
        return content_hash
