import logging, logging.config
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('libgit')

import os

class HeadRef:
    def __init__(self, repo_name):
        logger.info('Create a new Repo')
        self.pwd = os.getcwd()
        head_file = os.path.join(self.pwd, repo_name, '.git', 'HEAD')
        with open(head_file, 'w') as f:
            f.write('ref: refs/heads/master')
