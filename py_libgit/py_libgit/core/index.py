import logging, py_libgit.settings
logger = logging.getLogger(__name__)

import os

class Index:
    def __init__(self):
        logger.info('Create an Index object')
        git_root = self.get_git_root(os.getcwd())
        self.index_file = os.path.join(git_root, 'index')

    def get_git_root(self, current_dir=os.getcwd()):
        while not os.path.exists(os.path.join(current_dir, '..', '.git')):
            current_dir = os.path.dirname(current_dir)
            if '/' == current_dir:
                raise NotGitRepoError(current_dir, 'Not a git repository. Please run `git init` at the top-most level of this project')

        return current_dir

    def update_index(self, pathname):
        index_file = os.path.join(self.get_git_root(), pathname)
        with open(index_file, 'a') as f:
            f.write(pathname)
