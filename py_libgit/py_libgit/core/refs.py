import logging, logging.config
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('libgit')

import os

class Refs:
    def __init__(self, repo_name):
        logger.info('Create the Refs object')
        self.pwd = os.getcwd()
        refs_dir = os.path.join(self.pwd, repo_name, '.git', 'refs', 'heads')
        os.makedirs(refs_dir, mode=0o644)
