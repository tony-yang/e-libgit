import logging, py_libgit.settings
logger = logging.getLogger(__name__)

import os

class HeadRef:
    def __init__(self):
        logger.info('Create a new HEAD Ref')
        self.pwd = os.getcwd()

    def create_head_ref_file(self, repo_name, bare_repo=False):
        '''Create the HEAD file that holds the hash reference pointing to the top of the working tree

        Keyword arguments:
        repo_name -- the name of the repository
        bare_repo -- specify if this is a bare repo (default False)
        '''
        if bare_repo:
            head_file = os.path.join(self.pwd, repo_name, 'HEAD')
        else:
            head_file = os.path.join(self.pwd, repo_name, '.git', 'HEAD')

        with open(head_file, 'w') as f:
            f.write('ref: refs/heads/master')
