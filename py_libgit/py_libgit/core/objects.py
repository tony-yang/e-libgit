import logging, py_libgit.settings
logger = logging.getLogger(__name__)

import os

class Objects:
    def __init__(self, repo_name):
        logger.info('Create the Objects object')
        self.pwd = os.getcwd()
        objects_dir = os.path.join(self.pwd, repo_name, '.git', 'objects')
        os.makedirs(objects_dir, mode=0o644)
