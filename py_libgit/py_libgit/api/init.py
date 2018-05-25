import logging, py_libgit.settings
logger = logging.getLogger(__name__)

from py_libgit.core.repo import Repo

class Init:
    def __init__(self, repo_name):
        logger.info('Create the Init object')
        self.repo_name = repo_name

    def create_git_repo(self, bare_repo=False):
        self.repo = Repo()
        if bare_repo:
            self.repo.create_bare_repo(self.repo_name)
        else:
            self.repo.create_repo(self.repo_name)
