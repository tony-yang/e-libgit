import logging, py_libgit.settings
logger = logging.getLogger(__name__)

import os

class HeadRef:
    def __init__(self, repo_name):
        logger.info('Create a new Repo')
        self.pwd = os.getcwd()
        head_file = os.path.join(self.pwd, repo_name, '.git', 'HEAD')
        with open(head_file, 'w') as f:
            f.write('ref: refs/heads/master')
