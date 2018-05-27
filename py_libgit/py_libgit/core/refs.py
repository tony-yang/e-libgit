import logging, py_libgit.settings
logger = logging.getLogger(__name__)

import os

class Refs:
    def __init__(self):
        logger.info('Create a Refs object')
        self.pwd = os.getcwd()

    def create_refs_dir(self, repo_name, bare_repo=False):
        '''Create the refs directory for holding the hash reference to commits

        Keyword arguments:
        repo_name -- the name of the repository
        bare_repo -- specify if this is a bare repo (default False)
        '''
        if not bare_repo:
            refs_dir = os.path.join(self.pwd, repo_name, '.git', 'refs', 'heads')
        else:
            refs_dir = os.path.join(self.pwd, repo_name, 'refs', 'heads')

        os.makedirs(refs_dir, mode=0o644)
