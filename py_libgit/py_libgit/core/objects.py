import logging, py_libgit.settings
logger = logging.getLogger(__name__)

import os
from py_libgit.core.object import Object

class Objects:
    def __init__(self, repo):
        logger.info('Create an Objects object')
        self.pwd = os.getcwd()
        self.repo = repo

    def get_git_root(self, current_dir):
        while not os.path.exists(os.path.join(current_dir, '..', '.git')):
            current_dir = os.path.dirname(current_dir)
            if '/' == current_dir:
                raise NotGitRepoError(current_dir, 'Not a git repository. Please run `git init` at the top-most level of this project')
        current_dir = os.path.join(current_dir, '.git')
        return current_dir

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
